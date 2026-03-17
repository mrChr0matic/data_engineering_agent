from langchain_core.messages import SystemMessage, ToolMessage
from llm.azure_openai import get_llm
from rag.retriever import get_retriever
from tools.sql_tool import run_sql
from tools.github_tool import get_github_tools
from pydantic import BaseModel
from typing import Literal
import asyncio

class Route(BaseModel):
    route: Literal["rag", "sql", "github", "chat"]

llm = get_llm()

async def init_tools():
    github_tools = await get_github_tools()
    return [run_sql] + github_tools

tools = asyncio.run(init_tools())
llm_with_tools = llm.bind_tools(tools)
router_llm = llm.with_structured_output(Route)
retriever = get_retriever()


def router_node(state):
    question = state["messages"][-1].content

    prompt = f"""
        You are a query router for an AI agent.

        Classify the user query into one of these routes:
        - rag
        - sql
        - github
        - chat

        Return ONLY valid JSON in this format:
        {{"route": "<route>"}}

        Query:
        {question}
    """
    route = router_llm.invoke(prompt)
    print("selected route:", route.route)
    return {"route": route.route}


def llm_node(state):
    print("\n===== LLM NODE =====")
    messages = state["messages"]

    print("Messages passed to LLM:")
    for m in messages:
        print(f"  {type(m).__name__}: {str(getattr(m, 'content', ''))[:80]}")

    response = llm_with_tools.invoke(messages)

    if hasattr(response, "tool_calls") and response.tool_calls:
        print("LLM decided to call tool(s):", response.tool_calls)

    return {"messages": [response]}


def retrieval_node(state):
    print("\n===== RETRIEVAL NODE =====")
    messages = state["messages"]
    question = messages[-1].content

    print("User question:", question)

    docs = retriever.invoke(question)
    print(f"Retrieved {len(docs)} document(s)")

    context = "\n\n".join(doc.page_content for doc in docs)

    system_msg = SystemMessage(
        content=f"""You are a helpful assistant.
            Use ONLY the information from the provided context to answer the question.
            Do NOT reveal the context itself.
            Do NOT output the documents.
            Do NOT list the retrieved information verbatim.

            Context:
            {context}
        """
    )

    print("Context injected into system prompt.")
    return {"messages": [system_msg]}


async def tool_node(state):
    print("\n===== TOOL NODE =====")
    messages = state["messages"]
    last_message = messages[-1]
    tool_calls = last_message.tool_calls

    print("Tool calls received:", tool_calls)
    outputs = []

    for call in tool_calls:
        tool_name = call["name"]
        args = call["args"]

        print(f"\nExecuting tool: {tool_name}, args: {args}")

        tool = next(t for t in tools if t.name == tool_name)

        if tool_name == "run_sql":
            result = tool.invoke(args["query"])
        else:
            result = await tool.ainvoke(args)

        print("Tool result:", str(result)[:200])

        outputs.append(
            ToolMessage(
                content=str(result),
                tool_call_id=call["id"]
            )
        )

    return {"messages": outputs}
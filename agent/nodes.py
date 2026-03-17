from langchain_core.messages import SystemMessage, ToolMessage
from llm.azure_openai import get_llm
from rag.retriever import get_retriever
from tools.sql.sql_tool import run_sql
from tools.github.github_tool import get_github_tools
from pydantic import BaseModel
from typing import Literal
import asyncio

class Route(BaseModel):
    route: Literal["rag", "sql", "github", "chat", "databricks"]

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
        You are a query router for a data engineering AI agent.

        Classify the user query into one of these routes:

        rag:
        Questions about documentation or knowledge base.

        sql:
        Queries requiring database SQL execution.

        github:
        Questions about GitHub repositories or files.

        databricks:
        Questions about Databricks, Spark, Delta Lake, Unity Catalog,
        Medallion architecture, streaming pipelines, or optimization.

        chat:
        General conversation.

        Return ONLY JSON:

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
    print("\nRetrieved sources:")
    for d in docs:
        print(d.metadata.get("source"))

    context = "\n\n".join(doc.page_content for doc in docs)

    system_msg = SystemMessage(
        content=f"""
            You are a Databricks data engineering assistant.

            Use ONLY the information from the provided context.

            Focus on:
            - Delta Lake
            - Spark optimization
            - Medallion architecture
            - Unity Catalog

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
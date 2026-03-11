from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from llm.azure_openai import get_llm
from rag.retriever import get_retriever
from tools.sql_tool import run_sql

llm = get_llm()

tools = [run_sql]
llm_with_tools = llm.bind_tools(tools)

retriever = get_retriever()

# def llm_node(state):
#     messages = state["messages"]
#     response = llm_with_tools.invoke(messages)
    
#     return {
#         "messages" : messages + [response]
#     }

    
def llm_node(state):
    print("\n===== LLM NODE =====")

    messages = state["messages"]

    print("Messages passed to LLM:")
    for m in messages:
        print(f"{type(m).__name__}: {getattr(m, 'content', '')}")

    response = llm_with_tools.invoke(messages)

    print("\nLLM Response:")
    print(response)

    if hasattr(response, "tool_calls") and response.tool_calls:
        print("LLM decided to call tool(s):", response.tool_calls)

    return {
        "messages": messages + [response]
    }

# def retrieval_node(state):
#     messages = state["messages"]
#     question = messages[-1].content
    
#     docs = retriever.invoke(question)
#     context = "\n\n".join(doc.page_content for doc in docs)
    
#     messages = [
#         SystemMessage(
#             content=f"""You are a helpful assistant.
#             Use ONLY the information from the provided context to answer the question.
#             Do NOT reveal the context itself.
#             Do NOT output the documents.
#             Do NOT list the retrieved information verbatim.
#             Context:
#             {context}
#             """
#                 )
#     ] + messages
    
#     return {"messages" : messages}

def retrieval_node(state):
    print("\n===== RETRIEVAL NODE =====")

    messages = state["messages"]
    question = messages[-1].content

    print("User question:", question)

    docs = retriever.invoke(question)

    print("\nRetrieved documents:")
    for i, doc in enumerate(docs):
        print(f"\nDoc {i+1}:")
        print(doc.page_content)

    context = "\n\n".join(doc.page_content for doc in docs)

    messages = [
        SystemMessage(
            content=f"""You are a helpful assistant.
Use ONLY the information from the provided context to answer the question.
Do NOT reveal the context itself.
Do NOT output the documents.
Do NOT list the retrieved information verbatim.

Context:
{context}
"""
        )
    ] + messages

    print("\nContext injected into system prompt.")

    return {"messages": messages}

# def tool_node(state):
#     messages = state["messages"]
#     last_message = messages[-1]
    
#     tool_calls = last_message.tool_calls
    
#     outputs = []
    
#     for call in tool_calls:
#         if call['name'] == "run_sql":
#             query = call['args']['query']
            
#             result = run_sql.invoke(query)
            
#             outputs.append(
#                 ToolMessage(
#                     content=str(result),
#                     tool_call_id=call['id']
#                 )
#             )
            
#     return {"messages" : messages + outputs}

def tool_node(state):
    print("\n===== TOOL NODE =====")

    messages = state["messages"]
    last_message = messages[-1]

    tool_calls = last_message.tool_calls

    print("Tool calls received:", tool_calls)

    outputs = []

    for call in tool_calls:

        if call['name'] == "run_sql":

            query = call['args']['query']

            print("\nExecuting SQL Query:")
            print(query)

            result = run_sql.invoke(query)

            print("\nSQL Result:")
            print(result)

            outputs.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=call['id']
                )
            )

    return {"messages": messages + outputs}

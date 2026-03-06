from langchain_core.messages import AIMessage, SystemMessage
from llm.azure_openai import get_llm
from rag.retriever import get_retriever

llm = get_llm()
retriever = get_retriever()

def llm_node(state):
    '''
    Calls the LLM with current conversation messages.
    '''
    messages = state["messages"]
    response = llm.invoke(messages)
    
    return {
        "messages" : messages + [AIMessage(content=response.content)]
    }
    
def retrieval_node(state):
    messages = state["messages"]
    question = messages[-1].content
    
    docs = retriever.invoke(question)
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
    
    return {"messages" : messages}
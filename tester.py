from llm.azure_openai import get_llm
from agent.graph import build_agent
from langchain_core.messages import HumanMessage
from rag import ingest, retriever

def test_llm():
    llm = get_llm()
    
    print("Data Engineering Agent CLI")
    print("Type 'exit' to quit\n")
    
    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            break

        response = llm.invoke(user_input)

        print("\nAgent:", response.content)
        print()

def test_graph():
    agent = build_agent()
    
    print("data engineering agent")
    print("type 'exit' to quit\n" )
    
    while True:
        user_input = input("User : ")
        if user_input.lower() == 'exit':
            break
        
        state = {
            "messages" : [HumanMessage(content=user_input)]
        }
        
        result = agent.invoke(state)
        
        response = result["messages"][-1].content
        
        print("\nAgent : ", response)
        print()

if __name__ == "__main__":
    # ingest.build_vector_store()
    test_graph()
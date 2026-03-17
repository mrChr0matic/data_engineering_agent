import asyncio
from llm.azure_openai import get_llm
from agent.graph import build_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

async def test_agent():
    agent = build_agent(checkpointer=memory)
    
    print("data engineering agent")
    print("type 'exit' to quit\n")

    config = {"configurable": {"thread_id": "user_1"}}

    while True:
        user_input = input("User : ")

        if user_input.lower() == "exit":
            break

        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )

        response = result["messages"][-1].content
        print("\nAgent:", response)
        print()

if __name__ == "__main__":
    asyncio.run(test_agent())
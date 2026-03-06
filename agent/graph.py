from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import llm_node, retrieval_node

def build_agent():
    builder = StateGraph(AgentState)
    builder.add_node("retrieve", retrieval_node)
    builder.add_node("llm", llm_node)
    
    builder.set_entry_point("retrieve")
    
    builder.add_edge("retrieve", "llm")
    builder.add_edge("llm", END);
    
    return builder.compile()

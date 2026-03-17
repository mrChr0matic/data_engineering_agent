from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import llm_node, retrieval_node, tool_node, router_node

def route_tools(state):
    last_message = state["messages"][-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    return END


def build_agent(checkpointer = None):
    builder = StateGraph(AgentState)
    builder.add_node("router", router_node)
    builder.add_node("retrieve", retrieval_node)
    builder.add_node("llm", llm_node)
    builder.add_node("tools", tool_node)
    
    builder.set_entry_point("router")
    builder.add_conditional_edges(
        "router",
        lambda state : state["route"],
        {
            'rag' : 'retrieve',
            'sql' : 'retrieve',
            'databricks' : 'retrieve',
            'chat' : 'llm',
            'github' : 'llm',
        }
    )
    builder.add_edge("retrieve", "llm")

    builder.add_conditional_edges("llm", route_tools)

    builder.add_edge("tools", "llm")
    
    return builder.compile(checkpointer=checkpointer)

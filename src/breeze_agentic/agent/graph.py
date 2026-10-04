from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from breeze_agentic.core.config import get_settings


class AgentState(TypedDict):
    message: str
    response: str


def _call_openai(state: AgentState) -> AgentState:
    settings = get_settings()
    llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)
    result = llm.invoke(
        [
            SystemMessage(content="You are Breeze Agentic, a concise and helpful AI agent."),
            HumanMessage(content=state["message"]),
        ]
    )
    return {"message": state["message"], "response": str(result.content)}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("call_openai", _call_openai)
    graph.add_edge(START, "call_openai")
    graph.add_edge("call_openai", END)
    return graph.compile()


agent_graph = build_graph()


def run_agent(message: str) -> str:
    result = agent_graph.invoke({"message": message, "response": ""})
    return result["response"]

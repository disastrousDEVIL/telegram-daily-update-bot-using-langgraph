from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict

class State(TypedDict, total=False):
    input: str
    output: str
llm=ChatOpenAI(model="gpt-5-mini-2025-08-07")

def generate_update_node(state:State):
    raw_text=state["input"]
    prompt = f"""
You are preparing a daily update message that will be sent to a company's internal bot.
Rewrite the information below into a clear, professional, technical daily update.

Requirements:
• Make it around 80–120 words, but do not add unnecessary fluff.
• Keep it professional but not robotic or overly stiff.
• Use concise technical language where appropriate.
• Write the update in bullet points starting with "-".
• Vary sentence structure so it does not feel repetitive.
• Include context for each point instead of short dry statements.

Information:
{raw_text}
"""
    response=llm.invoke(prompt)
    state["output"]=response.content
    return state

builder=StateGraph(State)
builder.add_node("generate_update", generate_update_node)
builder.set_entry_point("generate_update")
builder.add_edge("generate_update", END)

graph=builder.compile()

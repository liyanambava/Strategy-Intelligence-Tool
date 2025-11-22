"""
business_strategy_langgraph.py
UPDATED: Replaced OpenAI with Local Ollama Model
"""
#.\.venv312\Scripts\Activate.ps1

import os
import streamlit as st
from typing import TypedDict
from datetime import datetime
from pymongo import MongoClient
from ddgs import DDGS as ddg
import ollama                           
from langgraph.graph import StateGraph, START, END

# ---------------------------
# MongoDB Setup
# ---------------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "business_ai_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "strategy_sessions")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# ---------------------------
# LangGraph State Definition
# ---------------------------
class State(TypedDict):
    user_input: str
    market_insights: str
    consulting_analysis: str
    strategy_plan: str
    final_report: str

# ---------------------------
# Helper Functions
# ---------------------------

def ollama_chat(model: str, prompt: str) -> str:
    """
    Wrapper for Ollama local LLM inference.
    """
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"(ollama error: {str(e)})"


def run_search(query: str, max_results: int = 3) -> list[str]:
    results = []
    try:
        with ddg() as ddgs:
            for r in ddgs(text=query, max_results=max_results):
                title = r.get("title") or ""
                body = r.get("body") or ""
                url = r.get("url") or ""
                snippet = f"{title}\n{body}\n{url}"
                results.append(snippet)
    except Exception as e:
        results.append(f"(search error: {str(e)})")
    return results


def format_markdown_section(title: str, content: str) -> str:
    return f"## {title}\n\n{content}\n\n"

# ---------------------------
# LangGraph Nodes
# ---------------------------

def analyst_node(state: State) -> dict:
    query = state["user_input"]
    search_queries = [
        f"{query} market size 2024 2025 trends",
        f"{query} competitors {query} industry analysis",
        f"{query} consumer trends 2024 2025 {query}"
    ]

    snippets = []
    for q in search_queries:
        snippets.extend(run_search(q, max_results=2))

    prompt = (
        "You are a market research analyst. Based on the following search snippets, "
        "produce a concise market-insights summary:\n\n"
        f"User Query: {query}\n\n"
        f"Snippets:\n{chr(10).join(snippets)}\n\n"
        "Return:\n"
        "- 5 key market metrics\n"
        "- 3 competitors\n"
        "- 3 trends\n"
        "- 3 risks"
    )

    summary = ollama_chat("llama3", prompt)
    return {"market_insights": summary}


def consultant_node(state: State) -> dict:
    query = state["user_input"]
    market = state["market_insights"]

    prompt = (
        "You are a business consultant. Create SWOT + PESTEL:\n\n"
        f"Query: {query}\n\n"
        f"Market Insights:\n{market}\n\n"
        "Return a structured analysis."
    )

    analysis = ollama_chat("llama3", prompt)
    return {"consulting_analysis": analysis}


def strategist_node(state: State) -> dict:
    query = state["user_input"]
    swot = state["consulting_analysis"]
    market = state["market_insights"]

    prompt = (
        "You are a business strategist. Produce:\n"
        "1) Executive summary\n"
        "2) 3-phase roadmap (short / mid / long term)\n"
        "3) KPIs\n"
        "4) Top 3 actions\n"
        "5) Risks & mitigations\n\n"
        f"Query: {query}\n\n"
        f"Market Insights:\n{market}\n\n"
        f"SWOT & PESTEL:\n{swot}"
    )

    plan = ollama_chat("llama3", prompt)
    return {"strategy_plan": plan}


def final_compile_node(state: State) -> dict:
    query = state["user_input"]
    market = state["market_insights"]
    analysis = state["consulting_analysis"]
    plan = state["strategy_plan"]

    sections = []
    sections.append(format_markdown_section("Business Query", query))
    sections.append(format_markdown_section("Market Insights (Analyst)", market))
    sections.append(format_markdown_section("Consulting Analysis (SWOT & PESTEL)", analysis))
    sections.append(format_markdown_section("Strategy Plan (Strategist)", plan))

    final_report = "\n".join(sections)

    try:
        record = {
            "timestamp": datetime.utcnow(),
            "user_query": query,
            "market_insights": market,
            "consulting_analysis": analysis,
            "strategy_plan": plan,
            "final_report": final_report
        }
        #collection.insert_one(record)
    except Exception as e:
        final_report += f"\n\n(Warning: DB save failed: {str(e)})"

    return {"final_report": final_report}

# ---------------------------
# Build LangGraph
# ---------------------------
VERBOSE = True

def log(msg: str):
    if VERBOSE:
        print(f"[DEBUG] {msg}")

def verbose_wrapper(name, fn):
    def inner(state):
        log(f"--- Entering node: {name} ---")
        out = fn(state)
        log(f"--- Finished node: {name} --- Output keys: {list(out.keys())} ---")
        return out
    return inner

builder = StateGraph(State)
builder.add_node("analyst", verbose_wrapper("analyst", analyst_node))
builder.add_node("consultant", verbose_wrapper("consultant", consultant_node))
builder.add_node("strategist", verbose_wrapper("strategist", strategist_node))
builder.add_node("final_compile", verbose_wrapper("final_compile", final_compile_node))

builder.add_edge(START, "analyst")
builder.add_edge("analyst", "consultant")
builder.add_edge("consultant", "strategist")
builder.add_edge("strategist", "final_compile")
builder.add_edge("final_compile", END)

graph = builder.compile()

# ---------------------------
# Streamlit UI
# ---------------------------
import streamlit as st

st.set_page_config(
    page_title="Strategy Intelligence Tool",
    page_icon="📊",
    layout="centered"
)

# ---- HEADER ----
st.title("📊 Strategy Intelligence Tool")
st.subheader("AI-Powered Multi-Agent Business Strategy Generator")

st.caption(
    """
    This tool uses a multi-agent pipeline (Analyst → Consultant → Strategist) 
    powered by your **local Ollama LLM** to produce investor-ready business strategies.
    """
)

# ---- SIDEBAR ----
with st.sidebar:
    st.header("⚙️ Settings")
    st.info(
        """
        **Model:** Local Ollama Model  
        **Pipeline:** Analyst → Consultant → Strategist  
        **Output:** Market insights, analysis, structured strategy plan
        """
    )
    st.markdown("---")
    st.write("💡 *Tip: Provide detailed business queries for deeper insights.*")

# ---- HISTORY INIT ----
if "session_history" not in st.session_state:
    st.session_state.session_history = []

# ---- INPUT FORM ----
st.markdown("### 📝 Enter Your Business Challenge")
st.write(
    "Describe your business problem — e.g., market entry, product launch, competitive analysis, growth strategy, etc."
)

with st.form("strategy_form"):
    user_input = st.text_area(
        "Business Query",
        height=130,
        placeholder="Example: 'Develop a market entry strategy for electric bikes in Southeast Asia...'"
    )
    submit = st.form_submit_button("🚀 Generate Strategy")

# ---- PROCESSING ----
if submit and user_input.strip():
    with st.spinner("🔍 Analyzing with multi-agent pipeline..."):
        initial_state = {
            "user_input": user_input,
            "market_insights": "",
            "consulting_analysis": "",
            "strategy_plan": "",
            "final_report": ""
        }
        result = graph.invoke(initial_state)
        final_report = result.get("final_report", "Error: No output")

    st.success("✅ Strategy Generated Successfully!")
    st.markdown("### 📘 Final Strategy Report")
    st.markdown(final_report, unsafe_allow_html=True)

    # Save history
    st.session_state.session_history.append(final_report)

# ---- FOOTER ----
st.markdown("---")
st.caption("🚀 Powered by Local AI • Multi-Agent Reasoning • Optimized for Strategic Decision-Making")

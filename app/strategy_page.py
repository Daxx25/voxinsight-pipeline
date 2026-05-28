# app/strategy_page.py
import streamlit as st

def render_strategy():
    st.title("📑 Technical Architecture & Project Strategy Brief")
    st.subheader("An engineering deep-dive on scoping choices, constraints, and product context.")

    st.markdown("""
    ### 🎯 The Problem Context
    Product Management and Customer Success leaders handle massive streams of unstructured text every day (Gong transcripts, customer chat logs, ticketing systems). Manual transcription and processing is too slow and expensive to scale. 
    
    **VoxInsight** is an intelligent orchestration layer built to parse customer conversations, categorize issues into standardized engineering segments, evaluate client sentiment, and pull out real verbatim evidence automatically.

    ---

    ### 🏗️ How it Works (System Walkthrough)
    """)

    # Architectural flow presentation widgets
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("""
        **1. Data Stream Ingestion**
        The pipeline accepts text dumps from chat lines or phone records, tracks where they came from, and optimizes string spaces to limit API resource consumption.
        """)
    with c2:
        st.success("""
        **2. Groq AI Processing Engine**
        The application passes the payloads to the **Llama-3.3-70b** engine on **Groq**. This provides lightning-fast inference speeds while enforcing rigid JSON schema formatting.
        """)
    with c3:
        st.warning("""
        **3. Verification Guardrails**
        The data layer verifies the text output. It runs a python search check to confirm the AI's evidence quote actually exists within the original raw input, blocking hallucinations.
        """)

    st.markdown("""
    ---

    ### ⚡ Why Groq? (Infrastructure & Technical Decisions)
    * **Ultra-Low Latency Response Profiles:** Moving from legacy providers to Groq drops processing time from 4-6 seconds down to **200-400 milliseconds**. This makes real-time data syncs viable for active software teams.
    * **Strict Operational Formatting:** By selecting Groq's structured JSON configuration mode, the platform reduces parsing dropouts to near zero.
    * **Cost Management Optimization:** Processing high-volume support lines through cost-effective hardware networks maximizes operational margins.
    """)

if __name__ == "__main__":
    render_strategy()
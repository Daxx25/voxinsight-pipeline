# app/playground.py
import streamlit as st
from core.pipeline import run_voc_pipeline

MOCK_TRANSCRIPTS = {
    "🚨 Enterprise Support Ticket (High Urgency)": {
        "channel": "Zendesk Ticket",
        "text": "Subject: SSO Login loop bug. Every single time my team clicks 'Login via Okta', the page refreshes and loops right back to the sign-in screen. This is a complete workflow blocker. We are burning cash waiting around."
    },
    "📞 Gong Sales Call Snippet (Strategic Feedback)": {
        "channel": "Gong Call",
        "text": "Client: The system is cool, but our webhooks syncing to HubSpot keep throwing silent 500 errors. It's breaking our automated pipeline. If you guys don't expose a health-check endpoint or API log dashboard, we will migrate to your competitor next quarter."
    }
}

def render_playground():
    st.title("🔬 Live Pipeline Playground")
    
    # Context Header Card for non-technical users
    st.info("""
    ### 💡 What is this page?
    This is a live sandbox of our AI processing engine. Instead of a product manager spending hours reading long support logs or listening to phone calls, this page simulates how **Groq AI** acts instantly as a researcher—extracting insights, rating frustration, and checking for text evidence automatically.
    """)
    
    # --- CONFIG SIDEBAR & INFRASTRUCTURE ACCESS ---
    st.sidebar.write("### 🔑 Infrastructure Access")
    
    # Safely look for local secrets without breaking the container execution path
    try:
        default_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        default_key = ""

    groq_key = st.sidebar.text_input(
        "Enter Groq API Key:", 
        value=default_key, 
        type="password", 
        help="Grab a free key from console.groq.com"
    )
    
    if not groq_key:
        st.sidebar.warning("⚠️ Enter a Groq API Key to test live inputs.")
        st.sidebar.markdown("[Get a Free Groq Key Here](https://console.groq.com/)")

    st.write("---")
    st.write("### 🛠️ Step 1: Choose or Write Raw Input Text")
    
    sample_choice = st.selectbox("Pick an onboarding text profile to test with:", list(MOCK_TRANSCRIPTS.keys()))
    
    user_text = st.text_area(
        "Edit the text block freely to test the system's adaptability:",
        value=MOCK_TRANSCRIPTS[sample_choice]["text"],
        height=120
    )
    
    current_channel = MOCK_TRANSCRIPTS[sample_choice]["channel"]
    st.caption(f"**Identified Ingestion Channel Type:** {current_channel}")

    if st.button("⚡ Run Groq Processing Pipeline", type="primary"):
        if not groq_key:
            st.error("Please insert your Groq API key in the left sidebar configuration panel first.")
            return
            
        with st.spinner("Processing text stream via Groq Llama-3.3..."):
            result = run_voc_pipeline(user_text, current_channel, groq_key)
            
            if result["status"] == "error":
                st.error(result["message"])
                return
                
            st.success("🎉 Processing Finished in Milliseconds!")
            
            # --- CLEAR OUTPUT STRUCTURE ---
            st.write("### 📊 Step 2: View Structured Output Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ⚙️ Extracted Product Metadata")
                st.metric("Mapped Feature Module", result["data"]["product_area"])
                
                score = result["data"]["sentiment_score"]
                sentiment_label = "🔴 Severe Pain" if score < -0.3 else "🟢 Favorable"
                st.metric("Calculated Sentiment Score", f"{score}", delta=sentiment_label, delta_color="inverse")
                
                st.markdown("**Executive Summary Brief:**")
                st.info(result["data"]["summary"])

            with col2:
                st.markdown("#### 🛡️ Trust Verification & Quotes")
                
                # Trust badge based on deterministic check
                status_type = result["data"]["quote_verification_status"]
                if status_type == "exact":
                    st.success("✅ Verbatim Quote Authenticity Verified (0% Hallucination)")
                else:
                    st.warning(f"⚠️ Quote Audit Status: {status_type}")
                    
                st.markdown(f"**Extracted Customer Quote Evidence:**")
                st.markdown(f"> *\"{result['data']['verbatim_quote']}\"*")
                
            # Clear breakdown lists
            st.write("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### ❌ Identified Customer Pain Points")
                for p in result["data"]["pain_points"]:
                    st.markdown(f"- {p}")
            with c2:
                st.markdown("#### 💡 Feature/Enhancement Requests")
                for f in result["data"]["feature_requests"]:
                    st.markdown(f"- {f}")
# app/main.py
import os
import sys
import streamlit as st

# --- INDUSTRY STANDARD PATH FIX ---
# Force Python to recognize the project root directory so 'app.' and 'core.' imports work seamlessly
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

# Force global configuration styles early inside execution stack
st.set_page_config(
    page_title="VoxInsight Pipeline Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now these absolute imports will resolve perfectly!
from app.dashboard import render_dashboard
from app.playground import render_playground
from app.strategy_page import render_strategy

def main():
    st.sidebar.write("## 🧭 VoxInsight Control Node")
    
    # Intuitive clear navigation panel selector widgets
    navigation_mode = st.sidebar.radio(
        "Navigate Application Pages:",
        ["Executive Analytics Dashboard", "Live Pipeline Playground", "Architecture & Implementation Strategy"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("🤖 Developed as a production-tier portfolio project emphasizing system engineering and product prioritization.")

    # Explicit routing block execution paths
    if navigation_mode == "Executive Analytics Dashboard":
        render_dashboard()
    elif navigation_mode == "Live Pipeline Playground":
        render_playground()
    elif navigation_mode == "Architecture & Implementation Strategy":
        render_strategy()

if __name__ == "__main__":
    main()
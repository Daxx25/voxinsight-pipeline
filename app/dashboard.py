# app/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def render_dashboard():
    st.title("📊 Executive Voice of Customer (VoC) Dashboard")
    st.subheader("Transforming customer conversations into structured product telemetry")

    # Safe data loading
    file_path = os.path.join("data", "mock_historical.csv")
    if not os.path.exists(file_path):
        st.error(f"❌ Core data tracking layer missing at `{file_path}`. Please execute `scripts/generate_mock_data.py` first.")
        return

    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df['date_only'] = df['date'].dt.date

    # --- 1. DETECT EMERGING ISSUES (System Alert Logic) ---
    # Look for sudden spikes in volume or extreme drops in sentiment in the last 35 days
    recent_window = df[df['date'] >= (df['date'].max() - pd.Timedelta(days=35))]
    alert_triggered = False
    alert_area = ""
    
    for area in df['product_area'].unique():
        area_recent = recent_window[recent_window['product_area'] == area]
        if not area_recent.empty and area_recent['sentiment_score'].mean() < -0.4:
            alert_triggered = True
            alert_area = area
            break

    if alert_triggered:
        st.error(f"🚨 **HIGH PRIORITY ALERT:** Critical sentiment drop detected within the **'{alert_area}'** cluster over the past 30 days. Review recommended.")

    # --- 2. EXECUTIVE METRICS LAYER ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Logs Processed", f"{len(df)}")
    with col2:
        avg_sent = df['sentiment_score'].mean()
        st.metric("Global Avg Sentiment", f"{avg_sent:.2f}", delta=None)
    with col3:
        top_channel = df['source_type'].value_counts().idxmax()
        st.metric("Primary Data Source", top_channel)
    with col4:
        most_impacted = df.groupby('product_area')['sentiment_score'].mean().idxmin()
        st.metric("Highest Friction Area", most_impacted.split(" & ")[0])

    st.markdown("---")

    # --- 3. PLOTLY VISUALIZATIONS ---
    st.write("### 📈 Trend Dynamics & System Telemetry")
    
    # Chart A: Cumulative volume & moving average sentiment
    daily_metrics = df.groupby(['date_only', 'product_area']).agg(
        volume=('sentiment_score', 'count'),
        avg_sentiment=('sentiment_score', 'mean')
    ).reset_index()

    fig_trends = px.line(
        daily_metrics, 
        x="date_only", 
        y="avg_sentiment", 
        color="product_area",
        title="7-Day Rolling Sentiment Trajectory per Product Module",
        labels={"date_only": "Timeline", "avg_sentiment": "Sentiment Score (-1 to +1)"},
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_trends.add_hline(y=0.0, line_dash="dash", line_color="gray", annotation_text="Neutral Line")
    st.plotly_chart(fig_trends, use_container_width=True)

    # Chart B: Matrix Portfolio Allocation
    st.write("### 🎯 Volume vs. Sentiment Matrix Grid")
    st.caption("PM Priority Matrix: Prioritize development efforts on modules falling inside the bottom-right quadrant (High Friction / High Volume).")
    
    matrix_df = df.groupby('product_area').agg(
        total_volume=('sentiment_score', 'count'),
        mean_sentiment=('sentiment_score', 'mean')
    ).reset_index()

    fig_matrix = px.scatter(
        matrix_df,
        x="total_volume",
        y="mean_sentiment",
        text="product_area",
        size="total_volume",
        labels={"total_volume": "Total Mentions / Ticket Frequency", "mean_sentiment": "Average Segment Sentiment"},
        range_y=[-1.0, 1.0]
    )
    fig_matrix.update_traces(textposition='top center')
    fig_matrix.add_hline(y=0.0, line_color="black", line_width=1)
    st.plotly_chart(fig_matrix, use_container_width=True)

    # --- 4. DATA GRANULARITY AUDIT TRAIL ---
    st.write("### 🔍 Historical Source Material Log")
    selected_area = st.selectbox("Filter Audit Trail by Product Module:", ["All"] + list(df['product_area'].unique()))
    
    filtered_df = df if selected_area == "All" else df[df['product_area'] == selected_area]
    st.dataframe(
        filtered_df[['date', 'source_type', 'product_area', 'sentiment_score', 'summary', 'verbatim_quote']].sort_values(by='date', ascending=False),
        use_container_width=True
    )

if __name__ == "__main__":
    render_dashboard()
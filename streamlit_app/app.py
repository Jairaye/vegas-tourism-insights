# streamlit_app/app.py (Enhanced)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Las Vegas Tourism Dashboard")

@st.cache_data
def load_data():
    df = pd.read_excel("data/LVCVA Data.xlsx")
    indicators = df.iloc[:, 0].str.strip()
    data = df.iloc[:, 1:]
    data.columns = pd.to_datetime(data.columns, errors='coerce')
    df_wide = pd.DataFrame(data.values.T, columns=indicators)
    df_wide['date'] = data.columns
    return df_wide.set_index("date")

# Load the data
df = load_data()

# Sidebar options
metric_list = df.columns.sort_values()
default_index = list(metric_list).index("Visitor Volume") if "Visitor Volume" in metric_list else 0
metric = st.sidebar.selectbox("Choose a metric to analyze:", metric_list, index=default_index)
show_control_chart = st.sidebar.checkbox("Show Control Limits", value=True)
show_rolling = st.sidebar.checkbox("Show 6-Month Rolling Avg", value=True)

# Metric data (force numeric conversion)
series = pd.to_numeric(df[metric], errors="coerce").dropna()
rolling_mean = series.rolling(window=6, center=True).mean()
rolling_std = series.rolling(window=6, center=True).std()
upper = rolling_mean + 2 * rolling_std
lower = rolling_mean - 2 * rolling_std

# Main line chart
st.subheader(f"📈 {metric} Over Time")
st.line_chart(series.rename("value"))


# Control Chart
if show_control_chart:
    st.subheader("🔍 Control Chart")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series.index, y=series, mode='lines+markers', name='Actual'))
    if show_rolling:
        fig.add_trace(go.Scatter(x=rolling_mean.index, y=rolling_mean, mode='lines', name='Rolling Mean'))
        fig.add_trace(go.Scatter(x=rolling_mean.index, y=upper, mode='lines', name='Upper Limit'))
        fig.add_trace(go.Scatter(x=rolling_mean.index, y=lower, mode='lines', name='Lower Limit', fill='tonexty', fillcolor='rgba(255,165,0,0.2)'))
    fig.update_layout(title=f"{metric} Control Chart", xaxis_title="Date", yaxis_title=metric, legend_title="Legend")
    st.plotly_chart(fig, use_container_width=True)

# Quick insights
st.subheader("📌 Quick Insights")
high = series.idxmax()
low = series.idxmin()
delta = series.iloc[-1] - series.iloc[-2] if len(series) > 1 else 0
trend = "⬆️" if delta > 0 else "⬇️"

st.markdown(f"- 📈 **Highest**: {high.strftime('%B %Y')} — {series.max():,.0f}")
st.markdown(f"- 📉 **Lowest**: {low.strftime('%B %Y')} — {series.min():,.0f}")
if len(series) > 1:
    st.markdown(f"- 🔄 **Last Month Change**: {series.iloc[-2]:,.0f} → {series.iloc[-1]:,.0f} ({trend} {abs(delta):,.0f})")

st.markdown("---")
st.caption("Powered by LVCVA Data")

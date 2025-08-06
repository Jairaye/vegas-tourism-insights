# streamlit_app/app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
metric = st.sidebar.selectbox("Choose a metric to analyze:", df.columns.sort_values())
show_control_chart = st.sidebar.checkbox("Show Control Limits", value=True)

# Main chart
st.subheader(f"📈 {metric} Over Time")
st.line_chart(df[metric].dropna())

# Control chart logic
if show_control_chart:
    st.subheader("🔍 Control Chart")
    series = df[metric].dropna()
    rolling_mean = series.rolling(window=6, center=True).mean()
    rolling_std = series.rolling(window=6, center=True).std()
    upper = rolling_mean + 2 * rolling_std
    lower = rolling_mean - 2 * rolling_std

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(series.index, series.values, label="Actual", marker='o')
    ax.plot(rolling_mean.index, rolling_mean.values, label="Rolling Mean", color='orange')
    ax.fill_between(series.index, lower, upper, color='orange', alpha=0.2, label="±2σ Range")
    ax.set_title(f"{metric} Control Chart")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Highlight highest/lowest month
st.subheader("📌 Insights")
high = df[metric].idxmax()
low = df[metric].idxmin()
st.markdown(f"- 📈 **Highest**: {high.strftime('%B %Y')} — {df[metric].max():,.0f}")
st.markdown(f"- 📉 **Lowest**: {low.strftime('%B %Y')} — {df[metric].min():,.0f}")

# streamlit_app/app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_excel("data/LVCVA Data.xlsx")
    indicators = df.iloc[:, 0].str.strip()
    data = df.iloc[:, 1:]
    data.columns = pd.to_datetime(data.columns, errors='coerce')
    df_wide = pd.DataFrame(data.values.T, columns=indicators)
    df_wide['date'] = data.columns
    return df_wide.set_index("date")

df = load_data()
st.title("📊 Las Vegas Tourism Dashboard")

indicator = st.selectbox("Choose Metric", df.columns)
st.line_chart(df[indicator].dropna())

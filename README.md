# Las Vegas Tourism Dashboard

A Streamlit-based web application for exploring historical tourism trends in Las Vegas using official data from the Las Vegas Convention and Visitors Authority (LVCVA).

---

## 📊 Features

* **Interactive metric selector** for all reported LVCVA indicators
* **Time series charts** with:

  * Optional 6-month rolling average
  * Optional control limits (±2σ)
* **Quick insights panel** highlighting:

  * All-time high & low months
  * Month-over-month change

---

## 📁 Project Structure

```
vegas-tourism-insights/
├── data/
│   └── LVCVA Data.xlsx          # Official LVCVA report (cleaned)
├── notebooks/
│   └── 01_clean_and_explore.ipynb  # Initial cleanup + exploration
├── streamlit_app/
│   └── app.py                  # Main Streamlit dashboard
├── requirements.txt           # App dependencies
└── README.md                  # This file
```

---

## 🔧 Setup Instructions

1. Clone this repo:

   ```bash
   git clone https://github.com/Jairaye/vegas-tourism-insights.git
   cd vegas-tourism-insights
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run locally:

   ```bash
   streamlit run streamlit_app/app.py
   ```

---

## 🌐 Streamlit Cloud Deployment

App is live at: [https://Jairaye-vegas-tourism-insights.streamlit.app](https://Jairaye-vegas-tourism-insights.streamlit.app)

No install needed — just click and explore.

---

## 🤖 Forecasting & Modeling (Coming Soon)

* Predictive model for estimating **Room Tax / LVCVA's Portion**

  * Used linear regression based on historical correlation with:

    * Visitor Volume
    * Room Nights Occupied
    * Occupancy Rate
    * Average Daily Rate (ADR)
    * Revenue per Available Room (RevPAR)
* Example predictions added manually to June 2025:

  * May 2025 Room Tax: `$32.5M`
  * June 2025 Room Tax: `$25.7M`

---

## ⚠️ Known Issues & Fixes

### Problem:

`ModuleNotFoundError` or `ValueError` when selecting metrics like:
`"Avg. Daily Auto Traffic: All Major Highways*"`

### Cause:

The `*` character in column names breaks Streamlit's internal charting.

### Fix:

Explicitly rename the series before plotting:

```python
st.line_chart(series.rename("value"))
```

This avoids issues with Altair/VegaLite.

---

## 👤 Author

**J.R. Adams**
Data analyst and developer of automation and analytics tools.
Streamlit, Python, R, and sports/poker statistics.

---

## 📜 License

This project is open source under the MIT License.

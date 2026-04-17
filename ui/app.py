import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
API_BASE_URL = "https://business-decision-intelligence-engine.onrender.com"

st.set_page_config(
    page_title="Business Intelligence Engine",
    layout="wide",
    page_icon="📊"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
    <h1 style='margin-bottom:0;'>📊 Business Intelligence Engine</h1>
    <p style='color:gray; margin-top:0;'>
    Real-time KPI monitoring • Risk detection • Decision insights
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# FETCH DATA
# -----------------------------
@st.cache_data(show_spinner=False)
def fetch_kpis():
    res = requests.get(f"{API_BASE_URL}/kpis", timeout=10)
    res.raise_for_status()
    return pd.DataFrame(res.json())

@st.cache_data(show_spinner=False)
def fetch_insights():
    res = requests.get(f"{API_BASE_URL}/insights", timeout=10)
    res.raise_for_status()
    return res.json()

# -----------------------------
# LOAD DATA
# -----------------------------
try:
    with st.spinner("Loading dashboard..."):
        kpi_df = fetch_kpis()
        insights = fetch_insights()
except Exception as e:
    st.error("Backend connection failed")
    st.code(str(e))
    st.stop()

# -----------------------------
# PREP DATA
# -----------------------------
kpi_df["date"] = pd.to_datetime(kpi_df["date"])
kpi_df = kpi_df.sort_values("date")

latest = kpi_df.iloc[-1]

# -----------------------------
# KPI CARDS (PRODUCT STYLE)
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"{latest['revenue']:,.0f}")
col2.metric("Orders", f"{latest['orders']:,.0f}")
col3.metric("Customers", f"{latest['customers']:,.0f}")

st.divider()

# -----------------------------
# CHART
# -----------------------------
st.subheader("📈 Revenue Trend")

st.line_chart(
    kpi_df.set_index("date")[["revenue"]],
    use_container_width=True
)

st.divider()

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("🔎 Filters")

risk_filter = st.sidebar.multiselect(
    "Risk Level",
    ["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM", "LOW"]
)

# -----------------------------
# INSIGHTS SECTION
# -----------------------------
st.subheader("🚨 Decision Insights")

filtered = [i for i in insights if i["risk_level"] in risk_filter]

if not filtered:
    st.info("No insights available")
else:
    for item in filtered:

        # Color coding
        if item["risk_level"] == "HIGH":
            color = "#ff4b4b"
            label = "🔴 HIGH RISK"
        elif item["risk_level"] == "MEDIUM":
            color = "#ffa500"
            label = "🟠 MEDIUM RISK"
        else:
            color = "#2ecc71"
            label = "🟢 LOW RISK"

        # Card UI
        st.markdown(
            f"""
            <div style="
                border-left:6px solid {color};
                padding:15px;
                border-radius:10px;
                margin-bottom:15px;
                background-color:#111;
            ">
                <h4>{label} — {item['date']}</h4>
                <p>{item['insight']}</p>
                <p style='color:gray; font-size:12px;'>
                    Confidence: {int(item['confidence_score']*100)}% |
                    Valid till: {item['valid_until']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Actions
        with st.expander("📌 Recommended Actions"):
            for act in item["recommended_actions"]:
                st.markdown(
                    f"- **{act['team']}** ({act['priority']}) → {act['action']}"
                )

st.divider()

# -----------------------------
# FOOTER
# -----------------------------
st.caption(
    "Built with FastAPI • Streamlit • Data Science • Decision Intelligence"
)
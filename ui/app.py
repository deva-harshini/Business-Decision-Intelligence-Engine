import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
API_BASE_URL = "https://business-decision-intelligence-engine.onrender.com"

st.set_page_config(
    page_title="Business Decision Intelligence Engine",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.title("📊 Business Decision Intelligence Engine")
st.markdown(
    """
    Executive dashboard for KPI monitoring, anomaly detection,
    forecasting, and automated business decision insights.
    """
)

st.divider()

# -----------------------------
# FETCH DATA
# -----------------------------
@st.cache_data(show_spinner=False)
def fetch_kpis():
    response = requests.get(f"{API_BASE_URL}/kpis", timeout=10)
    response.raise_for_status()
    return pd.DataFrame(response.json())


@st.cache_data(show_spinner=False)
def fetch_insights():
    response = requests.get(f"{API_BASE_URL}/insights", timeout=10)
    response.raise_for_status()
    return response.json()


# -----------------------------
# LOAD DATA
# -----------------------------
try:
    with st.spinner("Loading data..."):
        kpi_df = fetch_kpis()
        insights = fetch_insights()

except Exception as e:
    st.error("❌ Could not connect to backend")
    st.code(str(e))
    st.stop()


# -----------------------------
# KPI TREND
# -----------------------------
st.subheader("📈 KPI Trends")

kpi_df["date"] = pd.to_datetime(kpi_df["date"])
kpi_df = kpi_df.sort_values("date")

st.line_chart(
    kpi_df.set_index("date")[["revenue", "orders", "customers"]]
)

st.divider()

# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

risk_filter = st.sidebar.multiselect(
    "Select Risk Level",
    options=["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM"]
)

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("🚨 Business Decision Insights")

filtered_insights = [
    i for i in insights if i["risk_level"] in risk_filter
]

if not filtered_insights:
    st.info("No insights match selected filters.")
else:
    for item in filtered_insights:
        risk = item["risk_level"]

        if risk == "HIGH":
            st.error(f"🔴 HIGH — {item['date']}")
        elif risk == "MEDIUM":
            st.warning(f"🟠 MEDIUM — {item['date']}")
        else:
            st.success(f"🟢 LOW — {item['date']}")

        st.markdown(item["insight"])

        st.caption(
            f"Confidence: {int(item['confidence_score']*100)}% | "
            f"Valid until: {item['valid_until']}"
        )

        st.markdown("**Recommended Actions:**")

        for act in item["recommended_actions"]:
            st.markdown(
                f"- **{act['team']}** ({act['priority']}) → {act['action']}"
            )

        st.divider()


# -----------------------------
# FOOTER
# -----------------------------
st.caption(
    "Business Decision Intelligence Engine | FastAPI • Streamlit • Data Science"
)
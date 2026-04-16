import streamlit as st
import requests
import pandas as pd
import io

# -----------------------------
# CONFIG
# -----------------------------
API_BASE_URL = "https://business-decision-intelligence-engine.onrender.com"

st.set_page_config(
    page_title="Business Decision Intelligence Engine",
    layout="wide"
)

# -----------------------------
# AUTH
# -----------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == "admin123":
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.text_input("🔐 Enter Password", type="password", on_change=password_entered, key="password")
        return False

    if not st.session_state["authenticated"]:
        st.text_input("🔐 Enter Password", type="password", on_change=password_entered, key="password")
        st.error("❌ Incorrect password")
        return False

    return True


if not check_password():
    st.stop()

# -----------------------------
# HEADER
# -----------------------------
st.title("📊 Business Decision Intelligence Engine")
st.markdown("Executive dashboard for KPI monitoring, anomaly detection, forecasting, and automated business insights.")
st.divider()

# -----------------------------
# FETCH DATA
# -----------------------------
@st.cache_data
def fetch_kpis():
    res = requests.get(f"{API_BASE_URL}/kpis")
    res.raise_for_status()
    return pd.DataFrame(res.json())

@st.cache_data
def fetch_insights():
    res = requests.get(f"{API_BASE_URL}/insights")
    res.raise_for_status()
    return res.json()

try:
    kpi_df = fetch_kpis()
    insights = fetch_insights()
except:
    st.error("❌ Backend not reachable")
    st.stop()

# -----------------------------
# KPI CHART
# -----------------------------
st.subheader("📈 KPI Trends")

kpi_df["date"] = pd.to_datetime(kpi_df["date"])
kpi_df = kpi_df.sort_values("date")

st.line_chart(kpi_df.set_index("date")[["revenue", "orders", "customers"]])

st.divider()

# -----------------------------
# FILTERS
# -----------------------------
risk_filter = st.sidebar.multiselect(
    "Risk Level",
    ["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM"]
)

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("🚨 Decision Insights")

filtered = [i for i in insights if i["risk_level"] in risk_filter]

if not filtered:
    st.info("No insights available")
else:
    for item in filtered:
        if item["risk_level"] == "HIGH":
            st.error(f"{item['date']} - HIGH RISK")
        elif item["risk_level"] == "MEDIUM":
            st.warning(f"{item['date']} - MEDIUM RISK")
        else:
            st.success(f"{item['date']} - LOW RISK")

        st.write(item["insight"])

        st.caption(
            f"Confidence: {int(item['confidence_score']*100)}% | "
            f"Valid until: {item['valid_until']}"
        )

        st.markdown("**Recommended Actions:**")
        for act in item["recommended_actions"]:
            st.markdown(
                f"- **{act['team']}** ({act['priority']}) → {act['action']}  \n"
                f"_{act['expected_impact']}_"
            )

        st.divider()

# -----------------------------
# DOWNLOAD
# -----------------------------
csv = pd.DataFrame(filtered).to_csv(index=False)

st.download_button(
    "Download Insights CSV",
    csv,
    "insights.csv",
    "text/csv"
)

# -----------------------------
# FOOTER
# -----------------------------
st.caption("Built with Python • FastAPI • Streamlit")
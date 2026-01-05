import streamlit as st
import requests
import pandas as pd
import io

# -----------------------------
# CONFIGURATION
# -----------------------------
API_BASE_URL = "http://127.0.0.1:8000"  # change to Render URL after deployment

st.set_page_config(
    page_title="Business Decision Intelligence Engine",
    layout="wide"
)

# -----------------------------
# SIMPLE AUTHENTICATION
# -----------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == "admin123":
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.text_input(
            "🔐 Enter Password",
            type="password",
            on_change=password_entered,
            key="password"
        )
        return False

    if not st.session_state["authenticated"]:
        st.text_input(
            "🔐 Enter Password",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("❌ Incorrect password")
        return False

    return True


if not check_password():
    st.stop()

# -----------------------------
# HEADER
# -----------------------------
st.title("📊 Business Decision Intelligence Engine")
st.markdown(
    """
    **Executive dashboard for KPI monitoring, anomaly detection, forecasting,  
    and automated business decision insights.**
    """
)

st.divider()

# -----------------------------
# FETCH FUNCTIONS
# -----------------------------
@st.cache_data(show_spinner=False)
def fetch_insights():
    response = requests.get(f"{API_BASE_URL}/insights", timeout=5)
    response.raise_for_status()
    return response.json()["insights"]

@st.cache_data(show_spinner=False)
def fetch_kpis():
    response = requests.get(f"{API_BASE_URL}/kpis", timeout=5)
    response.raise_for_status()
    return pd.DataFrame(response.json())

# -----------------------------
# LOAD DATA
# -----------------------------
try:
    with st.spinner("Loading KPI data..."):
        kpi_df = fetch_kpis()
        insights = fetch_insights()
except requests.exceptions.RequestException as e:
    st.error("❌ Could not connect to FastAPI backend")
    st.code(str(e))
    st.stop()

# -----------------------------
# KPI TREND CHARTS
# -----------------------------
st.subheader("📈 KPI Trends")

kpi_df["date"] = pd.to_datetime(kpi_df["date"])
kpi_df = kpi_df.sort_values("date")

st.line_chart(
    kpi_df.set_index("date")[["revenue", "orders", "customers"]]
)

st.divider()

# -----------------------------
# RISK FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

risk_filter = st.sidebar.multiselect(
    "Select Risk Level",
    options=["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM"]
)

# -----------------------------
# DISPLAY INSIGHTS
# -----------------------------
st.subheader("🚨 Business Decision Insights")

filtered_insights = [
    i for i in insights if i["risk_level"] in risk_filter
]

if not filtered_insights:
    st.info("No insights match the selected filters.")
else:
    for item in filtered_insights:
        risk = item["risk_level"]
        date = item["date"]
        text = item["insight"]

        if risk == "HIGH":
            st.error(f"🔴 HIGH RISK — {date}")
        elif risk == "MEDIUM":
            st.warning(f"🟠 MEDIUM RISK — {date}")
        else:
            st.success(f"🟢 LOW RISK — {date}")

        st.markdown(text)
        st.divider()
        st.caption(
    f"Confidence: {int(item['confidence_score']*100)}% | "
    f"Valid until: {item['valid_until']}")
    st.markdown("**Recommended Actions:**")

    for act in item["recommended_actions"]:
        st.markdown(
            f"- 🏷 **{act['team']}** | **{act['priority']} Priority**  \n"
            f"_{act['action']}_  \n"
            f"*Impact:* {act['expected_impact']}"
        )

# -----------------------------
# DOWNLOAD REPORT
# -----------------------------
st.subheader("📥 Download Reports")

csv_buffer = io.StringIO()
pd.DataFrame(filtered_insights).to_csv(csv_buffer, index=False)

st.download_button(
    label="Download Decision Insights (CSV)",
    data=csv_buffer.getvalue(),
    file_name="decision_insights.csv",
    mime="text/csv"
)

# -----------------------------
# FOOTER
# -----------------------------
st.caption(
    "Business Decision Intelligence Engine | Python • FastAPI • Streamlit • Analytics"
)

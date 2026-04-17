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
st.markdown("Upload your dataset and generate KPIs & insights instantly.")

st.divider()

# -----------------------------
# FILE UPLOAD
# -----------------------------
st.subheader("📂 Upload Dataset")

st.info("""
Upload a CSV file with:
- A date column (e.g., InvoiceDate)
- Numeric columns (sales, revenue, etc.)

We automatically detect KPIs and generate insights.
""")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # -----------------------------
    # GENERATE INSIGHTS
    # -----------------------------
    if st.button("🚀 Generate Insights"):
        with st.spinner("Processing dataset..."):

            try:
                response = requests.post(
                    f"{API_BASE_URL}/upload",
                    files={"file": uploaded_file.getvalue()}
                )

                result = response.json()

                if response.status_code == 200:

                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success("Insights generated!")

                        # KPIs
                        st.subheader("📊 KPIs")
                        kpi_df = pd.DataFrame(result["kpis"])
                        st.dataframe(kpi_df)

                        if "revenue" in kpi_df.columns:
                            st.line_chart(kpi_df["revenue"])

                        # Insights
                        st.subheader("🧠 Insights")
                        for ins in result["insights"]:
                            st.markdown(f"- {ins}")

                else:
                    st.error(result)

            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()

# -----------------------------
# LIVE DASHBOARD (OPTIONAL)
# -----------------------------
st.subheader("📈 Live System Dashboard")

try:
    kpi_df = pd.DataFrame(requests.get(f"{API_BASE_URL}/kpis").json())
    insights = requests.get(f"{API_BASE_URL}/insights").json()

    if not kpi_df.empty:
        kpi_df["date"] = pd.to_datetime(kpi_df["date"])
        kpi_df = kpi_df.sort_values("date")

        st.line_chart(kpi_df.set_index("date")[["revenue"]])

    st.subheader("🚨 Insights")

    for item in insights[:5]:
        st.write(item["insight"])

except Exception as e:
    st.warning("Live backend data not available")

# -----------------------------
# FOOTER
# -----------------------------
st.caption("Built with FastAPI • Streamlit • Data Science")
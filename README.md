# 📊 Business Decision Intelligence Engine

🚀 A full-stack data science system that transforms raw business data into actionable insights, risk alerts, and decision recommendations through an automated analytics pipeline and interactive dashboard.

---

## 🔍 Overview

The **Business Decision Intelligence Engine** simulates how modern companies use data to monitor KPIs, detect anomalies, forecast trends, and generate business decisions.

This project combines:

- 📈 Data Analytics  
- 🤖 Machine Learning Logic  
- ⚙️ Backend API (FastAPI)  
- 📊 Interactive Dashboard (Streamlit)  

---

## 🎯 Problem Statement

Businesses generate large volumes of data daily but often struggle to:

- Identify performance issues in real-time  
- Detect anomalies before they impact revenue  
- Forecast future risks  
- Convert insights into actionable decisions  

This system solves that by creating a **decision intelligence pipeline** that automates the entire process.

---

## 💡 Key Features

### 📊 KPI Monitoring
- Tracks core business metrics:
  - Revenue
  - Orders
  - Customers

### 🚨 Anomaly Detection
- Uses statistical methods (Z-score) to detect abnormal KPI behavior

### 📈 Forecasting
- Predicts future trends and identifies potential risks

### 🧠 Decision Intelligence
- Converts insights into business-level recommendations
- Includes:
  - Risk classification (LOW / MEDIUM / HIGH)
  - Confidence scoring
  - Actionable next steps

### 📺 Interactive Dashboard
- Visualizes:
  - KPI trends
  - Risk insights
  - Recommended actions

---

## 🏗️ System Architecture
Raw Data → Data Cleaning → KPI Calculation → Anomaly Detection
→ Forecasting → Insight Engine → Action Engine → API → Dashboard


---

## 🧠 Tech Stack

| Category | Tools |
|--------|------|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Matplotlib, Streamlit |
| Backend | FastAPI |
| Deployment | Render, Streamlit Cloud |
| Version Control | Git, GitHub |

---

## 📂 Project Structure


Business-Decision-Intelligence-Engine/
│
├── app/ # FastAPI backend
├── ui/ # Streamlit frontend
├── src/ # Core logic (ML, insights, actions)
├── pipelines/ # End-to-end data pipeline
├── data/ # Raw + processed data
├── notebooks/ # Analysis notebooks
├── requirements.txt
└── README.md


---

## 🚀 Live Demo

**Dashboard:**  
https://business-decision-intelligence-engine.streamlit.app/

---

## ⚙️ How to Run Locally

### 1. Clone Repository
```bash
git clone https://github.com/your-username/Business-Decision-Intelligence-Engine.git
cd Business-Decision-Intelligence-Engine
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Pipeline
```bash
python pipelines/run_pipeline.py
```

### 4. Start Backend
```bash
uvicorn app.main:app --reload
```

### 5. Run Dashboard
```bash
streamlit run ui/app.py
```
---

## 📈 Key Highlights
- Built an end-to-end data system, not just a model
- Combines analytics + backend + dashboard
- Focuses on business impact, not just accuracy
- Designed for real-world decision-making

---

## 👩‍💻 Author

Mandali Deva Harshini

LinkedIn: https://linkedin.com/in/deva-harshini

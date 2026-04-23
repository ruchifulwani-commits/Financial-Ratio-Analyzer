import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Financial Ratio Analyzer", layout="wide")

# -------------------------------
# Sidebar (Advanced Inputs)
# -------------------------------
st.sidebar.title("📁 Company Details")

fy = st.sidebar.selectbox("Financial Year", ["FY 2021-22", "FY 2022-23", "FY 2023-24", "FY 2024-25"])
company = st.sidebar.text_input("Company Name")
contact = st.sidebar.text_input("Contact Number")
email = st.sidebar.text_input("Email Address")
industry = st.sidebar.selectbox("Industry Type", ["Manufacturing", "Service", "Trading", "Others"])
currency = st.sidebar.selectbox("Currency", ["INR", "USD"])

generate_report = st.sidebar.button("📄 Generate Report")
reset = st.sidebar.button("🔄 Reset Inputs")

# -------------------------------
# Title
# -------------------------------
st.title("📊 Financial Ratio Analyzer")

# -------------------------------
# Company Header
# -------------------------------
if company:
    st.markdown(f"""
    ### 🏢 {company}
    **Financial Year:** {fy} | **Industry:** {industry} | **Currency:** {currency}  
    📞 {contact} | ✉️ {email}
    """)

# -------------------------------
# Input Section
# -------------------------------
st.header("📥 Financial Inputs")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Balance Sheet")
    current_assets = st.number_input("Current Assets", min_value=0.0)
    current_liabilities = st.number_input("Current Liabilities", min_value=0.0)
    inventory = st.number_input("Inventory", min_value=0.0)
    total_debt = st.number_input("Total Debt", min_value=0.0)
    equity = st.number_input("Shareholder's Equity", min_value=0.0)

with col2:
    st.subheader("Profit & Loss")
    revenue = st.number_input("Revenue", min_value=0.0)
    cogs = st.number_input("Cost of Goods Sold", min_value=0.0)
    net_profit = st.number_input("Net Profit", min_value=0.0)

# -------------------------------
# Calculation Functions
# -------------------------------
def safe_div(a, b):
    return a / b if b != 0 else 0

def calculate_ratios():
    return {
        "Current Ratio": safe_div(current_assets, current_liabilities),
        "Quick Ratio": safe_div(current_assets - inventory, current_liabilities),
        "Net Profit Margin": safe_div(net_profit, revenue),
        "Gross Profit Margin": safe_div(revenue - cogs, revenue),
        "Debt to Equity": safe_div(total_debt, equity)
    }

# -------------------------------
# Interpretation Logic
# -------------------------------
def interpret(r):
    insights = {}
    score = 0

    # Liquidity
    if r["Current Ratio"] < 1:
        insights["Current Ratio"] = ("Liquidity risk", "red")
    else:
        insights["Current Ratio"] = ("Healthy", "green")
        score += 2

    if r["Quick Ratio"] < 1:
        insights["Quick Ratio"] = ("Low liquidity", "red")
    else:
        insights["Quick Ratio"] = ("Strong liquidity", "green")
        score += 2

    # Profitability
    if r["Net Profit Margin"] < 0.1:
        insights["Net Profit Margin"] = ("Low profitability", "red")
    else:
        insights["Net Profit Margin"] = ("Good profitability", "green")
        score += 2

    if r["Gross Profit Margin"] < 0.2:
        insights["Gross Profit Margin"] = ("Weak margin", "red")
    else:
        insights["Gross Profit Margin"] = ("Strong margin", "green")
        score += 2

    # Solvency
    if r["Debt to Equity"] > 2:
        insights["Debt to Equity"] = ("High risk leverage", "red")
    else:
        insights["Debt to Equity"] = ("Balanced", "green")
        score += 2

    return insights, score

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Ratio Summary", "📈 Charts", "📄 Interpretation"])

ratios = calculate_ratios()
insights, score = interpret(ratios)

# -------------------------------
# TAB 1: Ratio Summary
# -------------------------------
with tab1:
    st.header("📊 Ratio Summary")

    cols = st.columns(5)
    for i, (k, v) in enumerate(ratios.items()):
        label, color = insights[k]
        cols[i].metric(k, round(v, 2))
        cols[i].markdown(f"<span style='color:{color}'>{label}</span>", unsafe_allow_html=True)

# -------------------------------
# TAB 2: Charts
# -------------------------------
with tab2:
    st.header("📈 Visual Analysis")

    df = pd.DataFrame({
        "Ratio": list(ratios.keys()),
        "Value": list(ratios.values())
    })

    # Bar Chart
    fig, ax = plt.subplots()
    ax.bar(df["Ratio"], df["Value"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Pie Chart (optional)
    if revenue > 0:
        st.subheader("Profit vs Expenses")
        fig2, ax2 = plt.subplots()
        ax2.pie([net_profit, cogs], labels=["Profit", "COGS"], autopct="%1.1f%%")
        st.pyplot(fig2)

# -------------------------------
# TAB 3: Interpretation
# -------------------------------
with tab3:
    st.header("📄 Detailed Interpretation")

    for k, (text, color) in insights.items():
        st.markdown(f"**{k}:** <span style='color:{color}'>{text}</span>", unsafe_allow_html=True)

    # Score
    st.subheader("📊 Financial Health Score")
    st.write(f"Score: {score} / 10")

    if score >= 8:
        st.success("Company is financially strong")
    elif score >= 5:
        st.warning("Company is moderate risk")
    else:
        st.error("Company is high risk")

# -------------------------------
# Report Download
# -------------------------------
if generate_report:
    report = pd.DataFrame({
        "Ratio": list(ratios.keys()),
        "Value": list(ratios.values())
    })

    csv = report.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name="financial_report.csv",
        mime="text/csv"
    )

# -------------------------------
# Warnings
# -------------------------------
if current_liabilities == 0 or revenue == 0 or equity == 0:
    st.warning("⚠️ Some inputs are zero. Ratios may be inaccurate.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
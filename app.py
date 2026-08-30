import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from health_engine import run_sir_model_advanced, fetch_disease_preset
from finance_engine import run_monte_carlo_live
from optimization_engine import optimize_resources
from map_engine import generate_resource_map
from streamlit_folium import st_folium

st.set_page_config(page_title="BioEcon Risk Platform", layout="wide")

st.title("BioEcon Risk & Resource Allocation Platform")
st.markdown("A quantitative platform combining computational epidemiology, live financial market data, and linear optimization.")

# Sidebar Controls
st.sidebar.header("Global Configuration")

# Module 1 Sidebar Setup
st.sidebar.subheader("Module 1: Disease Profile")
disease_choice = st.sidebar.selectbox("Select Disease Preset", [
                                      "COVID-19 (Original)", "Seasonal Influenza", "Measles", "Custom Scenario"])
preset = fetch_disease_preset(disease_choice)

population = st.sidebar.number_input(
    "Target Population", value=100000, step=10000)
if disease_choice == "Custom Scenario":
    beta = st.sidebar.slider("Transmission Rate (Beta)",
                             0.05, 1.50, preset["beta"])
    gamma = st.sidebar.slider("Recovery Rate (Gamma)",
                              0.01, 0.50, preset["gamma"])
else:
    beta = preset["beta"]
    gamma = preset["gamma"]
    st.sidebar.info(
        f"**Est. R0:** {preset['r0']} | **Beta:** {beta} | **Gamma:** {gamma}")

days = st.sidebar.slider("Simulation Horizon (Days)", 30, 365, 120)

# Module 2 Sidebar Setup
st.sidebar.subheader("Module 2: Live Market Portfolio")
ticker_input = st.sidebar.text_input(
    "Market Ticker (e.g., XLV, SPY, JNJ)", value="XLV")
num_shares = st.sidebar.number_input(
    "Portfolio Shares Owned", value=2000, step=100)

# Layout Columns
col1, col2, col3 = st.columns(3)

# Module 1 Execution
with col1:
    st.subheader(f"Outbreak Dynamics: {disease_choice}")
    t, y = run_sir_model_advanced(
        beta=beta, gamma=gamma, population=population, days=days)
    peak_infected_count = int(max(y[1]))

    fig1, ax1 = plt.subplots()
    ax1.plot(t, y[0], label='Susceptible', color='blue')
    ax1.plot(t, y[1], label='Infected', color='red')
    ax1.plot(t, y[2], label='Recovered', color='green')
    ax1.set_xlabel('Days')
    ax1.set_ylabel('People')
    ax1.legend()
    st.pyplot(fig1)
    st.metric(label="Projected Peak Infections",
              value=f"{peak_infected_count:,} people")

# Module 2 Execution
with col2:
    st.subheader(f"Market Portfolio Risk ({ticker_input})")
    paths, metrics = run_monte_carlo_live(ticker_symbol=ticker_input)

    if paths is not None:
        portfolio_value = metrics['current_price'] * num_shares
        st.write(
            f"**Share Price:** ${metrics['current_price']} | **Portfolio:** ${portfolio_value:,.2f}")
        st.write(
            f"**Hist. Return:** {metrics['annual_return']}% | **Volatility:** {metrics['volatility']}%")

        fig2, ax2 = plt.subplots()
        ax2.plot(paths * num_shares)
        ax2.set_xlabel('Trading Days (5 Years)')
        ax2.set_ylabel('Total Portfolio Value ($)')
        st.pyplot(fig2)
    else:
        st.error("Error fetching market data.")
        portfolio_value = 100000  # Fallback budget

# Module 3 Execution (Connected to Live Inputs)
with col3:
    st.subheader("Automated Resource Allocation")

    # Use live portfolio value as budget, and peak infection fraction to optimize
    peak_fraction = peak_infected_count / population
    result = optimize_resources(
        total_budget=portfolio_value, peak_infected=peak_fraction)

    if result["success"]:
        st.success(f"Optimal Allocation Calculated!")
        st.metric(label="Projected Lives Saved",
                  value=f"{result['lives_saved']:,}")
        st.metric(label="Total Capital Deployed",
                  value=f"${result['total_spent']:,.2f}")

        st.markdown("**Recommended Spending Plan:**")
        st.write(f"• **Vaccines:** {result['vaccines']:,} doses")
        st.write(f"• **ICU Beds:** {result['icu_beds']:,} units")
        st.write(f"• **Antiviral Treatments:** {result['treatments']:,} doses")
    else:
        st.error("Budget insufficient to satisfy minimum medical constraints.")
# Full-width Map Section at the bottom of the dashboard
st.divider()
st.subheader("Geospatial Resource Distribution Map")
st.caption("Visualizing real-time regional deployment of optimized medical assets based on local facility capacity.")
# Insert after Module 3 allocation results in app.py:

if result["success"]:
    st.subheader("Export Optimization Report")

    # Create structured data dictionary
    report_data = {
        "Facility": [
            "Lakeridge Health Oshawa",
            "Lakeridge Health Ajax Pickering",
            "Lakeridge Health Whitby",
            "Lakeridge Health Bowmanville"
        ],
        "Capacity Share": ["45%", "25%", "15%", "15%"],
        "Vaccine Doses": [
            int(result["vaccines"] * 0.45),
            int(result["vaccines"] * 0.25),
            int(result["vaccines"] * 0.15),
            int(result["vaccines"] * 0.15)
        ],
        "ICU Beds Allocated": [
            int(result["icu_beds"] * 0.45),
            int(result["icu_beds"] * 0.25),
            int(result["icu_beds"] * 0.15),
            int(result["icu_beds"] * 0.15)
        ],
        "Treatments Allocated": [
            int(result["treatments"] * 0.45),
            int(result["treatments"] * 0.25),
            int(result["treatments"] * 0.15),
            int(result["treatments"] * 0.15)
        ]
    }

    report_df = pd.DataFrame(report_data)

    # Display table in dashboard
    st.dataframe(report_df, width="stretch")

    # Generate CSV download button
    csv_bytes = report_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Allocation Plan (CSV)",
        data=csv_bytes,
        file_name="bioecon_resource_allocation_plan.csv",
        mime="text/csv"
    )
if result["success"]:
    m = generate_resource_map(
        vaccines=result["vaccines"],
        beds=result["icu_beds"],
        treatments=result["treatments"]
    )
    st_folium(m, width=1300, height=450)

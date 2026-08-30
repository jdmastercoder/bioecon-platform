import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from health_engine import run_epidemic_simulation
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
# =====================================================================
# MODULE 1: SIDEBAR INPUTS (Add incubation and hospitalization sliders)
# =====================================================================
# In your Sidebar:
# --- SIDEBAR INPUTS ---
disease_choice = st.sidebar.selectbox(
    "Select Pathogen", ["COVID-19", "Influenza", "Custom"])
population = st.sidebar.number_input(
    "Total Population", value=500000, step=10000)
initial_cases = st.sidebar.number_input("Initial Cases", value=10, step=1)
transmission_rate = st.sidebar.slider(
    "Transmission Rate (Beta)", 0.0, 1.0, 0.35, 0.01)
incubation_days = st.sidebar.slider("Incubation Period (Days)", 1, 14, 5, 1)
recovery_days = st.sidebar.slider("Recovery Period (Days)", 1, 30, 14, 1)
hospitalization_rate = st.sidebar.slider(
    "Hospitalization Rate (%)", 0.0, 20.0, 5.0, 0.5) / 100.0
days = 90

# In Module 1 Execution:
# --- MODULE 1 EXECUTION ---
# Create columns first so col1 exists
col1, col2, col3 = st.columns(3)

# Module 1 Execution
with col1:
    st.subheader(f"Outbreak Dynamics: {disease_choice}")

    sim_results = run_epidemic_simulation(
        population=population,
        initial_cases=initial_cases,
        transmission_rate=transmission_rate,
        incubation_days=incubation_days,
        recovery_days=recovery_days,
        hospitalization_rate=hospitalization_rate,
        days=days
    )

    peak_infected_count = int(np.max(sim_results['infected']))

    fig1, ax1 = plt.subplots()
    ax1.plot(sim_results['days'], sim_results['susceptible'],
             label='Susceptible', color='blue')
    ax1.plot(sim_results['days'], sim_results['exposed'],
             label='Exposed', color='orange')
    ax1.plot(sim_results['days'], sim_results['infected'],
             label='Infected', color='red')
    ax1.plot(sim_results['days'], sim_results['hospitalized'],
             label='Hospitalized', color='purple')
    ax1.plot(sim_results['days'], sim_results['recovered'],
             label='Recovered', color='green')
    ax1.set_xlabel('Days')
    ax1.set_ylabel('People')
    ax1.legend()
    st.pyplot(fig1)

# Module 2 Sidebar Setup
st.sidebar.subheader("Module 2: Live Market Portfolio")
ticker_input = st.sidebar.text_input(
    "Market Ticker (e.g., XLV, SPY, JNJ)", value="XLV")
num_shares = st.sidebar.number_input(
    "Portfolio Shares Owned", value=2000, step=100)

# Layout Columns
col1, col2, col3 = st.columns(3)

# Module 1 Execution
# Module 1 Execution
with col1:
    st.subheader(f"Outbreak Dynamics: {disease_choice}")

    sim_results = run_epidemic_simulation(
        population=population,
        initial_cases=initial_cases,
        transmission_rate=transmission_rate,
        incubation_days=incubation_days,
        recovery_days=recovery_days,
        hospitalization_rate=hospitalization_rate,
        days=days
    )

    peak_infected_count = int(np.max(sim_results['infected']))

    fig1, ax1 = plt.subplots()
    ax1.plot(sim_results['days'], sim_results['susceptible'],
             label='Susceptible', color='blue')
    ax1.plot(sim_results['days'], sim_results['exposed'],
             label='Exposed', color='orange')
    ax1.plot(sim_results['days'], sim_results['infected'],
             label='Infected', color='red')
    ax1.plot(sim_results['days'], sim_results['hospitalized'],
             label='Hospitalized', color='purple')
    ax1.plot(sim_results['days'], sim_results['recovered'],
             label='Recovered', color='green')
    ax1.set_xlabel('Days')
    ax1.set_ylabel('People')
    ax1.legend()
    st.pyplot(fig1)

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

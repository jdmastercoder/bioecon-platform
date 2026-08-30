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

st.set_page_config(
    page_title="BioEcon Platform",
    page_icon="🏥",
    layout="wide"
)

st.title("BioEcon Risk & Resource Allocation Platform")
st.markdown("Integrated epidemiological modeling, financial risk estimation, and geospatial resource distribution.")

# ---------------------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------------------
st.sidebar.header("Epidemic Parameters (SEIR-H)")
population = st.sidebar.number_input(
    "Total Population", value=500000, step=10000, key="main_population")
initial_cases = st.sidebar.number_input(
    "Initial Cases", value=10, step=1, key="main_initial_cases")
transmission_rate = st.sidebar.slider(
    "Transmission Rate (Beta)", 0.0, 1.0, 0.35, 0.01, key="main_beta")
incubation_days = st.sidebar.slider(
    "Incubation Period (Days)", 1, 14, 5, 1, key="main_incubation")
recovery_days = st.sidebar.slider(
    "Recovery Period (Days)", 1, 30, 14, 1, key="main_recovery")
hospitalization_rate = st.sidebar.slider(
    "Hospitalization Rate (%)", 0.0, 20.0, 5.0, 0.5, key="main_hosp_rate") / 100.0

st.sidebar.header("Resource Constraints")
total_vaccines = st.sidebar.number_input(
    "Available Vaccines", value=100000, step=5000, key="main_vaccines")
total_beds = st.sidebar.number_input(
    "Available ICU Beds", value=500, step=50, key="main_beds")
total_treatments = st.sidebar.number_input(
    "Available Treatments", value=25000, step=1000, key="main_treatments")

# Create Navigation Tabs
tab1, tab2 = st.tabs(["📊 Main Allocation Dashboard",
                     "🧪 Stress Testing & Sensitivity"])

# ---------------------------------------------------------------------
# TAB 1: MAIN DASHBOARD
# ---------------------------------------------------------------------
with tab1:
    st.header("1. Epidemiological Dynamic Projections")

    sim_results = run_epidemic_simulation(
        population=population,
        initial_cases=initial_cases,
        transmission_rate=transmission_rate,
        incubation_days=incubation_days,
        recovery_days=recovery_days,
        hospitalization_rate=hospitalization_rate,
        days=90
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Active Cases",
                f"{int(np.max(sim_results['infected'])):,}")
    col2.metric("Peak Hospitalizations (ICU)",
                f"{sim_results['peak_hospitalizations']:,}")
    col3.metric("Peak Strain Day", f"Day {sim_results['peak_day']}")

    chart_df = pd.DataFrame({
        "Day": sim_results["days"],
        "Susceptible": sim_results["susceptible"],
        "Exposed": sim_results["exposed"],
        "Infected": sim_results["infected"],
        "Hospitalized": sim_results["hospitalized"],
        "Recovered": sim_results["recovered"]
    }).set_index("Day")

    st.line_chart(chart_df, width="stretch")

    st.header("2. Optimized Resource Allocation Plan")

    report_data = {
        "Facility": [
            "Lakeridge Health Oshawa",
            "Lakeridge Health Ajax Pickering",
            "Lakeridge Health Whitby",
            "Lakeridge Health Bowmanville"
        ],
        "Capacity Share": ["45%", "25%", "15%", "15%"],
        "Vaccine Doses": [int(total_vaccines * 0.45), int(total_vaccines * 0.25), int(total_vaccines * 0.15), int(total_vaccines * 0.15)],
        "ICU Beds Allocated": [int(total_beds * 0.45), int(total_beds * 0.25), int(total_beds * 0.15), int(total_beds * 0.15)],
        "Treatments Allocated": [int(total_treatments * 0.45), int(total_treatments * 0.25), int(total_treatments * 0.15), int(total_treatments * 0.15)]
    }

    report_df = pd.DataFrame(report_data)
    st.dataframe(report_df, width="stretch")

    csv_bytes = report_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Allocation Plan (CSV)",
        data=csv_bytes,
        file_name="bioecon_resource_allocation_plan.csv",
        mime="text/csv"
    )

    st.header("3. Regional Asset Deployment Map")
    map_obj = generate_resource_map(
        vaccines=total_vaccines,
        beds=total_beds,
        treatments=total_treatments,
        peak_hospitalized=sim_results['peak_hospitalizations']
    )
    st_folium(map_obj, width=1100, height=500)

# ---------------------------------------------------------------------
# TAB 2: STRESS TESTING & SENSITIVITY ANALYSIS
# ---------------------------------------------------------------------
with tab2:
    st.header("Scenario Sensitivity Analysis")
    st.markdown(
        "Evaluate hospital capacity deficits under worst-case and best-case epidemiological surges.")

    beta_multiplier = st.slider(
        "Transmission Surge Multiplier", 0.5, 2.0, 1.2, 0.1)

    # Run Baseline vs Surge Simulation
    sim_baseline = sim_results
    sim_surge = run_epidemic_simulation(
        population=population,
        initial_cases=initial_cases,
        transmission_rate=min(1.0, transmission_rate * beta_multiplier),
        incubation_days=incubation_days,
        recovery_days=recovery_days,
        hospitalization_rate=hospitalization_rate,
        days=90
    )

    scen_col1, scen_col2 = st.columns(2)
    scen_col1.metric("Baseline Peak ICU Demand",
                     f"{sim_baseline['peak_hospitalizations']:,}")
    scen_col2.metric(
        "Surge Scenario Peak ICU Demand",
        f"{sim_surge['peak_hospitalizations']:,}",
        delta=f"{sim_surge['peak_hospitalizations'] - sim_baseline['peak_hospitalizations']:,} patients",
        delta_color="inverse"
    )

    comparison_df = pd.DataFrame({
        "Day": sim_baseline["days"],
        "Baseline Hospitalizations": sim_baseline["hospitalized"],
        "Surge Scenario Hospitalizations": sim_surge["hospitalized"]
    }).set_index("Day")

    st.line_chart(comparison_df, width="stretch")

    icu_deficit = sim_surge['peak_hospitalizations'] - total_beds
    if icu_deficit > 0:
        st.error(
            f"⚠️ **Capacity Deficit Warning:** The surge scenario exceeds total available regional beds by **{icu_deficit:,} beds**!")
    else:
        st.success(
            f"✅ **Capacity Buffer:** Regional bed capacity holds a surplus buffer of **{abs(icu_deficit):,} beds** under this scenario.")
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
        key="main_dowload_btn"
    )
if result["success"]:
    m = generate_resource_map(
        vaccines=result["vaccines"],
        beds=result["icu_beds"],
        treatments=result["treatments"]
    )
    st_folium(m, width=1300, height=450)

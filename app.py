import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from health_engine import run_epidemic_simulation
from stochastic_health_engine import run_stochastic_seir_h
from finance_engine import run_monte_carlo_live
from optimization_engine import optimize_resources, optimize_resources_milp
from map_engine import generate_resource_map
from report_engine import generate_pdf_report
from streamlit_folium import st_folium

# ---------------------------------------------------------------------
# PAGE CONFIGURATION (Must be at the very top)
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="BioEcon Platform",
    page_icon="🏥",
    layout="wide"
)

st.title("BioEcon Risk & Resource Allocation Platform")
st.markdown("Integrated epidemiological modeling, financial risk estimation, and geospatial resource distribution.")

# ---------------------------------------------------------------------
# SIDEBAR CONTROLS (Unified Pathogen Presets & Settings)
# ---------------------------------------------------------------------
st.sidebar.header("Epidemic Parameters (SEIR-H)")

disease_choice = st.sidebar.selectbox(
    "Select Pathogen Preset",
    ["COVID-19 (Omicron)", "Seasonal Influenza", "Measles", "Custom"],
    key="main_pathogen_preset"
)

# Pathogen Presets Dynamic Baselines
if disease_choice == "COVID-19 (Omicron)":
    default_beta, default_inc, default_rec, default_hosp = 0.65, 3, 7, 3.0
elif disease_choice == "Seasonal Influenza":
    default_beta, default_inc, default_rec, default_hosp = 0.35, 2, 5, 1.5
elif disease_choice == "Measles":
    default_beta, default_inc, default_rec, default_hosp = 0.90, 10, 14, 10.0
else:
    default_beta, default_inc, default_rec, default_hosp = 0.35, 5, 14, 5.0

population = st.sidebar.number_input(
    "Total Population", value=500000, step=10000, key="main_population")
initial_cases = st.sidebar.number_input(
    "Initial Cases", value=10, step=1, key="main_initial_cases")

transmission_rate = st.sidebar.slider(
    "Transmission Rate (Beta)", 0.0, 1.0, default_beta, 0.01,
    key="main_beta",
    help="Represents the average number of adequate contacts per unit time that lead to transmission."
)

incubation_days = st.sidebar.slider(
    "Incubation Period (Days)", 1, 14, default_inc, 1, key="main_incubation")
recovery_days = st.sidebar.slider(
    "Recovery Period (Days)", 1, 30, default_rec, 1, key="main_recovery")
hospitalization_rate = st.sidebar.slider(
    "Hospitalization Rate (%)", 0.0, 20.0, default_hosp, 0.5, key="main_hosp_rate") / 100.0
days = 90

st.sidebar.header("Market Risk Inputs")
ticker_input = st.sidebar.text_input(
    "Market Ticker (e.g., XLV, SPY, JNJ)", value="XLV", key="main_ticker")
num_shares = st.sidebar.number_input(
    "Portfolio Shares Owned", value=2000, step=100, key="main_shares")

st.sidebar.header("Resource Constraints")
total_vaccines = st.sidebar.number_input(
    "Available Vaccines", value=100000, step=5000, key="main_vaccines")
total_beds = st.sidebar.number_input(
    "Available ICU Beds", value=500, step=50, key="main_beds")
total_treatments = st.sidebar.number_input(
    "Available Treatments", value=25000, step=1000, key="main_treatments")

# ---------------------------------------------------------------------
# TABS NAVIGATION
# ---------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Main Allocation Dashboard",
    "🧪 Stress Testing & Sensitivity",
    "🔬 Advanced SDE & MILP Engine"
])

# =====================================================================
# TAB 1: MAIN DASHBOARD
# =====================================================================
with tab1:
    col1, col2, col3 = st.columns(3)

    # Module 1: Outbreak Dynamics
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

    # Module 2: Market Portfolio Risk
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
            portfolio_value = 100000

    # Module 3: Resource Allocation Solver
    with col3:
        st.subheader("Automated Resource Allocation")

        peak_fraction = peak_infected_count / population
        result = optimize_resources(
            total_budget=portfolio_value, peak_infected=peak_fraction)

        if result["success"]:
            st.success("Optimal Allocation Calculated!")
            st.metric(label="Projected Lives Saved",
                      value=f"{result['lives_saved']:,}")
            st.metric(label="Total Capital Deployed",
                      value=f"${result['total_spent']:,.2f}")

            st.markdown("**Recommended Spending Plan:**")
            st.write(f"• **Vaccines:** {result['vaccines']:,} doses")
            st.write(f"• **ICU Beds:** {result['icu_beds']:,} units")
            st.write(
                f"• **Antiviral Treatments:** {result['treatments']:,} doses")
        else:
            st.error("Budget insufficient to satisfy minimum medical constraints.")

    st.divider()

    # SECTION 2: UNIFIED ALLOCATION REPORT
    st.header("2. Optimized Resource Allocation Plan")

    if result["success"]:
        alloc_v = result["vaccines"]
        alloc_b = result["icu_beds"]
        alloc_t = result["treatments"]
    else:
        alloc_v = total_vaccines
        alloc_b = total_beds
        alloc_t = total_treatments

    report_data = {
        "Facility": [
            "Lakeridge Health Oshawa",
            "Lakeridge Health Ajax Pickering",
            "Lakeridge Health Whitby",
            "Lakeridge Health Bowmanville"
        ],
        "Capacity Share": ["45%", "25%", "15%", "15%"],
        "Vaccine Doses": [int(alloc_v * 0.45), int(alloc_v * 0.25), int(alloc_v * 0.15), int(alloc_v * 0.15)],
        "ICU Beds Allocated": [int(alloc_b * 0.45), int(alloc_b * 0.25), int(alloc_b * 0.15), int(alloc_b * 0.15)],
        "Treatments Allocated": [int(alloc_t * 0.45), int(alloc_t * 0.25), int(alloc_t * 0.15), int(alloc_t * 0.15)]
    }

    report_df = pd.DataFrame(report_data)
    st.dataframe(report_df, width="stretch")

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        csv_bytes = report_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Allocation Plan (CSV)",
            data=csv_bytes,
            file_name="bioecon_resource_allocation_plan.csv",
            mime="text/csv",
            key="main_tab_download_csv"
        )

    with exp_col2:
        pdf_bytes = generate_pdf_report(
            disease_choice, sim_results, alloc_v, alloc_b, alloc_t)
        st.download_button(
            label="📄 Download Executive Brief (PDF)",
            data=pdf_bytes,
            file_name="bioecon_executive_summary.pdf",
            mime="application/pdf",
            key="main_tab_download_pdf"
        )

    st.divider()

    # SECTION 3: GEOSPATIAL MAP VISUALIZATION
    st.header("3. Regional Asset Deployment Map")
    st.caption(
        "Visualizing real-time regional deployment of optimized medical assets based on local facility capacity.")

    map_obj = generate_resource_map(
        vaccines=alloc_v,
        beds=alloc_b,
        treatments=alloc_t,
        peak_hospitalized=sim_results['peak_hospitalizations']
    )
    st_folium(map_obj, width="stretch", height=500)

# =====================================================================
# TAB 2: STRESS TESTING & SENSITIVITY ANALYSIS
# =====================================================================
with tab2:
    st.header("Scenario Sensitivity Analysis")
    st.markdown(
        "Evaluate hospital capacity deficits under worst-case and best-case epidemiological surges.")

    beta_multiplier = st.slider(
        "Transmission Surge Multiplier", 0.5, 2.0, 1.2, 0.1, key="tab2_beta_mult")

    sim_baseline = sim_results
    sim_surge = run_epidemic_simulation(
        population=population,
        initial_cases=initial_cases,
        transmission_rate=min(1.0, transmission_rate * beta_multiplier),
        incubation_days=incubation_days,
        recovery_days=recovery_days,
        hospitalization_rate=hospitalization_rate,
        days=days
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

# =====================================================================
# TAB 3: ADVANCED STOCHASTIC & MILP MODELING
# =====================================================================
with tab3:
    st.header("Stochastic Differential Equations & MILP Integer Optimization")
    st.markdown(
        "This research module runs **Euler-Maruyama SDE integration** over multiple Monte Carlo paths "
        "to calculate 95% confidence bounds on infection trajectories, paired with a **Mixed-Integer Linear Program (MILP)**."
    )

    sde_col1, sde_col2 = st.columns(2)
    with sde_col1:
        num_runs = st.slider("Monte Carlo Stochastic Runs",
                             10, 100, 30, 5, key="tab3_sde_runs")
    with sde_col2:
        noise_level = st.slider(
            "Wiener Process Noise Intensity (σ)", 0.0, 0.1, 0.02, 0.005, key="tab3_noise")

    stoch_res = run_stochastic_seir_h(
        population=population,
        initial_cases=initial_cases,
        transmission_rate=transmission_rate,
        incubation_days=incubation_days,
        recovery_days=recovery_days,
        hospitalization_rate=hospitalization_rate,
        days=days,
        noise_intensity=noise_level,
        runs=num_runs
    )

    fig_sde, ax_sde = plt.subplots(figsize=(10, 4))
    ax_sde.plot(stoch_res["time"], stoch_res["infected_mean"],
                color="red", label="Mean Active Infections")
    ax_sde.fill_between(
        stoch_res["time"],
        stoch_res["infected_lower"],
        stoch_res["infected_upper"],
        color="red",
        alpha=0.2,
        label="95% Confidence Interval (SDE Noise)"
    )
    ax_sde.set_xlabel("Days")
    ax_sde.set_ylabel("Infected Population")
    ax_sde.set_title("Stochastic Infection Trajectory (Euler-Maruyama SDE)")
    ax_sde.legend()
    st.pyplot(fig_sde)

    st.divider()

    st.subheader("Mixed-Integer Linear Programming (MILP) Asset Solver")
    milp_res = optimize_resources_milp(
        total_budget=portfolio_value, peak_infected=transmission_rate)

    if milp_res["success"]:
        milp_c1, milp_c2, milp_c3, milp_c4 = st.columns(4)
        milp_c1.metric("Optimal Vaccines (Integer)",
                       f"{milp_res['vaccines']:,} doses")
        milp_c2.metric("Optimal ICU Beds (Integer)",
                       f"{milp_res['icu_beds']:,} units")
        milp_c3.metric("Optimal Antivirals (Integer)",
                       f"{milp_res['treatments']:,} doses")
        milp_c4.metric("MILP Projected Lives Saved",
                       f"{milp_res['lives_saved']:,}")
    else:
        st.error("MILP optimization failed to converge within constraints.")

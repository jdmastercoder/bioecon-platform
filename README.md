Markdown

# BioEcon Risk & Resource Allocation Platform

An open-source quantitative decision-support engine combining computational epidemiology, live financial market risk modeling, and linear optimization to solve complex medical supply chain allocation problems.

---

## Overview

Public health agencies and non-profit healthcare organizations frequently face dual challenges during disease outbreaks: modeling rapid epidemiological spread while managing volatile funding sources and constrained operational budgets.

The **BioEcon Platform** bridges quantitative finance and computational biology into a single web-based analytical engine. By combining system differential equations, live market data feeds, and linear programming, the system enables decision-makers to evaluate financial risk and optimize supply distribution dynamically.

---

## System Architecture & Features

┌─────────────────────────────────────────────────────────────────────────┐
│ BioEcon Dashboard │
└────────────────────────────────────┬────────────────────────────────────┘
│
┌───────────────────────────┼───────────────────────────┐
▼ ▼ ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Module 1: Health│ │Module 2: Finance│ │ Module 3: Math │
│ Differential │ │ Monte Carlo │ │ Optimization │
│ Equations │ │ Simulations │ │ (Linear Prog.) │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
│ │ │
└───────────────────────────┼──────────────────────────┘
▼
┌─────────────────────────┐
│ Interactive Spatial Map │
│ (Geospatial Folium) │
└─────────────────────────┘

### Key Modules

1. **Module 1: Computational Epidemiology Engine (`health_engine.py`)**
   - Solves non-linear Systems of Ordinary Differential Equations (SIR Models) using `scipy.integrate.solve_ivp`.
   - Simulates susceptible, infected, and recovered trajectory populations across dynamic time horizons.
   - Includes parameter presets for real-world pathogens (COVID-19, Seasonal Influenza, Measles).

2. **Module 2: Financial Risk & Portfolio Simulation Engine (`finance_engine.py`)**
   - Connects to Yahoo Finance (`yfinance`) to fetch historical price feeds for real market tickers (e.g., ETFs, equities, health sector indices).
   - Calculates annualized returns and asset volatility to run Monte Carlo simulations (Geometric Brownian Motion paths).
   - Models portfolio uncertainty and establishes real-time operational budget limits.

3. **Module 3: Resource Optimization Engine (`optimization_engine.py`)**
   - Uses Linear Programming (`scipy.optimize.linprog` with the Highs interior-point solver) to compute the mathematically ideal allocation of medical assets (vaccines, ICU beds, antiviral treatments).
   - Maximizes total impact (projected lives saved) subject to strict live portfolio budget constraints and facility capacity bounds.

4. **Geospatial Mapping & Analytics UI (`map_engine.py` & `app.py`)**
   - Interactive dashboard rendered via Streamlit.
   - Generates real-time geospatial maps (`folium` / `streamlit-folium`) displaying facility nodes, regional risk indicators, and asset distribution plans.

---

## Tech Stack & Dependencies

- **Language:** Python 3.10+
- **Frontend / Dashboard Framework:** Streamlit
- **Math & Data Libraries:** NumPy, SciPy, Pandas
- **Financial Data Feed:** `yfinance`
- **Plotting & Mapping:** Matplotlib, Folium, `streamlit-folium`

---

## Installation & Running Locally

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/jdmastercoder/bioecon-platform.git](https://github.com/jdmastercoder/bioecon-platform.git)
   cd bioecon-platform
   ```

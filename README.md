# BioEcon Risk & Resource Allocation Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bioecon-platform-8cfuamypfxjgndkhkhybzc.streamlit.app/)

🔗 **Live Interactive App:** [bioecon-platform.streamlit.app](https://bioecon-platform-8cfuamypfxjgndkhkhybzc.streamlit.app/)

An open-source quantitative decision-support engine combining computational epidemiology, live financial market risk modeling, and linear optimization to solve complex medical supply chain allocation problems.

---

## Overview

Public health agencies and healthcare organizations frequently face dual challenges during disease outbreaks: modeling rapid epidemiological spread while managing volatile funding sources and constrained operational budgets.

The **BioEcon Platform** bridges quantitative finance and computational biology into a single web-based analytical engine. By combining system differential equations, live market data feeds, and linear programming, the system enables decision-makers to evaluate financial risk and optimize supply distribution dynamically.

---

## System Architecture

┌─────────────────────────────────────────────────────────────────────────┐
│                           BioEcon Dashboard                             │
└────────────────────────────────────┬────────────────────────────────────┘
│
┌───────────────────────────┼───────────────────────────┐
▼                           ▼                           ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│ Module 1: Health│         │Module 2: Finance│         │ Module 3: Math  │
│  SEIR-H System  │         │   Monte Carlo   │         │  Optimization   │
│   (SciPy ODE)   │         │ (yfinance/GBM)  │         │  (SciPy LinProg)│
└────────┬────────┘         └────────┬────────┘         └────────┬────────┘
│                           │                           │
└───────────────────────────┼───────────────────────────┘
▼
┌─────────────────────────┐
│ Interactive Spatial Map │
│   (Geospatial Folium)   │
└─────────────────────────┘


---

## Key Modules

### Module 1: Computational Epidemiology Engine (`health_engine.py`)
* Solves non-linear Systems of Ordinary Differential Equations using `scipy.integrate.odeint`.
* Simulates Susceptible, Exposed, Infected, Hospitalized, and Recovered (SEIR-H) population dynamics across dynamic time horizons.
* Includes dynamic parameter controls for incubation periods, recovery windows, and ICU admission probabilities.

### Module 2: Financial Risk & Portfolio Simulation Engine (`finance_engine.py`)
* Connects to Yahoo Finance (`yfinance`) to fetch live market feeds for equities, healthcare sector indices (`XLV`), and ETFs.
* Calculates annualized returns and asset volatility to run stochastic Monte Carlo simulations (Geometric Brownian Motion).
* Models portfolio uncertainty and establishes real-time operational budget limits for emergency deployment.

### Module 3: Resource Optimization Engine (`optimization_engine.py`)
* Employs Linear Programming (`scipy.optimize.linprog`) to compute optimal distribution vectors for medical assets (vaccines, ICU beds, antiviral treatments).
* Maximizes projected lives saved subject to operational budget limits and hospital capacity constraints.

### Module 4: Geospatial Analytics UI (`map_engine.py` & `app.py`)
* Interactive multi-tab dashboard rendered via Streamlit.
* Generates real-time geospatial maps (`folium` / `streamlit-folium`) displaying facility nodes, hospital strain risk halos, and resource deployment plans.

---

## Tech Stack & Dependencies

* **Language:** Python 3.10+
* **Dashboard Framework:** Streamlit
* **Math & Optimization:** NumPy, SciPy, Pandas
* **Financial Data Engine:** `yfinance`
* **Plotting & Geospatial:** Matplotlib, Folium, `streamlit-folium`

---

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/jdmastercoder/bioecon-platform.git](https://github.com/jdmastercoder/bioecon-platform.git)
   cd bioecon-platform
Install Dependencies:

Bash
pip install -r requirements.txt
Run Application:

Bash
python -m streamlit run app.py

### Commit to GitHub

To push this refined version to your repository, run:

```bash
git add README.md
git commit -m "Updated README with system architecture diagram and module specs"
git push

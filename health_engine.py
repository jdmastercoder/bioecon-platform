import numpy as np
from scipy.integrate import solve_ivp
import requests
import pandas as pd


def fetch_disease_preset(preset_name):
    """
    Returns real baseline epidemiology parameters for known diseases.
    """
    presets = {
        "COVID-19 (Original)": {"beta": 0.4, "gamma": 0.1, "r0": 4.0},
        "Seasonal Influenza": {"beta": 0.25, "gamma": 0.2, "r0": 1.25},
        "Measles": {"beta": 1.2, "gamma": 0.08, "r0": 15.0},
        "Custom Scenario": {"beta": 0.3, "gamma": 0.1, "r0": 3.0}
    }
    return presets.get(preset_name, presets["Custom Scenario"])


def run_sir_model_advanced(beta=0.3, gamma=0.1, population=100000, days=100):
    """
    Runs the SIR differential equation model scaled to an actual population size.
    """
    def sir_equations(t, y):
        S, I, R = y
        # Normalized SIR differential equations scaled to population N
        dSdt = - (beta * S * I) / population
        dIdt = (beta * S * I) / population - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]

    # Initial conditions: 1 infected person, rest susceptible
    y0 = [population - 1, 1, 0]
    t_eval = np.linspace(0, days, days)

    sol = solve_ivp(sir_equations, (0, days), y0, t_eval=t_eval)

    return sol.t, sol.y

import numpy as np
from scipy.integrate import odeint


def seir_h_model(y, t, N, beta, sigma, gamma, eta):
    """
    SEIR-H Differential Equations System:
    S: Susceptible, E: Exposed (Incubating), I: Infected (Active), 
    R: Recovered, H: Hospitalized (Severe/ICU)
    """
    S, E, I, R, H = y

    dSdt = -beta * S * I / N
    dEdt = (beta * S * I / N) - (sigma * E)
    dIdt = (sigma * E) - (gamma * I) - (eta * I)
    dRdt = gamma * I
    dHdt = (eta * I)  # Flow rate of severe cases entering hospital care

    return [dSdt, dEdt, dIdt, dRdt, dHdt]


def run_epidemic_simulation(population, initial_cases, transmission_rate, incubation_days, recovery_days, hospitalization_rate, days=90):
    """
    Solves the SEIR-H system over a given time horizon.
    """
    N = population
    I0 = initial_cases
    E0 = initial_cases * 2  # Estimated latent exposed group
    R0 = 0
    H0 = 0
    S0 = N - I0 - E0

    # Rate parameters
    sigma = 1.0 / incubation_days if incubation_days > 0 else 0.2  # Incubation rate
    gamma = 1.0 / recovery_days if recovery_days > 0 else 0.1       # Recovery rate
    # Hospitalization probability rate
    eta = hospitalization_rate
    beta = transmission_rate

    t = np.linspace(0, days, days)
    y0 = [S0, E0, I0, R0, H0]

    # Solve system using SciPy
    ret = odeint(seir_h_model, y0, t, args=(N, beta, sigma, gamma, eta))
    S, E, I, R, H = ret.T

    return {
        "days": t,
        "susceptible": S,
        "exposed": E,
        "infected": I,
        "recovered": R,
        "hospitalized": H,
        "peak_hospitalizations": int(np.max(H)),
        "peak_day": int(np.argmax(H))
    }

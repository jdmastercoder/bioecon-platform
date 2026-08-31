import numpy as np


def run_stochastic_seir_h(population, initial_cases, transmission_rate, incubation_days,
                          recovery_days, hospitalization_rate, days=90, noise_intensity=0.02, runs=50):
    """
    Solves a System of Stochastic Differential Equations (SDEs) for SEIR-H dynamics
    using Euler-Maruyama integration over multiple Monte Carlo iterations.
    """
    dt = 0.1  # Time step size
    steps = int(days / dt)
    time_grid = np.linspace(0, days, steps)

    sigma = 1.0 / incubation_days
    gamma = 1.0 / recovery_days
    eta = hospitalization_rate

    # Store trajectories across all runs
    infected_runs = np.zeros((runs, steps))
    hospitalized_runs = np.zeros((runs, steps))

    for r in range(runs):
        S, E, I, H, R = population - \
            initial_cases, 0.0, float(initial_cases), 0.0, 0.0

        S_hist, E_hist, I_hist, H_hist, R_hist = [], [], [], [], []

        for t in range(steps):
            # Stochastic Wiener process noise term
            dW = np.random.normal(0, np.sqrt(dt))

            # Deterministic drifts
            dS = -transmission_rate * S * I / population
            dE = transmission_rate * S * I / population - sigma * E
            dI = sigma * E - gamma * I
            dH = eta * dI - (1.0 / 10.0) * H  # Average 10-day ICU stay
            dR = (1.0 - eta) * gamma * I + (1.0 / 10.0) * H

            # Stochastic updates (Euler-Maruyama)
            S += dS * dt + noise_intensity * S * dW
            E += dE * dt + noise_intensity * E * dW
            I += dI * dt + noise_intensity * I * dW
            H += dH * dt + noise_intensity * H * dW
            R += dR * dt

            # Conservation bounds
            S, E, I, H, R = max(0, S), max(
                0, E), max(0, I), max(0, H), max(0, R)

            I_hist.append(I)
            H_hist.append(H)

        infected_runs[r, :] = I_hist
        hospitalized_runs[r, :] = H_hist

    # Calculate 95% Confidence Intervals
    return {
        "time": time_grid,
        "infected_mean": np.mean(infected_runs, axis=0),
        "infected_lower": np.percentile(infected_runs, 2.5, axis=0),
        "infected_upper": np.percentile(infected_runs, 97.5, axis=0),
        "hospitalized_mean": np.mean(hospitalized_runs, axis=0),
        "hospitalized_lower": np.percentile(hospitalized_runs, 2.5, axis=0),
        "hospitalized_upper": np.percentile(hospitalized_runs, 97.5, axis=0),
    }

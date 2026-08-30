from health_engine import run_sir_model
from finance_engine import run_monte_carlo

print("Running Health Spread Simulation...")
days, health_data = run_sir_model()

print("Running Financial Risk Simulation...")
finance_paths = run_monte_carlo()

print("Analysis complete!")

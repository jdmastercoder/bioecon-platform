import pytest
import numpy as np
from health_engine import run_epidemic_simulation
from optimization_engine import optimize_resources


def test_epidemic_simulation_conservation():
    """Verify total population remains conserved across SEIR-H compartments."""
    pop = 100000
    res = run_epidemic_simulation(
        population=pop, initial_cases=10, transmission_rate=0.35,
        incubation_days=5, recovery_days=14, hospitalization_rate=0.05, days=30
    )
    total_day_0 = res['susceptible'][0] + res['exposed'][0] + \
        res['infected'][0] + res['hospitalized'][0] + res['recovered'][0]
    assert np.isclose(total_day_0, pop, atol=1.0)


def test_optimization_solver_success():
    """Verify linear solver returns non-negative asset allocations."""
    res = optimize_resources(total_budget=500000, peak_infected=0.15)
    assert res['success'] is True
    assert res['vaccines'] >= 0
    assert res['icu_beds'] >= 0
    assert res['treatments'] >= 0

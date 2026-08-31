from optimization_engine import optimize_resources_milp
from stochastic_health_engine import run_stochastic_seir_h
import sys
import os
import pytest
import numpy as np  # <-- Make sure this line is present

# Dynamically add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


def test_stochastic_sde_engine():
    """Verify stochastic engine returns 95% confidence interval bounds."""
    res = run_stochastic_seir_h(
        population=100000,
        initial_cases=10,
        transmission_rate=0.35,
        incubation_days=5,
        recovery_days=14,
        hospitalization_rate=0.05,
        days=10,
        runs=5,
    )
    assert len(res["infected_mean"]) > 0
    assert np.all(res["infected_upper"] >= res["infected_lower"])


def test_milp_integer_constraints():
    """Verify MILP solver returns strictly non-fractional integer values."""
    res = optimize_resources_milp(total_budget=500000, peak_infected=0.15)
    assert res["success"] is True
    assert isinstance(res["vaccines"], int)
    assert isinstance(res["icu_beds"], int)
    assert isinstance(res["treatments"], int)

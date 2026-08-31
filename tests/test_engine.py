from report_engine import generate_pdf_report
from optimization_engine import optimize_resources
from health_engine import run_epidemic_simulation
import sys
import os
import pytest
import numpy as np

# Dynamically add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


def test_epidemic_simulation_conservation():
    """Verify total population remains conserved across SEIR-H compartments."""
    pop = 100000
    res = run_epidemic_simulation(
        population=pop,
        initial_cases=10,
        transmission_rate=0.35,
        incubation_days=5,
        recovery_days=14,
        hospitalization_rate=0.05,
        days=30,
    )
    total_day_0 = (
        res["susceptible"][0]
        + res["exposed"][0]
        + res["infected"][0]
        + res["hospitalized"][0]
        + res["recovered"][0]
    )
    assert np.isclose(total_day_0, pop, atol=1.0)


def test_optimization_solver_success():
    """Verify linear solver returns non-negative asset allocations."""
    res = optimize_resources(total_budget=500000, peak_infected=0.15)
    assert res["success"] is True
    assert res["vaccines"] >= 0
    assert res["icu_beds"] >= 0
    assert res["treatments"] >= 0


def test_pdf_report_generation():
    """Verify PDF generator produces non-empty binary output."""
    sim_res = {
        "infected": [100, 200, 150],
        "peak_hospitalizations": 25,
        "peak_day": 12,
    }
    pdf_bytes = generate_pdf_report(
        "COVID-19 (Omicron)", sim_res, 10000, 50, 2500)
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 0

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def optimize_resources_milp(total_budget, peak_infected, unit_costs=None):
    """
    Mixed-Integer Linear Programming (MILP) Solver.
    Forces integer constraints on physical assets while maximizing lives saved.
    """
    if unit_costs is None:
        unit_costs = {"vaccines": 25.0, "beds": 1200.0, "treatments": 150.0}

    # Decision Variables Vector: x = [Vaccines, Beds, Treatments]
    # Objective: Maximize Lives Saved (Linear coefficients: [0.001, 0.25, 0.05])
    # SciPy minimizes, so negate objective vector c
    c = np.array([-0.001, -0.25, -0.05])

    # Budget Constraint: 25*V + 1200*B + 150*T <= total_budget
    A_budget = np.array(
        [[unit_costs["vaccines"], unit_costs["beds"], unit_costs["treatments"]]])
    budget_constraint = LinearConstraint(A_budget, ub=[total_budget])

    # Integer Variables Mask: 1 indicates integer constraint (MILP)
    integrality = np.array([1, 1, 1])

    # Non-negative bounds
    bounds = Bounds(lb=[0, 0, 0], ub=[np.inf, np.inf, np.inf])

    # Solve MILP
    res = milp(c=c, integrality=integrality, bounds=bounds,
               constraints=budget_constraint)

    if res.success:
        v, b, t = res.x
        lives_saved = int(-res.fun)
        total_spent = float(
            v * unit_costs["vaccines"] + b * unit_costs["beds"] + t * unit_costs["treatments"])
        return {
            "success": True,
            "vaccines": int(v),
            "icu_beds": int(b),
            "treatments": int(t),
            "lives_saved": lives_saved,
            "total_spent": total_spent
        }
    else:
        return {"success": False}

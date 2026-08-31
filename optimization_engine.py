import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds


def optimize_resources(total_budget, peak_infected, unit_costs=None):
    """
    Standard Linear Programming (LP) Solver using scipy.optimize.linprog.
    """
    if unit_costs is None:
        unit_costs = {"vaccines": 25.0, "beds": 1200.0, "treatments": 150.0}

    # Objective: Maximize Lives Saved (negated for minimization)
    c = [-0.001, -0.25, -0.05]

    # Inequality constraints matrix (A_ub * x <= b_ub)
    A_ub = [[unit_costs["vaccines"], unit_costs["beds"], unit_costs["treatments"]]]
    b_ub = [total_budget]

    # Bounds for variables (Vaccines, Beds, Treatments)
    x_bounds = (0, None)
    bounds = [x_bounds, x_bounds, x_bounds]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

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


def optimize_resources_milp(total_budget, peak_infected, unit_costs=None):
    """
    Mixed-Integer Linear Programming (MILP) Solver using scipy.optimize.milp.
    Forces strict integer constraints on physical assets.
    """
    if unit_costs is None:
        unit_costs = {"vaccines": 25.0, "beds": 1200.0, "treatments": 150.0}

    c = np.array([-0.001, -0.25, -0.05])
    A_budget = np.array(
        [[unit_costs["vaccines"], unit_costs["beds"], unit_costs["treatments"]]])
    budget_constraint = LinearConstraint(A_budget, ub=[total_budget])

    integrality = np.array([1, 1, 1])
    bounds = Bounds(lb=[0, 0, 0], ub=[np.inf, np.inf, np.inf])

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

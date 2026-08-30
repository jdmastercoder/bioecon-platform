import numpy as np
from scipy.optimize import linprog


def optimize_resources(total_budget, peak_infected):
    """
    Optimizes allocation between 3 resources:
    x0: Vaccines ($50 each, saves 0.8 lives on average)
    x1: ICU Beds ($500 each, saves 0.9 lives on average)
    x2: Antiviral Treatments ($150 each, saves 0.6 lives on average)
    """
    # Costs per unit
    costs = [50, 500, 150]

    # Impact coefficients (negative because linprog minimizes)
    # Minimizing -lives_saved is equivalent to maximizing lives_saved
    c = [-0.8, -0.9, -0.6]

    # Inequality Constraint: Total Cost <= Total Budget
    A_ub = [costs]
    b_ub = [total_budget]

    # Bounds for each resource: (min_units, max_units)
    # Require at least 100 vaccines, up to peak_infected estimate
    bounds = [
        (100, max(500, int(peak_infected * 1000))),  # Vaccines
        (10, 500),                                   # ICU Beds
        (50, int(peak_infected * 500))               # Treatments
    ]

    # Run Linear Programming Solver
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if res.success:
        vaccines, icu_beds, treatments = res.x
        lives_saved = -res.fun
        total_spent = sum(x * cost for x, cost in zip(res.x, costs))
        return {
            "success": True,
            "vaccines": int(vaccines),
            "icu_beds": int(icu_beds),
            "treatments": int(treatments),
            "lives_saved": int(lives_saved),
            "total_spent": round(total_spent, 2)
        }
    else:
        return {"success": False}

from bisimulation_learning.shared import *
from bisimulation_learning.fintely_branching.conditions import *

def solve_one_shot(
    transition_system: BranchingTransitionSystem,
    template: BDTTemplate,
    ):

    print("Using branching formulas namjoshi")

    model_params     = template.model_params
    s                = template.m
    succ_s           = template.succ_m
    w                = template.w
    ranking_params   = template.rank_params_branching_global

    formulas = encode_classification_branching(
        transition_system   = transition_system,
        template            = template,
        theta               = model_params,
        eta                 = ranking_params,
        s                   = s, 
        succ_s              = succ_s, 
        w                   = w,
        explicit_classes    = False # TODO remove. explicit classes only
    )

    formula = ForAll([*s, *succ_s, *w],
        And([simplify(phi) for phi in formulas])
    )

    solver = Solver()
    solver.add(formula)

    res = solver.check()

    if f"{res}" == "sat":
        print("Found a solution!")
        m = solver.model()
        theta = [m.evaluate(param) for param in model_params]
        rankp = [[m.evaluate(param) for param in l] for l in ranking_params]
        adj = compute_adjacency_matrix(transition_system, template, theta)
        return True, (theta, adj, rankp)
    else:
        return False, None
    

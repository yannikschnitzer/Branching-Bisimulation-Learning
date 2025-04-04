from bisimulation_learning.fact_det.conditions import *
from bisimulation_learning.shared import *

def solve_one_shot(
    transition_system: DeterministicTransitionSystem,
    template: BDTTemplate
    ):
    
    model_params     = template.model_params
    adjacency_params = template.adjacency_params
    s                = template.m
    succ_s           = template.succ_m

    formulas = []

    print("Using deterministic formulas")
    ranking_params   = template.rank_params
    # formuals contain both cond_1 and cond_2
    formulas = encode_classification(
        transition_system   = transition_system,
        template            = template,
        proof_rules         = conds_wfb_deterministic,
        theta               = model_params,
        gamma               = adjacency_params,
        eta                 = ranking_params,
        s                   = s,
        succ_s              = succ_s
    )

    formula = ForAll([*s, *succ_s],
        And([simplify(phi) for phi in formulas])
    )

    solver = Solver()
    solver.add(formula)

    # resort to additional if fails


    res = solver.check()
    if f"{res}" == "sat":
        print("Found a solution!")
        return True, extract_solution(solver, template)
    else:
        return False, None


def encode_one_shot_additional(
    transition_system: DeterministicTransitionSystem,
    template: BDTTemplate,
    theta, gamma, eta, 
    s, succ_s
    ):

    phis = []

    successor = transition_system.successor
    domain    = transition_system.domain
    f, g, h   = template.get_template_functions()

    for p in template.partitions:
        phis.append(Implies(
            And(g(gamma, p, p) == IntVal(1),
                f(theta, s) == p,
                successor(s, succ_s),
                domain(s), 
                domain(succ_s)
            ), 
            f(theta, succ_s) == p
        ))
    
    return phis

from bl_solver.template import *
from bl_solver.transition_system import *

def one_shot(
    transition_system: TransitionSystem,
    abstract_system  : AbstractSystem,
    proposed_template: ProposedTemplate):
    
    model_params     = proposed_template.model_params
    adjacency_params = proposed_template.adjacency_params
    ranking_params   = proposed_template.rank_params
    s                = proposed_template.m
    succ_s           = proposed_template.succ_m

    # formuals contain both cond_1 and cond_2
    formulas = encode_classification(
        transition_system=transition_system,
        proposed_template=proposed_template,
        theta=model_params,
        gamma=adjacency_params,
        eta=ranking_params,
        s=s,
        succ_s=succ_s
    )

    formulas += encode_one_shot_additional(
        transition_system=transition_system,
        proposed_template=proposed_template,
        theta=model_params,
        gamma=adjacency_params,
        eta=ranking_params,
        s=s,
        succ_s=succ_s
    )

    formula = ForAll([*s, *succ_s],
        And([simplify(phi) for phi in formulas])
    )

    solver = Solver()
    solver.add(formula)
    res = solver.check()
    if f"{res}" == "sat":
        return True, extract_solution(solver, proposed_template)
    else:
        return False, None

def encode_one_shot_additional(
    transition_system: TransitionSystem,
    proposed_template: ProposedTemplate,
    theta, gamma, eta, 
    s, succ_s
    ):

    phis = []

    successor = transition_system.successor
    domain    = transition_system.domain
    f, g, h   = proposed_template.get_template_functions()

    for p in proposed_template.partitions:
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
    

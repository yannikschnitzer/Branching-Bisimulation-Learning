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
    print(formulas)

    formula = ForAll([*s, *succ_s],
        And(formulas)
    )

    solver = Solver()
    solver.add(formula)
    res = solver.check()
    if f"{res}" == "sat":
        return True, extract_solution(solver, proposed_template)
    else:
        return False, None


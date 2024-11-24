
from bl_solver.template import *
from bl_solver.z3_utils import *

def bisimulation_learning(transition_system: TransitionSystem, abstract_system: AbstractSystem, iters = 10):
    while True:
        template = ProposedTemplate(transition_system.dim, abstract_system)
        success, params = guess_and_check(transition_system, template, iters)
        if success:
            theta, gamma, eta = params
            print(f"{theta} {gamma} {eta}")
            # TODO print something more meaningful
            break
        else:
            # TODO propose new template
            pass

# cegis
def guess_and_check(transition_system: TransitionSystem, proposed_template: ProposedTemplate, iters):
    counterexamples = []
    for _ in range(iters):
        verified, (theta, gamma, eta) = guess(transition_system, proposed_template, counterexamples)
        print(f"""Proposed params are
        theta = {theta}
        gamma = {gamma}
        eta   = {eta}
        """)
        if verified:
            new_cexs = check(transition_system, proposed_template, theta, gamma, eta)
            print(f"New counterexamples = {new_cexs}")
            if len(new_cexs) == 0:
                return True, (theta, gamma, eta)
            else:
                counterexamples += new_cexs
        else:
            return False, None

def guess(transition_system: TransitionSystem, proposed_template: ProposedTemplate, counterexamples):
    """
    Takes as input a proposed template and a list of
    counterexamples in the form of a tuple (s, T(s)).

    Returns new theta, gamma, eta for the proposed template
    """

    theta = proposed_template.model_params
    gamma = proposed_template.adjacency_params
    eta   = proposed_template.rank_params
    formulas  = []

    for (s, succ_s) in counterexamples:
        formulas += encode_classification(
            transition_system=transition_system,
            proposed_template=proposed_template,
            theta=theta,
            gamma=gamma,
            eta=eta,
            s=s,
            succ_s=succ_s
        )
    
    solver = Solver()
    for formula in formulas:
        solver.add(simplify(formula))
    
    res = solver.check()
    
    if f"{res}" == "sat":
        return True, extract_solution(solver, proposed_template)
    else:
        # signal you have to change the template
        return False, None

def check(transition_system: TransitionSystem, proposed_template: ProposedTemplate, theta, gamma, eta):
    s = proposed_template.m
    succ_s = proposed_template.succ_m

    print(f"s = {s} succ_s = {succ_s}")

    counterexamples = []
    formulas = encode_classification(
        transition_system=transition_system,
        proposed_template=proposed_template,
        theta=theta,
        gamma=gamma,
        eta=eta,
        s=s,
        succ_s=succ_s
    )

    for formula in formulas:
        # NOTE: can be done in parallel
        solver = Solver()
        solver.add(simplify(Not(formula)))
        res = solver.check()
        if f"{res}" == "sat":
            model = solver.model()

            m = [eval_z3(model, n) for n in s]
            succ_m = [eval_z3(model, n) for n in succ_s]
            counterexamples.append((m, succ_m))
        else:
            # Good, nothing to do!
            pass
    
    return counterexamples


from bisimulation_learning.shared import *
from z3 import *


def bisimulation_learning(transition_system: DeterministicTransitionSystem, template: BDTTemplate, iters = 10):
    while True:
        success, params = guess_and_check(
            transition_system   = transition_system,
            template            = template,
            iters               = iters
        )
        if success:
            theta, gamma, eta = params
            return theta, gamma, eta
        else:
            # TODO propose new template
            return None, None, None


def guess_and_check(
    transition_system: DeterministicTransitionSystem, 
    template: BDTTemplate,
    iters = 10
    ):
    counterexamples = []
    for _ in range(iters):
        verified, (theta, gamma, eta) = guess(transition_system, template, counterexamples)
        if verified:
            new_cexs = check(transition_system, template, theta, gamma, eta)
            if len(new_cexs) == 0:
                return True, (theta, gamma, eta)
            else:
                counterexamples += new_cexs
        else:
            return False, None

def guess(transition_system: DeterministicTransitionSystem, template: BDTTemplate, counterexamples):
    """
    Takes as input a proposed template and a list of
    counterexamples in the form of a tuple (s, T(s)).

    Returns new theta, gamma, eta for the proposed template
    """

    theta = template.model_params
    gamma = template.adjacency_params
    eta   = template.rank_params
    formulas  = []

    for (s, succ_s) in counterexamples:
        formulas += encode_classification(
            transition_system   = transition_system,
            template            = template,
            theta               = theta,
            gamma               = gamma,
            eta                 = eta,
            s                   = s,
            succ_s              = succ_s
        )
    
    solver = Solver()
    for formula in formulas:
        solver.add(simplify(formula))
    
    res = solver.check()
    
    if f"{res}" == "sat":
        return True, extract_solution(solver, template)
    else:
        # signal you have to change the template
        return False, None


def check(transition_system: DeterministicTransitionSystem, template: BDTTemplate, theta, gamma, eta):
    s = template.m
    succ_s = template.succ_m

    counterexamples = []
    formulas = encode_classification(
        transition_system   = transition_system,
        template            = template,
        theta               = theta,
        gamma               = gamma,
        eta                 = eta,
        s                   = s,
        succ_s              = succ_s
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


from bl_solver.template import *
from bl_solver.z3_utils import *
from z3 import *

def branching_bisimulation_learning(transition_system: BranchingTransitionSystem, template: BDTTemplate, iters = 10):
    while True:
        success, params = branching_guess_and_check(
            transition_system   = transition_system,
            template            = template,
            iters               = iters
        )
        if success:
            theta, eta = params
            return theta, eta
        else:
            # TODO propose new template
            return None, None

def bisimulation_learning(transition_system: DeterminsticTransitionSystem, template: BDTTemplate, iters = 10):
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

def branching_guess_and_check(
    transition_system: DeterminsticTransitionSystem, 
    template: BDTTemplate,
    iters = 10
    ):
    counterexamples = []
    for _ in range(iters):
        verified, (theta, eta) = branching_guess(transition_system, template, counterexamples)
        if verified:
            new_cexs = branching_check(transition_system, template, theta, eta)
            if len(new_cexs) == 0:
                return True, (theta, eta)
            else:
                counterexamples += new_cexs
        else:
            return False, None

# cegis
def guess_and_check(
    transition_system: DeterminsticTransitionSystem, 
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

def branching_guess(transition_system: BranchingTransitionSystem, template: BDTTemplate, counterexamples):

    theta    = template.model_params
    eta      = template.rank_params_branching_global
    formulas = []

    for (s, succ_s, w) in counterexamples:
        formulas += encode_classification_branching(
            transition_system=transition_system,
            template=template,
            theta=theta, eta=eta,
            s=s, succ_s=succ_s, w=w
        )
    
    solver = Solver()
    for formula in formulas:
        solver.add(simplify(formula))
    
    res = solver.check()
    if res == sat:
        model = solver.model()
        guessed_theta = [model.evaluate(p) for p in theta]
        guessed_eta   = [[model.evaluate(p) for p in d] for d in eta]
        return True, (guessed_theta, guessed_eta)
    elif res == unsat:
        return False, None
    else:
        raise Exception(f"""
        Unexpected result in guess solver
        Expected: {sat} or {unsat}
        Got: {res} with reason {res.reason_unknown()}
        """)


def guess(transition_system: DeterminsticTransitionSystem, template: BDTTemplate, counterexamples):
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
            transition_system=transition_system,
            template=template,
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
        return True, extract_solution(solver, template)
    else:
        # signal you have to change the template
        return False, None

def branching_check(transition_system: DeterminsticTransitionSystem, template: BDTTemplate, theta, eta):
    s      = template.m
    succ_s = template.succ_m
    t      = template.w

    counterexamples = []

    formulas = encode_classification_branching(
        transition_system=transition_system,
        template=template,
        theta=theta, eta=eta,
        s=s, succ_s=succ_s, w=t
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
            w = [eval_z3(model, n) for n in t]
            counterexamples.append((m, succ_m, w))
        else:
            # Good, nothing to do!
            pass
    
    return counterexamples
        


def check(transition_system: DeterminsticTransitionSystem, template: BDTTemplate, theta, gamma, eta):
    s = template.m
    succ_s = template.succ_m

    counterexamples = []
    formulas = encode_classification(
        transition_system=transition_system,
        template=template,
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


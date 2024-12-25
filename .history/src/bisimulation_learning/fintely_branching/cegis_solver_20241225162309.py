
from bisimulation_learning.shared import *
from z3 import *
from bisimulation_learning.fintely_branching.conditions import *


solver = Solver()
set_param('smt.random_seed', 42)

def bisimulation_learning(
    transition_system: BranchingTransitionSystem, 
    template: BDTTemplate, 
    iters = 10,
    explicit_classes = False
    ):
    while True:
        success, params = guess_and_check(
            transition_system   = transition_system,
            template            = template,
            iters               = iters,
            explicit_classes    = explicit_classes
        )
        if success:
            theta, eta = params
            return theta, eta
        else:
            # TODO propose new template
            return None, None


def guess_and_check(
    transition_system: DeterministicTransitionSystem, 
    template: BDTTemplate,
    iters = 10,
    explicit_classes = False
    ):

    counterexamples = []
    solver = Solver()
    for _ in range(iters):
        # TODO: Initial samples
        verified, (theta, eta) = guess(solver,transition_system, template, counterexamples, explicit_classes)
        if verified:
            new_cexs = check(transition_system, template, theta, eta, explicit_classes)
            if len(new_cexs) == 0:
                return True, (theta, eta)
            else:

                counterexamples += new_cexs
        else:
            raise Exception("Unexpected failure for guess operation. Perhap")
    return False, None


def guess(
    transition_system: BranchingTransitionSystem, 
    template: BDTTemplate, 
    counterexamples,
    explicit_classes = False
    ):

    theta    = template.model_params
    eta      = template.rank_params_branching_classes if explicit_classes else template.rank_params_branching_global
    formulas = []

    for (s, succ_s, w) in counterexamples:
        formulas += encode_classification_branching(
            transition_system   = transition_system,
            template            = template,
            theta               = theta, 
            eta                 = eta,
            s                   = s, 
            succ_s              = succ_s, 
            w                   = w,
            explicit_classes    = explicit_classes
        )
    
    solver.reset()
  
    for formula in formulas:
        solver.add(simplify(formula))
    
    res = solver.check()
    if res == sat:
        model = solver.model()
        guessed_theta = [model.evaluate(p) for p in theta]
        guessed_eta   = [[model.evaluate(p) for p in d] for d in eta]
        return True, (guessed_theta, guessed_eta)
    elif res == unsat:
        print(f"[GUESS] Formula cannot be satisfied")
        return False, None
    else:
        raise Exception(f"""
        Unexpected result in guess solver
        Expected: {sat} or {unsat}
        Got: {res} with reason {res.reason_unknown()}
        """)

def check(
    transition_system: DeterministicTransitionSystem, 
    template: BDTTemplate, 
    theta, 
    eta,
    explicit_classes = False
    ):
    s      = template.m
    succ_s = template.succ_m
    t      = template.w

    counterexamples = []

    formulas = encode_classification_branching(
        transition_system   = transition_system,
        template            = template,
        theta               = theta, 
        eta                 = eta,
        s                   = s, 
        succ_s              = succ_s, 
        w                   = t,
        explicit_classes    = explicit_classes
    )

    for formula in formulas:
        # NOTE: can be done in parallel
        solver.reset()
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



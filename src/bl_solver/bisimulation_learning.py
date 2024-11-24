
from bl_solver.template import *

def guess(proposed_template: ProposedTemplate, counterexamples):
    """
    Takes as input a proposed template and a list of
    counterexamples in the form of a tuple (s, T(s)).

    Returns new theta, gamma, eta for the proposed template
    """

    theta = proposed_template.model_params
    gamma = proposed_template.adjacency_params
    eta   = proposed_template.rank_params
    formulas  = []

    for (s, s_succ) in counterexamples:
        formulas += encode_classification(
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

def check(proposed_template: ProposedTemplate, theta, gamma, eta):
    s = proposed_template.m
    succ_s = proposed_template.succ_m

    counterexamples = []
    formulas = encode_classification(
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
        if f"{res}" == "res":
            model = solver.model()

            m = [[eval_z3(mod, n) for n in s]]
            succ_m = [[eval_z3(mod, n) for n in succ_s]]
            counterexamples.append((m, succ_m))
        else:
            # Good, nothing to do!
            pass
    
    return counterexamples

class BisimulationLearning:

    def __init__(self, verbose = True, iters = 10):
        self.verbose = verbose
        self.iters = iters

    def main(transition_system):
        while True:
            template = ProposedTemplate(transition_system)
            theta, gamma, eta = self.guess_and_check(template)
            print(f"{theta} {gamma} {eta}")
            # TODO print something more meaningfull

    # cegis
    def guess_and_check(self, proposed_template: ProposedTemplate):
        counterexamples = []
        for _ in range(self.iters):
            verified, (theta, gamma, eta) = guess(proposed_template, counterexamples)
            if verified:
                new_cexs = check(proposed_template, theta, gamma, eta)
                if len(new_cexs) == 0:
                    return theta, gamma, eta
                else:
                    counterexamples += new_cexs
            else:
                # TODO propose new template
                pass

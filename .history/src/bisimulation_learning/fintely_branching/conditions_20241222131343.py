
from z3 import *
from bisimulation_learning.shared import *

"""
For (finitely) branching systems we implement only Namjoshi's conditions, 
given s, s' and t and that s (stuttering) bisimilar to t.

We just check against the partition template and the ranking function.
"""

def cond_implicit_partiton(
    successors, domain,
    f, h,
    theta, eta,
    s, succ_s, w
    ):
    """
    This function encodes the condition for the branching 
    well-founded bisimulation without taking any explicit partition,
    over a given *global* ranking function template h, eta
    """
    assumptions = And(
        domain(s),
        domain(succ_s),
        domain(w),
        f(theta, s) == f(theta, w), 
        Or([variables_equals(succ_s, u) for u in successors(s)])
    )
    straight_bisimulation = [f(theta, succ_s) == f(theta, v) for v in successors(w)]        
    stutter_on_s = And(
        f(theta, succ_s) == f(theta, w),
        h(eta, succ_s, succ_s) < h(eta, s, s)
    )
    # i.e. there is at least one successor v of w s.t. 
    stutter_on_w = [
        And(f(theta, s) == f(theta, v), h(eta, succ_s, v) < h(eta, succ_s, w))
            for v in successors(w)]
    return Implies(
        assumptions,
        Or(*straight_bisimulation, stutter_on_s, *stutter_on_w)
    )

def cond_explicit_partiton(
    successors, domain,
    f, h,
    theta, eta,
    c,
    s, succ_s, w
    ):
    assumptions = And(
        f(theta, s) == c, 
        f(theta, w) == c,
        Or([variables_equals(succ_s, u) for u in successors(s)])
    )
    straight_bisimulation = [f(theta, succ_s) == f(theta, v) for v in successors(w)]
    stutter_on_s = And(
        f(theta, succ_s) == c,
        h(eta, c, succ_s, succ_s) < h(eta, c, s, s)
    )
    stutter_on_w = [
        And(f(theta, v) == c, h(eta, c, succ_s, v) < h(eta, c, succ_s, w))
            for v in successors(w)]
    return Implies(
        assumptions,
        Or(*straight_bisimulation, stutter_on_s, *stutter_on_w)
    )


def encode_classification_branching(
    transition_system: BranchingTransitionSystem,
    template: BDTTemplate,
    theta, eta,
    s, succ_s, w,
    explicit_classes = False
    ):
    f, g, h = template.get_template_functions(branching=True, explicit_classes=explicit_classes)

    conds = []
    if explicit_classes:
        for p in template.partitions:
            cond = cond_explicit_partiton(
                successors  = transition_system.successors,
                domain      = transition_system.domain,
                f           = f, 
                h           = h,
                theta       = theta,
                eta         = eta,
                s           = s, 
                succ_s      = succ_s, 
                w           = w,
                c           = p
            )
            conds.append(cond)
        
    else:
        cond = cond_implicit_partiton(
            successors  = transition_system.successors,
            domain      = transition_system.domain,
            f           = f, 
            h           = h,
            theta       = theta, 
            eta         = eta,
            s           = s, 
            succ_s      = succ_s, 
            w           = w
        )
        conds = [cond]
    
    return conds

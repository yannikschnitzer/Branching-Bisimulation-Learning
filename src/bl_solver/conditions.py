
from z3 import *
from bl_solver.z3_utils import *

"""
    Conditions for the well founded bisimulation.

    Those functions take in input information about:
        - the concrete transition system
        - the template of the proposed abstract transition system, 
        - the parameters for such template
        - concrete values to check whether the conditions hold
    
    For the TS they require:
        - successor function
        - the domain constraint for state variables
    
    For the template of the abstract TS:
        - classification function f : Theta -> S -> S (based on BDTs)
        - abstract successor function g : Gamma -> S -> S -> IntVal(1) | IntVal(0) (which can even be z3's True and False)
        - ranking function h : Eta -> S\\simeq -> S -> Nat
    
    Concrete values to check against our formulas:
        - partitions p and its successor q
        - state s and its successor succ_s
    
"""

def cond_2_deterministic(
    successor, domain, # the successor function of the TS
    f, g, h, # the template for the abstract TS
    theta, gamma, eta, # the parameters for the template
    p, q, s, succ_s # the concrete values to check condition 2
    ):
    """
        Represents condition 2 from theorem 3,
        i.e. the "ranking condition".
    """
    return Implies(
        And(variables_equals(succ_s, successor(s)),
            g(gamma, p, q) == IntVal(1), 
            Not(p == q),
            f(theta, s) == p, 
            domain(s), 
            domain(succ_s)
        ), 
        Or( f(theta, succ_s) == q,
            And(f(theta, succ_s) == p,
                h(eta, p, s) > h(eta, p, succ_s)
            )
        )    
    )

def cond_1_deterministic(
    successor, domain, # the successor function of the TS
    f, g, # h, # the template for the abstract TS
    theta, gamma, # eta, # the parameters for the template
    p, q, s, succ_s # the concrete values to check condition 
    ):
    """
        Represents condition 3 from theorem 3.

        Note that here neither h nor eta are used,
        so we don't even require it
    """
    return Implies(
        And(variables_equals(succ_s, successor(s)),
            f(theta, s) == p, 
            f(theta, succ_s) == q, 
            domain(s), 
            domain(succ_s), 
            (Not(p == q))
        ), 
        g(gamma, p, q) == IntVal(1)
    )

"""
For (finitely) branching systems we implement only Namjoshi's conditions, 
given s, s' and t and that s (stuttering) bisimilar to t.

We just check against the partition template and the ranking function.
"""

def cond_branching_no_explicit_partiton(
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
    straight_bisimulation = Or([f(theta, succ_s) == f(theta, v) for v in successors(w)])
    stutter_on_s = And(
        f(theta, succ_s) == f(theta, w),
        h(eta, succ_s, succ_s) < h(eta, s, s)
    )
    # i.e. there is at least one successor v of w s.t. 
    stutter_on_w = Or([
        And(f(theta, s) == f(theta, v), h(eta, succ_s, v) < h(eta, succ_s, w))
            for v in successors(w)]
    )
    return Implies(
        assumptions,
        Or(straight_bisimulation, stutter_on_s, stutter_on_w)
    )

def cond_branching_explicit_partiton(
    successors, domain,
    f, h,
    theta, eta,
    c,
    s, succ_s, w):
    assumptions = And(
        domain(s),
        domain(succ_s),
        domain(w),
        f(theta, s) == c, 
        f(theta, w) == c,
        Or([succ_s == u for u in successors(s)])
    )
    straight_bisimulation = Or([f(theta, succ_s) == f(theta, v) for v in successors(w)])
    stutter_on_s = And(
        f(theta, succ_s) == c,
        h(eta, succ_s, succ_s) < h(eta, s, s)
    )
    # i.e. there is at least one successor v of w s.t. 
    stutter_on_w = Or([
        And(f(theta, v) == c, h(eta, succ_s, v) < h(eta, succ_s, w))
            for v in successors(w)]
    )
    return Implies(
        assumptions,
        Or(straight_bisimulation, stutter_on_s, stutter_on_w)
    )

def conds_wbs_deterministic(
    successor, domain, # the successor function of the TS
    f, g, h, # the template for the abstract TS
    theta, gamma, eta, # the parameters for the template
    p, q, s, succ_s # the concrete values to check condition 2
    ):
    """
    Returns the complete conditions for a well founded
    bisimulations over a deterministic system.
    """
    c1 = cond_1_deterministic(
        successor=successor,
        domain=domain,
        f=f,
        g=g,
        theta=theta,
        gamma=gamma,
        s=s,
        succ_s=succ_s,
        p=p,
        q=q
    )
    c2 = cond_2_deterministic(
        successor=successor,
        domain=domain,
        f=f,
        g=g,
        h=h,
        theta=theta,
        gamma=gamma,
        eta=eta,
        s=s,
        succ_s=succ_s,
        p=p,
        q=q
    )
    return [c1, c2]

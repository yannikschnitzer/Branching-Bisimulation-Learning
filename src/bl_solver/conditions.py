
from z3 import *

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

def cond_2(
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
        And(successor(s, succ_s),
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

def cond_1(
    successor, domain, # the successor function of the TS
    f, g, # h, # the template for the abstract TS
    theta, gamma, # eta, # the parameters for the template
    p, q, s, succ_s # the concrete values to check condition 2
    ):
    """
        Represents condition 3 from theorem 3.

        Note that here neither h nor eta are used,
        so we don't even require it
    """
    return Implies(
        And(successor(s, succ_s),
            f(theta, s) == p, 
            f(theta, succ_s) == q, 
            domain(s), 
            domain(succ_s), 
            (Not(p == q))
        ), 
        g(gamma, p, q) == IntVal(1)
    )

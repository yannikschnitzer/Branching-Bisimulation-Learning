
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
        And(successor(s, succ_s),
            f(theta, s) == p, 
            f(theta, succ_s) == q, 
            domain(s), 
            domain(succ_s), 
            (Not(p == q))
        ), 
        g(gamma, p, q) == IntVal(1)
    )

"""
We define for condition 1 and 2
    p the partition of s and w
    q the partition of v : w-->v (it always exists since non blocking systems)

So we need to assume g(gamma, p, q) == 1
--

We define for condition 3
    p the partition of s, w and v
    q the partition of u = u

So we need to assume g(gamma, p, q) == 1
"""

def cond_1_branching(
    successor, domain, # the successor function of the TS
    f, g, h, # the template for the abstract TS
    theta, gamma, eta, # the parameters for the template
    p, q, 
    s, succ_s # the concrete values to check condition 
    ):
    return Implies(
        And(successor(s, succ_s),           # s-->u
            f(theta, s) == p,               # s : p (s B w) 
            g(gamma, p, q) == IntVal(1),    # w-->v : q
            domain(s), 
            domain(succ_s)
        ),
        f(theta, succ_s) == q,              # u : q (u B v)
    )

def cond_2_branching(
    successor, domain, # the successor function of the TS
    f, g, h, # the template for the abstract TS
    theta, gamma, eta, # the parameters for the template
    p, q, 
    s, succ_s # the concrete values to check condition 
    ):
    return Implies(
        And(successor(s, succ_s),               # s-->u
            f(theta, s) == p,                   # s B w
            Not(q == p),                        # stutter only if not self loop
            domain(s), 
            domain(succ_s)),
        And(f(theta, succ_s) == p,              # u B w
            h(eta, p, succ_s) < h(eta, p, s)    # decrease rank of u
        )
    )

def cond_3_branching(
    successor, domain, # the successor function of the TS
    f, g, h, # the template for the abstract TS
    theta, gamma, eta, # the parameters for the template
    p, q, 
    s, succ_s # the concrete values to check condition 
    ):
    return Implies(
        And(successor(s, succ_s),               # w-->v
            f(theta, s) == p,                   # s B w
            g(gamma, p, q) == IntVal(1),        # u : q (we assume it exists since non blocking)
            Not(p == q),
            domain(s), 
            domain(succ_s)),
        And(f(theta, succ_s) == p,              # s B v
            h(eta, q, succ_s) < h(eta, q, s)    # ranking condition 
        )
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


def conds_wbs_branching(
    successor, domain, # the successor function of the TS
    f, g, h, # the template for the abstract TS
    theta, gamma, eta, # the parameters for the template
    p, q, s, succ_s # the concrete values to check condition 2
    ):
    """
    Returns the complete conditions for a well founded
    bisimulations over a deterministic system.
    """
    c1 = cond_1_branching(
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
    c2 = cond_2_branching(
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
    c3 = cond_3_branching(
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
    return [c1, c2, c3]



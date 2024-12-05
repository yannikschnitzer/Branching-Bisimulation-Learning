from z3 import *
from bisimulation_learning.shared import *

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

def cond_3(
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

def conds_wfb_deterministic(
    successor, domain, # the successor function of the TS
    f, g, h, # the template for the abstract TS
    theta, gamma, eta, # the parameters for the template
    p, q, s, succ_s # the concrete values to check condition 2
    ):
    """
    Returns the complete conditions for a well founded
    bisimulations over a deterministic system.
    """
    c1 = cond_3(
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
    c2 = cond_2(
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

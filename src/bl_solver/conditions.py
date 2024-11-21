
from z3 import *

class ConditionsCEGIS:

    """
    Conditions for the well founded bisimulation.

    Those functions require:
        - partitions p and q,
        - classification of s and T(s)
        - domain formulas for s and T(s)
        - adjacency value == 1 iff g(p) == q
        - ranking values for s and T(s)
    """

    # TODO: take as argument the successor formula
    # eg. Or(t_m_0 = m_0 + 1, t_m_0 = m_0 - 1)
    # The classification should account for that
    # i.e. express class_succ in terms of t_m_0
    def condition_1(p, q, class_s, class_succ, is_dom_s, is_dom_succ, p_q_adjacent):
        """
            Condition 1 for for well founded bisimulation.
            Asks for parameters:
                - p (concrete partition)
                - q (concrete partition)
                - class_s (classification formula for s)
                - class_succ (classification formula for T(s))
                - is_dom_s (formula for s to be in the domain)
                - is_dom_succ (formula as above)
                - p_q_adjacent (formula returning 1 or 0) 
            Optimization notes:
                - this formula evaluates always True when p == q
                - when it is known in advance that p and q are adjacent, set p_q_adjacent=1
                - when the opposite, set it equals to 0
        """
        return Implies(
            And(class_s == p,
                class_succ == q, 
                is_dom_s, 
                is_dom_succ,
                Not(p == q)
            ), 
            p_q_adjacent == IntVal(1)
        )
    
    def condition_2(p, q, class_s, class_succ, is_dom_s, is_dom_succ, p_q_adjacent, rnk_s, rnk_succ):
        """
            Condition 2 for for well founded bisimulation.
            Asks for parameters:
                - p (concrete partition)
                - q (concrete partition)
                - class_s (classification formula for s)
                - class_succ (classification formula for T(s))
                - is_dom_s (formula for s to be in the domain)
                - is_dom_succ (formula as above)
                - p_q_adjacent (formula returning 1 or 0)
                - rnk_s (the rank of s)
                - rnk_succ (the rank of T(s))

            Optimization notes:
                - this formula evaluates always True when p == q
                - this formula evaluates always True when p is not adjacent with q (i.e. p_q_adjacent == 0)
        """
        return Implies(
            And(p_q_adjacent == IntVal(1), 
                class_s == p, 
                is_dom_s, 
                is_dom_succ,
                Not(p == q)
            ), 
            Or( class_succ == q,
                And(class_succ == p, rnk_s > rnk_succ)
            )    
        )

class ConditionsOneShot:
    """
    Represents an instance of the conditions formulas for Theorem 3
    given a fixed transition system, i.e. passing as arguments of 
    the class constructor:
        - the successor function;
        - the domain constraint for the states of the given system;
        - the classification BDT.
    
    Condition functions' arguments are:
        - theta: parameters of the classification BDT, i.e. the parameters for f(theta; s);
        - gamma: parameters of adjacency, in this case a function s.t. gamma(p, q) == 1 iff g(p) = q;
        - eta: parameters for the ranking function;
    Those preceding arguments are the parameters for the formulas in the paper. Follow now the formula arguments:
        - s: the state to check te formula against
    Now follow the classification expectations:
        - p: the classification of s
        - q: the classification of T(s)
    """
    def __init__(self, successor, domain, classify):
        self.successor = successor
        self.domain = domain
        self.classify = classify

    def condition_2(self, theta, gamma, eta, s, succ_s, p, q):
        """
        Represents formula Phi_1 given state p and q to check, i.e. Condition 2 of Theorem 3.
        To see what the arguments are, refer to the class' description.

        Note that in this case, eta is unused since there is no ranking function
        but it is declared to make the function definition consistent as in the paper.
        """
        return Implies(
            And(self.successor(s, succ_s),
                self.classify(theta, s) == p, 
                self.classify(theta, succ_s) == q, 
                self.domain(s), 
                self.domain(succ_s), 
                (Not(p == q))
            ), 
            gamma(p, q) == 1
        )
    
    def condition_1(self, theta, gamma, rank, s, succ_s, p, q):
        """
        Represents Phi_2 given state p and q to check, i.e. Condition 3 of Theorem 3.
        To see what the arguments are, refer to the class' description.
        """
        return And(
            Implies(
                And(self.successor(s, succ_s),
                    gamma(p, q) == 1, 
                    Not(p == q),
                    self.classify(theta, s) == p, 
                    self.domain(s), 
                    self.domain(succ_s)
                ), 
                Or( self.classify(theta, succ_s) == q,
                    And(self.classify(theta, succ_s) == p,
                        rank(p, s) > rank(p, succ_s)
                    )
                )    
            ),
            # TODO not quite sure from where is this from
            Implies(
                And(gamma(p, q) == 1, 
                    (p == q)
                ), 
                Implies(
                    And(self.successor(s, succ_s),
                        self.classify(theta, s) == p, 
                        self.domain(s), 
                        self.domain(succ_s)
                    ), 
                    self.classify(theta, succ_s) == p)
                )
        )

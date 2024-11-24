from z3 import *

"""
Utilities wrapper around z3
"""

def eval_z3(m, x):
        """
            Evaluate Z3 result
        """
        return m.evaluate(x) if not (m.evaluate(x) == x) else 0
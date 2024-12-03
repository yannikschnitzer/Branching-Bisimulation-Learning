from z3 import *

"""
Utilities wrapper around z3
"""

def eval_z3(m, x):
        """
            Evaluate Z3 result
        """
        return m.evaluate(x) if not (m.evaluate(x) == x) else 0

def variables_equals(s, t):
    if len(s) != len(t):
        raise Exception(f"""
        Tried to check whether two variables are equal, but they have different lenght
        {len(s)} != {len(t)}
        First variable was {s}
        Second variable was {t}
        """)
    return And([s[d] == t[d] for d in range(len(s))])

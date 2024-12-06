from bisimulation_learning.shared import *
from bisimulation_learning.deterministic.experiments.conditional_termination_succ_trees import bdt_term_loop_2

"""
Branching system termination

three states:
x > 0 can either loop into itself, or go in x = 0
x = 0 can only loop
x < 0 can only loop

while  x < -1 or x > 1  do
    x := x + if random and x > 1
        then +1
        else -1

"""

def successors_term_loop_nd(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    terminated = And(s[0] >= -1, s[0] <= 1)

    # if random = false
    succ_s_act_1[0] = If(terminated, 
        s[0], 
        s[0] - 1
    )
    succ_s_act_1[1] = s[1]

    # if random = true
    succ_s_act_2[0] = If(terminated, 
        s[0], 
        If(s[0] > 1, s[0] + 1, s[0] - 1)
    )
    succ_s_act_2[1] = s[1]

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - term-loop-2
# 
# Labelling Function: x[0] > 0 -> not-terminated, x[0] <= 1 -> terminated
def bdt_term_loop_nd(params, x, num_params, partitions):
    u = BDTNodePoly([params[num_params], params[num_params+1]], x, params[0],
                        BDTLeave(partitions[0]), BDTLeave(partitions[1]))

    v = BDTNodePoly([params[num_params+2], params[num_params+3]], x, params[1],
                        BDTLeave(partitions[0]), BDTLeave(partitions[1]))

    b = BDTNodePoly([RealVal(1),RealVal(0)],x, RealVal(1), 
            BDTNodePoly([RealVal(-1),RealVal(0)],x, RealVal(1), 
                        BDTLeave(partitions[2]),
                        v
                        ),
            u
            )
    return b.formula(), b


def term_loop_nd():

    dim = 2

    transition_system = BranchingTransitionSystem(
        dim=dim,
        successors=successors_term_loop_nd
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_term_loop_nd,
        num_coefficients=4,
        num_params=2,
        num_partitions=3
    )

    return transition_system, template
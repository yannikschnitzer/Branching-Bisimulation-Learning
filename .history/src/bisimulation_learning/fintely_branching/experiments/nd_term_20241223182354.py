from bisimulation_learning.shared import *
from bisimulation_learning.deterministic.experiments.conditional_termination_succ_trees import bdt_term_loop_2

"""
Branching system termination

three states:
x > 1 can either loop into itself, or go in x = 0
x = 0 can only loop
x < -1 can only loop

while  x < -1 or x > 1  do
    x := x + if random and x > 1
        then +1
        else -1

"""

def successors_term_loop_nd(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    terminated = And(s[0] >= -1, s[0] <= 1)

    # if nondet = false
    succ_s_act_1[0] = If(terminated, 
        s[0], 
        s[0] - 1
    )

    # if nondet = true
    succ_s_act_2[0] = If(terminated, 
        s[0], 
        If(s[0] > 1, s[0] + 1, s[0] - 1)
    )

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - term-loop-nd-1
# 
# Labelling Function: x[0] > 1 or x[0] < -1 -> not-terminated
def bdt_term_loop_nd(params, x, num_params, partitions):
    assert(num_params > 1)
    u = BDTNodePoly([params[num_params]], x, params[0],
                        BDTLeave(partitions[0]), BDTLeave(partitions[1]))

    v = BDTNodePoly([params[num_params+1]], x, params[1],
                        BDTLeave(partitions[1]), BDTLeave(partitions[0]))

    b = BDTNodePoly(
        # x <= 1
        [RealVal(1)],x, RealVal(1), 
        # x <= 1 => might be terminated
        BDTNodePoly(
            # -x <= 1 <=> x >= -1
            [RealVal(-1)],x, RealVal(1), 
            # x >= -1 and x <= 1 => for sure terminated
            BDTLeave(partitions[2]),
            # x < -1 => for sure not terminated
            v
            ),
        # x > 1 => for sure non terminated
        u
        )
    return b.formula(), b


def term_loop_nd():

    dim = 1

    transition_system = BranchingTransitionSystem(
        dim=dim,
        successors=successors_term_loop_nd
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_term_loop_nd,
        num_coefficients=2,
        num_params=2,
        num_partitions=3
    )

    return transition_system, template


"""
P17 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P17(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    succ_s_act_1[0] = s[0] + 1

    succ_s_act_2[0] = If(s[0] <= 5, 
        1, 
        s[0] + 1
    )

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P17
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P17(params, x, num_params, partitions):
        b = BDTNodePoly([RealVal(1)],x, RealVal(5), 
                BDTNodePoly([params[num_params]], x, params[0],
                                BDTLeave(partitions[0]), BDTLeave(partitions[1])),
                BDTNodePoly([params[num_params+1]], x, params[1],
                                BDTLeave(partitions[2]), BDTLeave(partitions[3]))
                )
        return b.formula(), b
def P17():
    dim = 1

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P17
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P17,
        num_coefficients=2,
        num_params=2,
        num_partitions=4
    )

    return transition_system, template


"""
P18 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P18(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    succ_s_act_1[0] = s[0] + 1

    succ_s_act_2[0] = If(s[0] <= 5, 
        1, 
        s[0] + 1
    )

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P18
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P18(params, x, num_params, partitions):
        b = BDTNodePoly([RealVal(1)],x, RealVal(5), 
                BDTNodePoly([params[num_params]], x, params[0],
                                BDTLeave(partitions[0]), BDTLeave(partitions[1])),
                BDTNodePoly([params[num_params+1]], x, params[1],
                                BDTLeave(partitions[2]), BDTLeave(partitions[3]))
                )
        return b.formula(), b
def P18():
    dim = 1

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P18
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P18,
        num_coefficients=2,
        num_params=2,
        num_partitions=4
    )

    return transition_system, template

"""
Branching system termination (2)

three states:
x >= 3 can either loop into itself, or go in x > 0 and x < 3
x > 0 and x < 3 can only go into x <= 0
x <= 0 can only loop (terminated)

while x >= 1 do
    x := x + if random and x >= 3
        then +1
        else -1

"""
def successors_term_loop_nd_2(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    terminated = And(s[0] <= 0)

    # if random = false
    succ_s_act_1[0] = If(terminated, 
        s[0], 
        s[0] - 1
    )
    succ_s_act_1[1] = s[1]

    # if random = true
    succ_s_act_2[0] = If(terminated, 
        s[0], 
        If(s[0] >= 3, s[0] + 1, s[0] - 1)
    )
    succ_s_act_2[1] = s[1]

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - term-loop-nd-2
# 
# Labelling Function: x[0] <= 0 -> terminated, otherwise if x[0] < 3 -> will terminate eventually, otherwise: split
def bdt_term_loop_nd_2(params, x, num_params, partitions):

    b = BDTNodePoly(
        # x <= 0
        [RealVal(1),RealVal(0)],x, RealVal(0), 
        # x <= 0 => terminated
        BDTLeave(partitions[2]),
        BDTNodePoly([params[num_params], params[num_params+1]], x, params[0],
                        BDTLeave(partitions[0]), BDTLeave(partitions[1]))
        )
    return b.formula(), b

def term_loop_nd_2():

    dim = 2

    transition_system = BranchingTransitionSystem(
        dim=dim,
        successors=successors_term_loop_nd_2
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_term_loop_nd_2,
        num_coefficients=2,
        num_params=1,
        num_partitions=3
    )

    return transition_system, template

"""
Branching system termination (y)

three states:
x >= 3 can either loop into itself, or go in x > 0 and x < 3
x > 0 and x < 3 can only go into x <= 0
x <= 0 can only loop (terminated)

while x >= 1 do
    x := x + if random and x >= y
        then +1
        else -1

"""
def successors_term_loop_nd_y(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    terminated = Or(s[0] <= 0)

    # if random = false
    succ_s_act_1[0] = If(terminated, 
        s[0], 
        s[0] - 1
    )
    succ_s_act_1[1] = s[1]

    # if random = true
    succ_s_act_2[0] = If(terminated, 
        s[0], 
        If(s[0] >= s[1], s[0] + 1, s[0] - 1)
    )
    succ_s_act_2[1] = s[1]

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - term-loop-nd-2
# 
# Labelling Function: x[0] <= 0 -> terminated, otherwise if x[0] < 3 -> will terminate eventually, otherwise: split
def bdt_term_loop_nd_y(params, x, num_params, partitions):

    b = BDTNodePoly(
        # x <= 0
        [RealVal(1),RealVal(0)],x, RealVal(0), 
        # x <= 0 => terminated
        BDTLeave(partitions[2]),
        BDTNodePoly([params[num_params], params[num_params+1]], x, params[0],
                        BDTLeave(partitions[0]), BDTLeave(partitions[1]))
        )
    return b.formula(), b

def term_loop_nd_y():

    dim = 2

    transition_system = BranchingTransitionSystem(
        dim=dim,
        successors=successors_term_loop_nd_y
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_term_loop_nd_y,
        num_coefficients=2,
        num_params=1,
        num_partitions=3
    )

    return transition_system, template


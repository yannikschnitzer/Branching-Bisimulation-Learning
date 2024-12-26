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

    succ_s_act_2[0] = If(s[0] > 2, 
        2, 
        s[0]
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

def successors_robots(s):
    """
    The nondeterministic inputs are:
    id: the id of the robot to move
    a : the first transformation parameter
    b : the second transformation parameter
    """
    """
    We first fix a and b so that the program is simpler.
    """
    a = 1
    b = 1
    """
    We have to model the program in a way that it can learn by 
    itself to recognize the partition.

    That is: when encountering the "all robots in same place" state,
    it halts.
    """
    x_indexes = [0, 2, 4]
    y_indexes = [1, 3, 5]
    big_crash = And(
        [s[x_indexes[i]] == s[x_indexes[(i + 1) % 3]] for i in range(3)]
        + [s[y_indexes[i]] == s[y_indexes[(i + 1) % 3]] for i in range(3)]
    )
    # User decides which robot moves
    """
    Robot 1:
    x_1 := x_1 + 2a + b
    y_1 := y_1
    """
    robot_1 = [x for x in s]
    # robot_1[0] = s[0] + 2 * a + b
    robot_1[0] = If(big_crash, s[0], s[0] + 1)
    robot_1[1] = s[1]
    # x_2, y_2, x_3, y_3
    robot_1[2] = s[2]
    robot_1[3] = s[3]
    robot_1[4] = s[4]
    robot_1[5] = s[5]
    """
    Robot 2:
    x_2 := x_2 + a + b
    y_2 := y_2 - 2a - 2b
    """
    robot_2 = [x for x in s]
    robot_2[0] = s[0]
    robot_2[1] = s[1]
    # robot_2[2] = s[2] + a + b
    # robot_2[3] = s[3] - 2 * a - 2 * b
    robot_2[2] = If(big_crash, s[2], s[2] + 1)
    robot_2[3] = If(big_crash, s[3], s[3] - 2)
    robot_2[4] = s[4]
    robot_2[5] = s[5]
    """
    Robot 3:
    x_3 := x_3 + a + b
    y_3 := y_3 - a - b
    """
    robot_3 = [x for x in s]
    robot_3[0] = s[0]
    robot_3[1] = s[1]
    robot_3[2] = s[2]
    robot_3[3] = s[3]
    # robot_3[4] = s[4] + a + b
    # robot_3[5] = s[5] - a - b
    robot_3[4] = If(big_crash, s[4], s[4] + 1)
    robot_3[5] = If(big_crash, s[5], s[5] - 2)
    return [robot_1, robot_2, robot_3]

def bdt_robots(params, x, num_params, partitions):
    """
    The BDT for robots (safety) has to discern the three
    abstract states of interest:
    - 0 : the three robots are in the same position
    - 1 : at least two robots are in different positions
    - 2 : the three robots are in an impossible position

    The "impossible" position is such that robot_1 < robot_2,
    i.e. x_1 < x_2 + y_2
        [ that's the case since y_2 = -2 * x_2 and with chosen a an db
            x_1 >= 0 and x_2 >= 0, since they start as x_1 = 0 and x_2 = 0 ]
    so that with the initial values given in the source paper, the states
    in this region are unreachable.
    
    Basically our aim is to verify that 1 -/-> 0,
    other states relations are interest of another scope.

    We pilot manually the node for a state to be unreachable,
    the other node's parameters are to be learned and discern
    whether it's in 0 or 1.
    """
    b = BDTNodePoly(
        # r_2 <= r_1
        [RealVal(-1) ,RealVal(-1), RealVal(1), RealVal(1), RealVal(0), RealVal(0)], x, RealVal(0), 
        # True => check further
        BDTNodePoly(
            [params[num_params+i] for i in range(6)], x, params[0],
            BDTLeave(partitions[0]), 
            BDTLeave(partitions[1])
        ),
        # False => Unreachable state 
        BDTLeave(partitions[2])
        )
    return b.formula(), b

def robots():
    """
    Example taken from section 4 (Case Study 1) from the paper
    of Carelli and Grumberg.
    It features three concurrent robots that change their position
    each depending on a different linear transformation.
    """
    dim = 6
    trs = BranchingTransitionSystem(
        dim = dim,
        successors = successors_robots
    )
    tem = BDTTemplate(
        dim = dim,
        bdt_classifier = bdt_robots,
        num_params = 1,
        num_coefficients = 6,
        num_partitions = 3
    )
    return trs, tem
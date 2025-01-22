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
P1 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P1(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    # succ_s_act_1 just stays, corresponds to direct jump to loc5

    # 0 -> A, 1 -> R, 2 -> N
    succ_s_act_2[0] = 1
    succ_s_act_2[1] = If(s[2] > 0, s[1], 1)
    succ_s_act_2[2] = If(s[2] > 0, s[2] - 1, s[2])

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P1
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P1a(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1), 
                            BDTLeave(partitions[0]),
                            BDTLeave(partitions[1])
                    )
        return b.formula(), b

def bdt_P1(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1), 
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[0]),
                                BDTLeave(partitions[1]),
                            ),
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[2]), 
                                BDTNodePoly([params[num_params], params[num_params+1], params[num_params+2]], x, params[1],
                                    BDTLeave(partitions[3]), BDTLeave(partitions[4]))
                            )
                    )

        return b.formula(), b

def bdt_P1b(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1), 
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTNodePoly([params[num_params], params[num_params+1], params[num_params+2]], x, params[0],
                                    BDTLeave(partitions[0]), BDTLeave(partitions[1])
                                ),
                                BDTNodePoly([params[num_params+6], params[num_params+7], params[num_params+8]], x, params[2],
                                    BDTLeave(partitions[5]), BDTLeave(partitions[6]))
                            ),
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTNodePoly([params[num_params+3], params[num_params+4], params[num_params+5]], x, params[1],
                                    BDTLeave(partitions[3]), BDTLeave(partitions[4])), 
                                BDTNodePoly([params[num_params+9], params[num_params+10], params[num_params+11]], x, params[4],
                                    BDTLeave(partitions[7]), BDTLeave(partitions[8]))
                            )
                    )

        return b.formula(), b



def P1():
    dim = 3

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P1
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P1,
        num_coefficients=3,
        num_params=2,
        num_partitions=5
    )

    return transition_system, template

"""
P2 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P2(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    # succ_s_act_1 just stays, corresponds to direct jump to loc5
    
    # 0 -> A, 1 -> R, 2 -> N
    succ_s_act_2[0] = 1
    succ_s_act_2[1] = If(s[2] > 0, s[1], 1)
    succ_s_act_2[2] = If(s[2] > 0, s[2] - 1, s[2])

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P2
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P2(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(1), RealVal(0)],x, RealVal(5), 
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[0]),
                                BDTNodePoly([params[num_params], params[num_params+1], params[num_params+2]], x, params[0],
                                    BDTLeave(partitions[1]), BDTLeave(partitions[2]))
                            ),
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[3]), 
                                BDTLeave(partitions[4])
                            )
                    )

        return b.formula(), b



def P2():
    dim = 3

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P2
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P2,
        num_coefficients=3,
        num_params=1,
        num_partitions=5
    )

    return transition_system, template


"""
P3 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P3(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    # succ_s_act_1 just stays, corresponds to direct jump to loc5
    
    # 0 -> A, 1 -> R, 2 -> N
    succ_s_act_2[0] = If(s[0] == 1, 0, 1)
    succ_s_act_2[1] = If(s[1] == 1, 0, 1)
    succ_s_act_2[2] = s[2]

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P2
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P3(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1), 
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[0]),
                                BDTLeave(partitions[1])
                            ),
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[2]), 
                                BDTLeave(partitions[3])
                            )
                    )

        return b.formula(), b



def P3():
    dim = 3

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P3
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P3,
        num_coefficients=0,
        num_params=0,
        num_partitions=4
    )

    return transition_system, template

"""
P4 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P4(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true
    succ_s_act_3 = [v for v in s] # if random = true

    # succ_s_act_1 just stays, corresponds to direct jump to loc5
    
    # 0 -> A, 1 -> R, 2 -> N
    succ_s_act_2[0] = 1
    succ_s_act_2[1] = If(s[2] <= 0, 1, 0)
    succ_s_act_2[2] = s[2] - 1

    succ_s_act_3[0] = 1
    succ_s_act_3[1] = If(s[2] <= 0, 1, 0)
    succ_s_act_3[2] = s[2]

    return [succ_s_act_1, succ_s_act_2, succ_s_act_3]

# BDT Template - P2
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P4(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1), 
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[0]),
                                BDTNodePoly([params[num_params], params[num_params+1], params[num_params+2]], x, params[0],
                                    BDTLeave(partitions[1]), BDTLeave(partitions[2]))
                            ),
                            BDTNodePolyEquality([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[3]), 
                                BDTNodePoly([params[num_params+3], params[num_params+4], params[num_params+5]], x, params[1],
                                    BDTLeave(partitions[4]), BDTLeave(partitions[5]))
                            )
                    )

        return b.formula(), b



def P4():
    dim = 3

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P4
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P4,
        num_coefficients=6,
        num_params=2,
        num_partitions=6
    )

    return transition_system, template

"""
P5 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P5(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true
    
    # 0 -> I, 1 -> P, 2 -> S, 3 -> U
    succ_s_act_1[0] = If(s[0] < s[1], s[0], s[0] + 1)
    succ_s_act_1[1] = s[1]
    succ_s_act_1[2] = 1
    succ_s_act_1[3] = If(s[0] < s[1], 1, s[3])

    succ_s_act_2[0] = s[0]
    succ_s_act_2[1] = s[1]
    succ_s_act_2[2] = 1
    succ_s_act_2[3] = 1

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P2
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P5(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(0), RealVal(1)],x, RealVal(1), 
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[0]),
                                BDTLeave(partitions[1])
                            ),
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[2]), 
                                BDTNodePoly([params[num_params], params[num_params+1], params[num_params+2], params[num_params+3]], x, params[0],
                                    BDTLeave(partitions[3]), BDTLeave(partitions[4]))
                            )
                    )

        return b.formula(), b



def P5():
    dim = 4

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P5
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P5,
        num_coefficients=4,
        num_params=1,
        num_partitions=5
    )

    return transition_system, template


"""
P6 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P6(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true
    succ_s_act_3 = [v for v in s] # if random = true

    # 0 -> I, 1 -> P, 2 -> S, 3 -> U
    succ_s_act_1[0] = If(s[0] < s[1], s[0], s[0] + 1)
    succ_s_act_1[1] = s[1]
    succ_s_act_1[2] = 1
    succ_s_act_1[3] = If(s[0] < s[1], 1, s[3])

    succ_s_act_2[0] = s[0]
    succ_s_act_2[1] = s[1]
    succ_s_act_2[2] = 1
    succ_s_act_2[3] = 1

    succ_s_act_3[0] = s[0]
    succ_s_act_3[1] = s[1]
    succ_s_act_3[2] = 1
    succ_s_act_3[3] = s[3]

    return [succ_s_act_1, succ_s_act_2, succ_s_act_3]

# BDT Template - P6
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P6(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(0), RealVal(1)],x, RealVal(1), 
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[0]),
                                BDTLeave(partitions[1])
                            ),
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[2]), 
                                BDTLeave(partitions[3])
                            )
                    )

        return b.formula(), b



def P6():
    dim = 4

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P6
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P6,
        num_coefficients=0,
        num_params=0,
        num_partitions=4
    )

    return transition_system, template

"""
P7 from [Beyne et al. 2013] (same as P6)
See T2 repo.

"""
def successors_P7(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true
    succ_s_act_3 = [v for v in s] # if random = true

    # 0 -> I, 1 -> P, 2 -> S, 3 -> U
    succ_s_act_1[0] = If(s[0] < s[1], s[0], s[0] + 1)
    succ_s_act_1[1] = s[1]
    succ_s_act_1[2] = 1
    succ_s_act_1[3] = If(s[0] < s[1], 1, s[3])

    succ_s_act_2[0] = s[0]
    succ_s_act_2[1] = s[1]
    succ_s_act_2[2] = 1
    succ_s_act_2[3] = 1

    succ_s_act_3[0] = s[0]
    succ_s_act_3[1] = s[1]
    succ_s_act_3[2] = 1
    succ_s_act_3[3] = s[3]

    return [succ_s_act_1, succ_s_act_2, succ_s_act_3]

# BDT Template - P6
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P7(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(0), RealVal(1)],x, RealVal(1), 
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[0]),
                                BDTLeave(partitions[1])
                            ),
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[2]), 
                                BDTLeave(partitions[3])
                            )
                    )

        return b.formula(), b



def P7():
    dim = 4

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P7
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P7,
        num_coefficients=0,
        num_params=0,
        num_partitions=4
    )

    return transition_system, template

"""
P8 from [Beyne et al. 2013] (same as P6)
See T2 repo.

"""
def successors_P8(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    # 0 -> I, 1 -> P, 2 -> S, 3 -> U, 4 -> X
    succ_s_act_1[0] = If(s[0] < s[1], s[0], s[0] + 1)
    succ_s_act_1[1] = s[1]
    succ_s_act_1[2] = If(s[4] >= 1, 1, 0)
    succ_s_act_1[3] = If(s[4] >= 1, 0, 1)
    succ_s_act_1[4] = s[4]

    return [succ_s_act_1, succ_s_act_1]

# BDT Template - P6
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P8(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1), 
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0),RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[0]),
                                BDTLeave(partitions[1])
                            ),
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0), RealVal(0)],x, RealVal(1),
                                BDTLeave(partitions[2]), 
                                BDTLeave(partitions[3])
                            )
                    )

        return b.formula(), b

def bdt_P8(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(0), RealVal(1), RealVal(0)],x, RealVal(1), 
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0),RealVal(0)],x, RealVal(1),
                                BDTNodePoly([params[num_params], params[num_params+1], params[num_params+2],params[num_params+3],params[num_params+4]], x, params[0],
                                    BDTLeave(partitions[0]), BDTLeave(partitions[1])),
                                BDTNodePoly([params[num_params+5], params[num_params+6], params[num_params+7],params[num_params+8],params[num_params+9]], x, params[1],
                                    BDTLeave(partitions[2]), BDTLeave(partitions[3]))
                            ),
                            BDTNodePolyEquality([RealVal(0), RealVal(0), RealVal(1), RealVal(0),RealVal(0)],x, RealVal(1),
                                BDTNodePoly([params[num_params+10], params[num_params+11], params[num_params+12],params[num_params+13],params[num_params+14]], x, params[2],
                                    BDTLeave(partitions[4]), BDTLeave(partitions[5])), 
                                BDTNodePoly([params[num_params+15], params[num_params+16], params[num_params+17],params[num_params+18],params[num_params+19]], x, params[3],
                                    BDTLeave(partitions[6]), BDTLeave(partitions[7]))
                            )
                    )

        return b.formula(), b



def P8():
    dim = 5

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P8
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P8,
        num_coefficients=20,
        num_params=4,
        num_partitions=8
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
        b = BDTNodePoly([RealVal(1)],x, RealVal(1), 
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
P19 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P19(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    succ_s_act_1[0] = s[0] + 1

    succ_s_act_2[0] = If(And(s[0] <= 5, s[0] > 2), s[0] - 1, s[0] + 1)

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P18
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P19(params, x, num_params, partitions):
        b = BDTNodePoly([RealVal(1)],x, RealVal(1), 
                BDTNodePoly([params[num_params]], x, params[0],
                                BDTLeave(partitions[0]), BDTLeave(partitions[1])),
                BDTNodePoly([params[num_params+1]], x, params[1],
                                BDTLeave(partitions[2]), BDTLeave(partitions[3]))
                )
        return b.formula(), b
def P19():
    dim = 1

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P19
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P19,
        num_coefficients=2,
        num_params=2,
        num_partitions=4
    )

    return transition_system, template

"""
P20 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P20(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    succ_s_act_1[0] = If(s[0] < 0, s[0], s[0] + 1)

    succ_s_act_2[0] = If(s[0] < 0, s[0], 
                         If(s[0] > 5, s[0] + 1, 
                            If(s[0] > 2, s[0] - 1, s[0])))

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P18
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P20(params, x, num_params, partitions):
        b = BDTNodePoly([RealVal(1)],x, RealVal(1), 
                BDTNodePoly([params[num_params]], x, params[0],
                                BDTLeave(partitions[0]), BDTLeave(partitions[1])),
                BDTNodePoly([params[num_params+1]], x, params[1],
                                BDTLeave(partitions[2]), BDTLeave(partitions[3]))
                )
        return b.formula(), b
def P20():
    dim = 1

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P20
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P20,
        num_coefficients=2,
        num_params=2,
        num_partitions=4
    )

    return transition_system, template


"""
P21 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P21(s):
    succ_s_act_1 = [v for v in s] 
    succ_s_act_2 = [v for v in s] 

    succ_s_act_1[0] = 1 # W
    succ_s_act_1[1] = If(s[1] >= 1, 0, s[1]) # G
    
    return [succ_s_act_1]

# BDT Template - P20
# 
# Labelling Function: x[0] == 1;
def bdt_P21(params, x, num_params, partitions):
        b = BDTNodePoly([RealVal(1), RealVal(0)],x, RealVal(1), 
                        BDTNodePoly([RealVal(-1), RealVal(0)],x, RealVal(-1), 
                                    BDTLeave(partitions[0]),
                                    BDTNodePoly([params[num_params], params[num_params+1]], x, params[0],
                                        BDTLeave(partitions[1]), BDTLeave(partitions[2]))
                            ),
                        BDTNodePoly([params[num_params+2], params[num_params+3]], x, params[1],
                                BDTLeave(partitions[3]), BDTLeave(partitions[4])
                            )
                    )
        return b.formula(), b
def P21():
    dim = 2

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P21
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P21,
        num_coefficients=4,
        num_params=2,
        num_partitions=5
    )

    return transition_system, template

"""
P22 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P22(s):
    succ_s_act_1 = [v for v in s] 
    succ_s_act_2 = [v for v in s] 

    # W
    succ_s_act_1[0] = 0
    succ_s_act_2[0] = 1

    # G
    succ_s_act_1[1] = If(s[1] >= 1, 0, s[1])
    succ_s_act_2[1] = If(s[1] >= 1, 0, s[1])

    return [succ_s_act_1, succ_s_act_2] 


# BDT Template - P20
# 
# Labelling Function: x[0] == 1;
def bdt_P22(params, x, num_params, partitions):
        b = BDTNodePoly([RealVal(1), RealVal(0)],x, RealVal(1), 
                        BDTNodePoly([RealVal(-1), RealVal(0)],x, RealVal(-1), 
                                    BDTLeave(partitions[0]),
                                    BDTNodePoly([params[num_params], params[num_params+1]], x, params[0],
                                        BDTLeave(partitions[1]), BDTLeave(partitions[2]))
                            ),
                        BDTNodePoly([params[num_params+2], params[num_params+3]], x, params[1],
                                BDTLeave(partitions[3]), BDTLeave(partitions[4])
                            )
                    )
        return b.formula(), b
def P22():
    dim = 2

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P22
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P22,
        num_coefficients=4,
        num_params=2,
        num_partitions=5
    )

    return transition_system, template

"""
P23 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P23(s):
    succ_s_act_1 = [v for v in s] 
    succ_s_act_2 = [v for v in s] 

    # W
    succ_s_act_1[0] = If(s[1] < 1, If(s[0] >= 1, 0, s[0]), 1)
    succ_s_act_2[0] = If(s[1] < 1, If(s[0] >= 1, 0, s[0]), s[0])

    # G
    succ_s_act_1[1] = If(s[1] < 1, s[1], 0)
    succ_s_act_2[1] = If(s[1] < 1, s[1], 0)

    return [succ_s_act_1, succ_s_act_2] 


# BDT Template - P20
# 
# Labelling Function: x[0] == 1;
def bdt_P23(params, x, num_params, partitions):
        b = BDTNodePoly([RealVal(1), RealVal(0)],x, RealVal(1), 
                        BDTNodePoly([RealVal(-1), RealVal(0)],x, RealVal(-1), 
                                    BDTLeave(partitions[0]),
                                    BDTNodePoly([params[num_params], params[num_params+1]], x, params[0],
                                        BDTLeave(partitions[1]), BDTLeave(partitions[2]))
                            ),
                        BDTNodePoly([params[num_params+2], params[num_params+3]], x, params[1],
                                BDTLeave(partitions[3]), BDTLeave(partitions[4])
                            )
                    )
        return b.formula(), b

def P23():
    dim = 2

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P23
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P23,
        num_coefficients=4,
        num_params=2,
        num_partitions=5
    )

    return transition_system, template

"""
P24 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P24(s):
    succ_s_act_1 = [v for v in s] 
    succ_s_act_2 = [v for v in s] 
    succ_s_act_3 = [v for v in s] 

    # 0 -> W, 1 -> G
    succ_s_act_1[0] = If(s[0] > 0, 0, 1)
    succ_s_act_1[1] = 1

    succ_s_act_2[0] = If(s[0] > 0, 0, s[0])
    succ_s_act_2[1] = 1

    return [succ_s_act_1, succ_s_act_2, succ_s_act_3] 


# BDT Template - P20
# 
# Labelling Function: x[0] == 1;
def bdt_P24(params, x, num_params, partitions):
        b = BDTNodePolyEquality([RealVal(1), RealVal(0)],x, RealVal(1), 
                        BDTLeave(partitions[0]),
                        BDTLeave(partitions[1])
                    )
        return b.formula(), b

def P24():
    dim = 2

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P24
    )


    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P24,
        num_coefficients=0,
        num_params=0,
        num_partitions=2
    )

    return transition_system, template


"""
P25-27 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P25(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true
    
    # 0 -> C, 1 -> R, 2 -> CS
    succ_s_act_1[0] = If(s[2] <= 0, s[0], If(s[0] >= s[2], s[0] - 1, s[0]))
    succ_s_act_1[1] = If(s[2] <= 0, s[1], If(s[0] >= s[2], s[1] + 1, s[1]))
    succ_s_act_1[2] = If(s[2] <= 0, s[2], If(s[0] >= s[2], s[2] - 1, s[2]))

    succ_s_act_1[0] = s[0]
    succ_s_act_1[1] = s[1]
    succ_s_act_1[2] = If(s[2] <= 0, s[2], If(s[0] >= s[2], s[2] - 1, s[2]))

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P2
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P25(params, x, num_params, partitions):
        b = BDTNodePoly([RealVal(0), RealVal(1), RealVal(0)],x, RealVal(5), 
                            BDTNodePoly([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(5),
                                BDTLeave(partitions[0]),
                                BDTLeave(partitions[1])
                            ),
                            BDTNodePoly([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(5),
                                BDTLeave(partitions[2]), 
                                BDTLeave(partitions[3])
                            )
                    )

        return b.formula(), b

def P25():
    dim = 3

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P25
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P25,
        num_coefficients=0,
        num_params=0,
        num_partitions=4
    )

    return transition_system, template

"""
P28 from [Beyne et al. 2013]
See T2 repo.

"""
def successors_P28(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true
    
    # 0 -> C, 1 -> R, 2 -> CS
    succ_s_act_1[0] = If(Or(s[2] <= 0, s[0] > 5), s[0], If(s[0] >= s[2], s[0] - 1, s[0]))
    succ_s_act_1[1] = If(Or(s[2] <= 0, s[0] > 5), s[1], If(s[0] >= s[2], s[1] + 1, s[1]))
    succ_s_act_1[2] = If(Or(s[2] <= 0, s[0] > 5), s[2], If(s[0] >= s[2], s[2] - 1, s[2]))

    succ_s_act_1[0] = s[0]
    succ_s_act_1[1] = s[1]
    succ_s_act_1[2] = If(Or(s[2] <= 0, s[0] > 5), s[2], If(s[0] >= s[2], s[2] - 1, s[2]))

    return [succ_s_act_1, succ_s_act_2]

# BDT Template - P2
# 
# Labelling Function: x[0] >= 1, x[0] < 1
def bdt_P28(params, x, num_params, partitions):
        b = BDTNodePoly([RealVal(0), RealVal(1), RealVal(0)],x, RealVal(5), 
                            BDTNodePoly([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(5),
                                BDTLeave(partitions[0]),
                                BDTLeave(partitions[1])
                            ),
                            BDTNodePoly([RealVal(1), RealVal(0), RealVal(0)],x, RealVal(5),
                                BDTLeave(partitions[2]), 
                                BDTLeave(partitions[3])
                            )
                    )

        return b.formula(), b

def P28():
    dim = 3

    transition_system = BranchingTransitionSystem(
        dim,
        successors = successors_P28
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_P28,
        num_coefficients=0,
        num_params=0,
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

def successors_quadratic_nd(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    terminated = Or(s[0] <= 0, s[0] > 1000)

    # if random = false
    succ_s_act_1[0] = If(terminated, 
        s[0], 
        s[0] + 1
    )
    succ_s_act_1[1] = s[1]

    # if random = true
    succ_s_act_2[0] = If(terminated, 
        s[0], 
        s[0] * s[0]
    )
    succ_s_act_2[1] = s[1]

    return [succ_s_act_1, succ_s_act_2]

def quadratic_nd():

    dim = 2

    transition_system = BranchingTransitionSystem(
        dim=dim,
        successors=successors_quadratic_nd
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_quadratic,
        num_coefficients=2,
        num_params=1,
        num_partitions=3
    )

    return transition_system, template

def successors_cubic_nd(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    terminated = Or(s[0] <= 0, s[0] > 10000)

    # if random = false
    succ_s_act_1[0] = If(terminated, 
        s[0], 
        s[0] + 1
    )
    succ_s_act_1[1] = s[1]

    # if random = true
    succ_s_act_2[0] = If(terminated, 
        s[0], 
        s[0] * s[0] * s[0] * 4 + s[0] * s[0] * 2 + s[0] + 1
    )
    succ_s_act_2[1] = s[1]

    return [succ_s_act_1, succ_s_act_2]

def cubic_nd():

    dim = 2

    transition_system = BranchingTransitionSystem(
        dim=dim,
        successors=successors_cubic_nd
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_cubic,
        num_coefficients=2,
        num_params=1,
        num_partitions=3
    )

    return transition_system, template

def successors_nlr_cond_nd(s):
    succ_s_act_1 = [v for v in s] # if random = false
    succ_s_act_2 = [v for v in s] # if random = true

    terminated = And(s[0] * s[0] * s[0] > 100)

    # if random = false
    succ_s_act_1[0] = If(terminated, 
        s[0], 
        s[0] + 1
    )
    succ_s_act_1[1] = s[1]

    # if random = true
    succ_s_act_2[0] = If(terminated, 
        s[0], 
        s[0] * s[0] * s[0] * 4 + s[0] * s[0] * 2 + s[0] + 1
    )
    succ_s_act_2[1] = s[1]

    return [succ_s_act_1, succ_s_act_2]

def nlr_cond_nd():

    dim = 2

    transition_system = BranchingTransitionSystem(
        dim=dim,
        successors=successors_nlr_cond_nd
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_nlr_cond,
        num_coefficients=2,
        num_params=1,
        num_partitions=3
    )

    return transition_system, template


"""
Branching system termination (y)

three states:
x >= y can either loop into itself, or go in x > 0 and x < y
x > 0 and x < y can only go into x <= 0
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

def successors_robots_ab(s,a=0,b=1):
    """
    The nondeterministic inputs are:
    id: the id of the robot to move
    a : the first transformation parameter
    b : the second transformation parameter
    """
    """
    We first fix a and b so that the program is simpler
    (i.e. we assume the user will always input those values)
    """

    """
    We have to model the program in a way that it can learn by 
    itself to recognize the partition.

    That is: when encountering the "all robots in same place" state,
    it halts.
    """
    x_indexes = [0, 2, 4]
    y_indexes = [1, 3, 5]
    all_crash = And(
        s[0] == s[2], s[2] == s[4], s[4] == s[0],
        s[1] == s[3], s[3] == s[5], s[5] == s[1]
    )
    # User decides which robot moves
    """
    Robot 1:
    x_1 := x_1 + 2a + b
    y_1 := y_1
    """
    robot_1 = [x for x in s]
    # robot_1[0] = s[0] + 2 * a + b
    robot_1[0] = If(all_crash, robot_1[0], robot_1[0] + 1)
    robot_1[1] = s[1]
    # x_2, y_2, x_3, y_3
    """
    Robot 2:
    x_2 := x_2 + a + b
    y_2 := y_2 - 2a - 2b
    """
    robot_2 = [x for x in s]
    # robot_2[2] = s[2] + a + b
    # robot_2[3] = s[3] - 2 * a - 2 * b
    robot_2[2] = If(all_crash, robot_2[2], robot_2[2] + 1)
    robot_2[3] = If(all_crash, robot_2[3], robot_2[3] - 2)
    """
    Robot 3:
    x_3 := x_3 + a + b
    y_3 := y_3 - a - b
    """
    robot_3 = [x for x in s]
    # robot_3[4] = s[4] + a + b
    # robot_3[5] = s[5] - a - b
    robot_3[4] = If(all_crash, robot_3[4], robot_3[4] + 1)
    robot_3[5] = If(all_crash, robot_3[5], robot_3[5] - 1)
    return [robot_1, robot_2, robot_3]

#     a_vals = [-1,0,1]
#     b_vals = [-1,0,1]
def successors_robots(s, a_vals = [-10,-2,-1,0,1,2,10], b_vals = [-10,-2,-1,0,1,2,10]):

    succs = []
    for a in a_vals:
        for b in b_vals:
            succs += successors_robots_ab(s,a,b)

    return succs

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
        [RealVal(-1), RealVal(-1), RealVal(1), RealVal(1), RealVal(0), RealVal(0)], x, RealVal(0), 
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

def successors_two_robots(s):
    succ_move_robot_1 = [x for x in s]
    succ_move_robot_2 = [x for x in s]
    clash = And(s[0] == IntVal(0), s[1] == IntVal(0))
    # robot 1 walks only horizontally E -> W on x axis (i.e. y_1 == 0)
    # its position variable is just s[0] (X axis)
    succ_move_robot_1[0] = If(clash, s[0], s[0] + 1)
    # robot 2 walks only vertically S -> N on y axis (i.e. x_2 == 0)
    # its position variable is just s[1] (Y axis)
    succ_move_robot_2[1] = If(clash, s[1], s[1] + 1)
    return [succ_move_robot_1, succ_move_robot_2]

def bdt_two_robots(params, x, num_params, partitions):
    """
    The BDT for robots (safety) has to discern the three
    abstract states of interest:
    - 0 : two robots are in the same position (x_1 == 0 && y_2 == 0)
    - 1 : the two robots can clash (x_1 <= 0 && y_2 <= 0)
    - 2 : the two robots cannot clash (otherwise)
    """
    # b = BDTNodePolyEquality(
    #     # y_2 == 0
    #     [RealVal(0), RealVal(0), RealVal(1)], x, RealVal(0), 
    #     BDTNodePolyEquality(
    #         # x_1 == x_2
    #         [RealVal(1), RealVal(-1), 0], x, RealVal(0),
    #         BDTLeave(partitions[0]),
    #         BDTNodePoly(
    #             [params[num_params+3],params[num_params+4],params[num_params+5]], x, params[1],
    #             BDTLeave(partitions[1]),
    #             BDTLeave(partitions[2])
    #         )
    #     ),
    #     # y_2 != 0
    #     BDTNodePoly(
    #         # y_2 > 0
    #         [RealVal(0), RealVal(0), RealVal(-1)], x, RealVal(0),
    #         BDTLeave(partitions[1]),
    #         # y_2 < 0
    #         BDTNodePoly(
    #             [params[num_params],params[num_params+1],params[num_params+2]], x, params[0],
    #             BDTLeave(partitions[1]),
    #             BDTLeave(partitions[2])
    #         )
    #     )
    #     # or just BDTNodePoly 1 / 2
    # )
    b = BDTNodePoly(
        # y_2 <= 0
        [RealVal(0), RealVal(1)], x, RealVal(0), 
        BDTNodePoly(
            # x_1 <= 0
            [RealVal(1), RealVal(0)], x, RealVal(0),
            BDTNodePoly(
                [params[num_params],params[num_params+1]], x, params[0],
                BDTLeave(partitions[1]),
                BDTLeave(partitions[2])
            ),
            BDTLeave(partitions[0]) # G safe
        ),
        # y_2 > 0
        BDTLeave(partitions[0]) # G safe
    )
    return b.formula(), b

def two_robots():
    """
    Semplification of the example taken from section 4 (Case Study 1) from the paper
    of Carelli and Grumberg.
    It features two concurrent robots that change their position
    depending on a different linear transformation.
    """
    dim = 2
    trs = BranchingTransitionSystem(
        dim = dim,
        successors = successors_two_robots
    )
    tem = BDTTemplate(
        dim = dim,
        bdt_classifier = bdt_two_robots,
        num_params = 1,
        num_coefficients = 2,
        num_partitions = 3
    )
    return trs, tem

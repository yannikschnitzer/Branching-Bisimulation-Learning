from z3 import *
from bisimulation_learning.shared import *
from bisimulation_learning.deterministic.experiments.clock_synchronization_succ_trees import *
import bisimulation_learning.deterministic.experiments.clock_synchronization_succ_trees as exp_sync

def get_domain(n, con = False):
    def domain(x):
        up = 2 if con and n == 10 else 2.5
        dom = [ [0, n],
                [0, int(n * up)]]
        return And([simplify(
            And(x[i] >= dom[i][0], x[i] <= dom[i][1])
        ) for i in range(len(dom))])
    return domain

def tte_sf(n):
    successor  = getattr(exp_sync, f"successor_tte_sf_{n}")
    classifier = getattr(exp_sync, f"bdt_tte_{n}")
        
    trs = DeterministicTransitionSystem(
        dim = 2,
        domain=get_domain(n),
        successor=successor
    )
    tem = BDTTemplate(
        dim = 2,
        bdt_classifier=classifier,
        num_params=1,
        num_coefficients=2,
        num_partitions=3
    )
    return trs.to_branching(), tem

def tte_usf(n):
    successor  = getattr(exp_sync, f"successor_tte_usf_{n}")
    classifier = getattr(exp_sync, f"bdt_tte_{n}")
        
    trs = DeterministicTransitionSystem(
        dim = 2,
        domain=get_domain(n),
        successor=successor
    )
    tem = BDTTemplate(
        dim = 2,
        bdt_classifier=classifier,
        num_params=1,
        num_coefficients=2,
        num_partitions=3
    )
    return trs.to_branching(), tem


def con_sf(n):
    successor  = getattr(exp_sync, f"successor_con_sf_{n}")
    classifier = getattr(exp_sync, f"bdt_con_{n}")
        
    trs = DeterministicTransitionSystem(
        dim = 2,
        domain=get_domain(n, con=True),
        successor=successor
    )
    tem = BDTTemplate(
        dim = 2,
        bdt_classifier=classifier,
        num_params=1,
        num_coefficients=2,
        num_partitions=3
    )
    return trs.to_branching(), tem


def con_usf(n):
    successor  = getattr(exp_sync, f"successor_con_usf_{n}")
    classifier = getattr(exp_sync, f"bdt_con_{n}")
        
    trs = DeterministicTransitionSystem(
        dim = 2,
        domain=get_domain(n, con=True),
        successor=successor
    )
    tem = BDTTemplate(
        dim = 2,
        bdt_classifier=classifier,
        num_params=1,
        num_coefficients=2,
        num_partitions=3
    )
    return trs.to_branching(), tem

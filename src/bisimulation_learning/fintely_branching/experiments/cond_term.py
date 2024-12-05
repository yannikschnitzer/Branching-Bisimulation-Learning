
from bisimulation_learning.deterministic.experiments import *


def term_loop_2():

    dim = 2

    transition_system = DeterminsticTransitionSystem(
        dim=dim,
        successor=successor_term_loop_2
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_term_loop_2,
        num_coefficients=2,
        num_params=1,
        num_partitions=3
    )

    return transition_system, template

def euclid():
    ts = DeterminsticTransitionSystem(
        dim=2,
        domain=domain,
        successor=successor_euclid
    )

    qs = BDTTemplate(
        dim=2,
        bdt_classifier=bdt_euclid,
        num_params=2,
        num_coefficients=4,
        num_partitions=3
    )
    return ts, qs


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

    return transition_system.to_branching(), template

def audio_compr():
    ts = DeterministicTransitionSystem(
        dim = 1,
        successor=successor_audio_compr
    )

    tem = BDTTemplate(
        dim=1,
        bdt_classifier=bdt_audio_compr,
        num_params=1,
        num_coefficients=1,
        num_partitions=3
    )

    return ts.to_branching(), tem

def euclid():
    ts = DeterministicTransitionSystem(
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
    return ts.to_branching(), qs

def greater():
    ts = DeterministicTransitionSystem(
        dim=2,
        successor=successor_greater
    )
    tem = BDTTemplate(
        bdt_classifier=bdt_greater,
        dim=2,
        num_params=1,
        num_coefficients=2,
        num_partitions=3
    )
    return ts.to_branching(), tem

def smaller():
    trs = DeterministicTransitionSystem(
        dim=2,
        successor=successor_smaller
    )

    tem = BDTTemplate(
        bdt_classifier=bdt_smaller,
        num_params=1,
        num_coefficients=2,
        num_partitions=3,
        dim=2
    )

    return trs.to_branching(), tem
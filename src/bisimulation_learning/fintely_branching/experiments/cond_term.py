
from bisimulation_learning.deterministic.experiments import *

def term_loop_1():

    dim = 1

    transition_system = DeterministicTransitionSystem(
        dim=dim,
        successor=successor_term_loop_1
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_term_loop_1,
        num_coefficients=1,
        num_params=1,
        num_partitions=3
    )

    return transition_system.to_branching(), template

def term_loop_2():

    dim = 2

    transition_system = DeterministicTransitionSystem(
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

def conic():
    trs = DeterministicTransitionSystem(
        dim=2,
        successor=successor_conic
    )
    tem = BDTTemplate(
        bdt_classifier=bdt_conic,
        num_params=2,
        num_coefficients=4,
        num_partitions=3,
        dim=2
    )
    return trs.to_branching(), tem

def disjunction():
    trs = DeterministicTransitionSystem(
        dim=3,
        successor=successor_disjunction
    )
    tem = BDTTemplate(
        bdt_classifier=bdt_disjunction,
        num_params=1,
        num_coefficients=3,
        num_partitions=3,
        dim=3
    )
    return trs.to_branching(), tem


def parallel():
    trs = DeterministicTransitionSystem(
        dim=2,
        successor=successor_parallel
    )
    tem = BDTTemplate(
        bdt_classifier=bdt_parallel,
        num_params=2,
        num_coefficients=4,
        num_partitions=3,
        dim=2
    )
    return trs.to_branching(), tem

def quadratic():
    trs = DeterministicTransitionSystem(
        dim=1,
        successor=successor_quadratic
    )
    tem = BDTTemplate(
        bdt_classifier=bdt_quadratic,
        num_params=2,
        num_coefficients=2,
        num_partitions=4,
        dim=1
    )
    return trs.to_branching(), tem

def cubic():
    trs = DeterministicTransitionSystem(
        dim=1,
        successor=successor_cubic
    )
    tem = BDTTemplate(
        bdt_classifier=bdt_cubic,
        num_params=2,
        num_coefficients=2,
        num_partitions=4,
        dim=1
    )
    return trs.to_branching(), tem

def nlr_cond():
    trs = DeterministicTransitionSystem(
        dim=1,
        successor=successor_nlr_cond
    )
    tem = BDTTemplate(
        bdt_classifier=bdt_nlr_cond,
        num_params=2,
        num_coefficients=2,
        num_partitions=4,
        dim=1
    )
    return trs.to_branching(), tem

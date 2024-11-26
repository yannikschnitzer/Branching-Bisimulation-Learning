from bl_solver.one_shot_solver import *

from conditional_termination_succ_trees import *

def domain(x):
    return True

def term_loop_1():
    def domain(x):
        """
            Domain bounding x[1] to be a boolean (not-terminated / terminated)
        """
        return simplify(And(x[1] >= 0 , x[1] <= 1))
    dim = 2

    transition_system = TransitionSystem(
        dim=dim,
        successor=nd_successor_term_loop_1,
        domain=domain
    )

    template = QuotientSystem(
        dim=dim,
        bdt_classifier=bdt_term_loop_1,
        num_coefficients=2,
        num_params=2,
        num_partitions=3
    )

    return transition_system, template

def term_loop_2():

    dim = 2

    transition_system = TransitionSystem(
        dim=dim,
        successor=nd_successor_term_loop_2,
        domain=domain
    )

    template = QuotientSystem(
        dim=dim,
        bdt_classifier=bdt_term_loop_2,
        num_coefficients=2,
        num_params=1,
        num_partitions=3
    )

    return transition_system, template

def audio_compr():
    dim = 1

    transition_system = TransitionSystem(
        dim=dim,
        successor=nd_successor_audio_compr,
        domain=domain
    )

    template = QuotientSystem(
        dim=dim,
        bdt_classifier=bdt_audio_compr,
        num_coefficients=1,
        num_params=1,
        num_partitions=3
    )

    return transition_system, template


def run(constructor):
    ts, t = constructor()
    res, (theta, gamma, eta) = one_shot(ts, t)
    print(f"""
    Found theta = {theta}
    Found gamma = {gamma}
    Found eta   = {eta}
    """)

if __name__ == "__main__":
    # run(term_loop_2)
    run(audio_compr)

    
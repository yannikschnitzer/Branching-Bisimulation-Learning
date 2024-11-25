from bl_solver.bisimulation_learning import *

from conditional_termination_succ_trees import successor_term_loop_1, bdt_term_loop_1

if __name__ == "__main__":

    def domain(x):
        """
            Domain bounding x[1] to be a boolean (not-terminated / terminated)
        """
        return simplify(And(x[1] >= 0 , x[1] <= 1))

    transition_system = TransitionSystem(
        dim=2,
        successor=nd_successor_term_loop_1,
        domain=domain
    )

    abstract_system = AbstractSystem(
        bdt_classifier=bdt_term_loop_1,
        num_coefficients=2,
        num_params=2,
        num_partitions=3
    )

    bisimulation_learning(transition_system, abstract_system)
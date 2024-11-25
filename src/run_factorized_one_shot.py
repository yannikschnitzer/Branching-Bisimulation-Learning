from bl_solver.one_shot_solver import *

from conditional_termination_succ_trees import nd_successor_term_loop_1, bdt_term_loop_1

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

    template = ProposedTemplate(
        dim=transition_system.dim,
        abstract_system=abstract_system
    )

    res, (theta, gamma, eta) = one_shot(
        transition_system,
        abstract_system,
        template)
    print(f"""
    Found theta = {theta}
    Found gamma = {gamma}
    Found eta   = {eta}
    """)
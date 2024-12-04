
from bl_solver.bisimulation_learning import *
from conditional_termination_experiments import *
from conditional_termination_succ_trees import *

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

def visualize_template(theta, t: BDTTemplate):

    exp = Experiment(
        classifier=t.bdt_classifier,
        name="Default Name",
        num_coefficients=t.num_coefficients,
        num_initial=10,
        num_params=t.num_params,
        num_partitions=t.num_partitions,
        successor=None,
        dim=None,
        domain=None
    )
    visualize(theta, exp, 0.2, save = False)

if __name__ == "__main__":
    ts, t = term_loop_2()
    theta, eta = branching_bisimulation_learning(ts.to_branching(), t, iters=100)
    
    print(f"""
    theta = {theta},
    eta   = {eta} 
    """)
    visualize_template(theta, t)
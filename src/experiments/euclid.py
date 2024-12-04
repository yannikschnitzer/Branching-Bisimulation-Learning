
from bl_solver.bisimulation_learning import *
from conditional_termination_experiments import *
from conditional_termination_succ_trees import *

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

if __name__ == "__main__":
    ts, t = euclid()
    theta, eta = branching_bisimulation_learning(ts.to_branching(), t, iters=100)
    
    print(f"""
    theta = {theta},
    eta   = {eta} 
    """)
    visualize_template(theta, t)
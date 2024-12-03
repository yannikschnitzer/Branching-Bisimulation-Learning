from bl_solver.one_shot_solver import *

from conditional_termination_succ_trees import *

from visualization import *

def domain(x):
    return True

def term_loop_1():
    def domain(x):
        """
            Domain bounding x[1] to be a boolean (not-terminated / terminated)
        """
        return simplify(And(x[1] >= 0 , x[1] <= 1))
    dim = 2

    transition_system = DeterminsticTransitionSystem(
        dim=dim,
        successor=nd_successor_term_loop_1,
        domain=domain
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_term_loop_1,
        num_coefficients=2,
        num_params=2,
        num_partitions=3
    )

    return transition_system, template

def term_loop_2():

    dim = 2

    transition_system = DeterminsticTransitionSystem(
        dim=dim,
        successor=successor_term_loop_2,
        domain=domain
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_term_loop_2,
        num_coefficients=2,
        num_params=1,
        num_partitions=3
    )

    return transition_system, template

def draw_template(gamma, t: BDTTemplate):

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
    draw_quotient(gamma, exp)

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

def audio_compr():
    dim = 1

    transition_system = DeterminsticTransitionSystem(
        dim=dim,
        successor=successor_audio_compr,
        domain=domain
    )

    template = BDTTemplate(
        dim=dim,
        bdt_classifier=bdt_audio_compr,
        num_coefficients=1,
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

def run(constructor, allow_branching=False):
    ts, t = constructor()
    res = False
    params = None
    if allow_branching:
        res, params = one_shot_namjoshi(ts.to_branching(), t)
    else:
        res, params = one_shot_deterministic(ts, t)
    if res:
        (theta, gamma, eta) = params
        print(f"""
        Found theta = {theta}
        Found gamma = {gamma}
        Found eta   = {eta}
        """)

        draw_template(gamma, t)
        visualize_template(theta, t)
    else:
        print("No condition found!")

if __name__ == "__main__":
    # run(term_loop_2, allow_branching=True)
    run(audio_compr, allow_branching=True)
    # run(euclid, allow_branching=True)

    
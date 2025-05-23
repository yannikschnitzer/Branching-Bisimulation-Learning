from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *
from bisimulation_learning.shared import *
from bisimulation_learning.deterministic.experiments.conditional_termination_experiments import *

def run_and_show(trs, tem):
    theta, eta = bisimulation_learning(trs, tem, iters=100, explicit_classes=True)
    gamma = compute_adjacency_matrix(trs, tem, theta)
    draw_quotient(gamma, "Default Name")
    visualize_branching(theta, tem)

def run_and_print(trs, tem: BDTTemplate, expl: False):
    theta, eta = bisimulation_learning(trs, tem, iters=1000, explicit_classes=expl)
    print(f"""
    theta = {theta},
    eta   = {eta} 
    """)
    gamma = compute_adjacency_matrix(trs, tem, theta)
    for p in range(len(gamma)):
        for q in range(len(gamma[p])):
            if gamma[p][q]:
                print(f"{p}->{q}")
    
    formula, tree = tem.bdt_classifier(theta, tem.m, tem.num_params, tem.partitions)
    from z3 import simplify
    print(f"{simplify(formula)}")
    
    

if __name__ == "__main__":
    # trs, tem = conic()
    # trs, tem = disjunction()
    # trs, tem = parallel()
    # trs, tem = euclid()
    # trs, tem = tte_sf(1000)
    # trs, tem = tte_usf(2000)
    # trs, tem = con_sf(10)
    # trs, tem = con_usf(10)
    # trs, tem = term_loop_nd()
    # trs, tem = term_loop_nd_2()
    # trs, tem = term_loop_nd_y()
    # trs, tem = term_loop_nd_y()
    # trs, tem = P2()
    # trs, tem = two_robots_axis()
    # trs, tem = two_robots_axis_actions()
    trs, tem = two_robots_axis_actions_quadratic()
    # two_robots doesn't work
    # trs, tem = two_robots()
    # trs, tem = quadratic_nd()
    run_and_print(trs, tem, expl=True)
    # run_and_show(trs, tem)
    # for i in range(10):
    #     trs, tem = P5()
    #     run_and_print(trs, tem, expl = True)

    
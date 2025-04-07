from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.one_shot_solver import *
from bisimulation_learning.shared import *

def run_and_show(trs, tem):
    theta, eta = solve_one_shot(trs, tem, explicit_classes=False)
    
    print(f"""
    theta = {theta},
    eta   = {eta} 
    """)
    gamma = compute_adjacency_matrix(trs, tem, theta)
    draw_quotient(gamma, "Default Name")
    visualize_branching(theta, tem)


if __name__ == "__main__":
    # trs, tem = cubic()
    # trs, tem = euclid()
    # trs, tem = tte_sf(1000)
    # trs, tem = term_loop_nd()
    # trs, tem = term_loop_nd_2()
    trs, tem = term_loop_nd_y()
    run_and_show(trs, tem)
    
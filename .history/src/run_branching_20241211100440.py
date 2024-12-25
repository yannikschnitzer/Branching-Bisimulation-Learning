from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *
from bisimulation_learning.shared import *

import time

def run_and_show(trs, tem):
    theta, eta = bisimulation_learning(trs, tem, iters=30, explicit_classes=True)
    
    print(f"""
    theta = {theta},
    eta   = {eta} 
    """)
    gamma = compute_adjacency_matrix(trs, tem, theta)
    draw_quotient(gamma, "Default Name")
    visualize_branching(theta, tem)


if __name__ == "__main__":
    # trs, tem = cubic()
    
    trs, tem = euclid()
    #trs, tem = tte_sf(10)

    time = time.time_ns()
    run_and_show(trs, tem)

     time2 = time.time_ns()

    print("Time: ")
    
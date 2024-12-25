from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *
from bisimulation_learning.shared import *

import time

def run_and_show(trs, tem):
    start_time = time.time()
    theta, eta = bisimulation_learning(trs, tem, iters=1000, explicit_classes=True)
    
    print("--- %s seconds ---" % (time.time() - start_time))

    print(f"""
    theta = {theta},
    eta   = {eta} 
    """)
    gamma = compute_adjacency_matrix(trs, tem, theta)
    draw_quotient(gamma, "Default Name")
    visualize_branching(theta, tem)


if __name__ == "__main__":
    trs, tem = larger()
    
    #trs, tem = euclid()
    #trs, tem = tte_sf(10000)

    run_and_show(trs, tem)
    
from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *
from bisimulation_learning.shared import *


constructor = term_loop_2
# constructor = euclid

if __name__ == "__main__":
    ts, t = constructor()
    ts = ts.to_branching()
    theta, eta = bisimulation_learning(ts, t, iters=10)
    
    print(f"""
    theta = {theta},
    eta   = {eta} 
    """)
    gamma = compute_adjacency_matrix(ts, t, theta)
    draw_quotient(gamma, "Default Name")
    visualize_branching(theta, t)
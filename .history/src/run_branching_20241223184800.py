from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *
from bisimulation_learning.shared import *
    

def run_and_show(trs, tem):
    theta, eta = bisimulation_learning(trs, tem, iters=100, explicit_classes=True)
    gamma = compute_adjacency_matrix(trs, tem, theta)
    draw_quotient(gamma, "Default Name")
    visualize_branching(theta, tem)

def run_and_print(trs, tem: BDTTemplate):
    theta, eta = bisimulation_learning(trs, tem, iters=100, explicit_classes=True)
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
    for i in range(10):
        trs, tem = con_sf(10)
    # trs, tem = con_usf(10)
    # trs, tem = term_loop_nd()
    # trs, tem = term_loop_nd_2()
    # trs, tem = term_loop_nd_y()
    # run_and_show(trs, tem)
        print("======")
    #trs, tem = robots()
        run_and_print(trs, tem)
    
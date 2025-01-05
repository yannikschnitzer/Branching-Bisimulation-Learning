from argparse import ArgumentParser
import time
import numpy as np

from bisimulation_learning.shared import *
from bisimulation_learning.deterministic.experiment_runner import *
from bisimulation_learning.deterministic.experiments import *
from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *

experiments = [
#     term_loop_nd,
#     term_loop_nd_2,
#    # term_loop_nd_y,
#     P17,
#     P18,
    P4
]

experiments_robot = [
    robots
]

def compute_branching_abstract_system(trs, tem, explicit_classes):
    theta, eta = bisimulation_learning(trs, tem, 1000, explicit_classes)
    gamma = compute_adjacency_matrix(trs, tem, theta)

def compare_times(branching, iters = 10):
    trs, tem = branching()
    branching_times_impl = []
    for i in range(iters):
        branching_start_time = time.time()
        compute_branching_abstract_system(trs, tem, False)
        branching_end_time = time.time()
        branching_times_impl.append(branching_end_time - branching_start_time)
        print(f"--- Branching Implicit Formula {i}: {branching_times_impl[-1]}s expired ")
    brn_avg = np.average(branching_times_impl)
    brn_std = np.std(branching_times_impl)
    print(f"--- Branching Implicit Formulas - Average expired time is {brn_avg}s - STD: {brn_std}")

    trs, tem = branching()
    branching_times_expl = []
    for i in range(iters):
        branching_start_time = time.time()
        compute_branching_abstract_system(trs, tem, True)
        branching_end_time = time.time()
        branching_times_expl.append(branching_end_time - branching_start_time)
        print(f"--- Branching Explicit Formula {i}: {branching_times_expl[-1]}s expired ")
    brn_avg = np.average(branching_times_expl)
    brn_std = np.std(branching_times_expl)
    print(f"--- Branching Explicit Formulas - Average expired time is {brn_avg}s - STD: {brn_std}")

    return brn_avg

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog = "Branching Bisimulation Learning - Deterministic Benchmarks",
        description = "Runs iteratively all the deterministic examples with branching and deterministic approaches comparing time averages.",
        epilog = "Copyright?"
    )
    arg_parser.add_argument("-i", "--iters")
    arg_parser.add_argument("-g", "--global-rank", action="store_true") # store_true means that if not given, counts as False
    arg_parser.add_argument("-o", "--output-file")
    args = arg_parser.parse_args()
    
    iters = args.iters or 10 # default iterations is 10
    iters = int(iters)
    explicit_classes = not args.global_rank
    if explicit_classes:
        print(f"Running with {iters} iters with a ranking function for each partition")
    else:
        print(f"Running with {iters} iters with a global ranking function")

    output_file = args.output_file

    for branching in experiments:
        print(f"Running experiment {str(branching)}")
        brn_avg = compare_times(branching, iters)
        print(f"End experiment {str(branching)}\n")
        if output_file is not None:
            with open(output_file, 'a') as out:
                out.write(f"{brn_avg} \\\\\n")

    
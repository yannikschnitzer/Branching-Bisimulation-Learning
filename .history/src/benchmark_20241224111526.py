from argparse import ArgumentParser
import time
import numpy as np

from bisimulation_learning.shared import *
from bisimulation_learning.deterministic.experiment_runner import *
from bisimulation_learning.deterministic.experiments import *
from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *

experiments = [
    (con_sf(10), con_),
    (term_loop_2, exp_term_loop_2),
    (audio_compr, exp_audio_compr),
    (euclid, exp_euclid),
    (greater, exp_greater),
    (smaller, exp_smaller)
]

def compute_branching_abstract_system(trs, tem, explicit_classes):
    theta, eta = bisimulation_learning(trs, tem, 100, explicit_classes)
    gamma = compute_adjacency_matrix(trs, tem, theta)

def compare_times(branching, deterministic, iters = 10, explicit_classes = True):
    trs, tem = branching()
    times = []
    for i in range(iters):
        branching_start_time = time.time()
        compute_branching_abstract_system(trs, tem, explicit_classes)
        branching_end_time = time.time()
        times.append(branching_end_time - branching_start_time)
        print(f"--- Branching Formula {i}: {times[-1]}s expired ")
    
    print(f"--- Branching Formulas - Average expired time is {np.average(times)}s")

    times = []
    for i in range(iters):
        branching_start_time = time.time()
        run_experiment(deterministic())
        branching_end_time = time.time()
        times.append(branching_end_time - branching_start_time)
        print(f"--- Deterministic Formula {i}: {times[-1]}s expired ")

    print(f"--- Deterministic Formulas - Average expired time is {np.average(times)}s")


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog = "Branching Bisimulation Learning - Deterministic Benchmarks",
        description = "Runs iteratively all the deterministic examples with branching and deterministic approaches comparing time averages.",
        epilog = "Copyright?"
    )
    arg_parser.add_argument("-i", "--iters")
    arg_parser.add_argument("-g", "--global-rank", action="store_true") # store_true means that if not given, counts as False
    args = arg_parser.parse_args()
    
    iters = args.iters or 10 # default iterations is 10
    explicit_classes = not args.global_rank
    if explicit_classes:
        print(f"Running with {iters} iters with a ranking function for each partition")
    else:
        print(f"Running with {iters} iters with a global ranking function")

    for (branching, deterministic) in experiments:
        experiment = deterministic()
        print(f"Running experiment {experiment.name}")
        compare_times(branching, deterministic, iters, explicit_classes)
        print(f"End experiment {experiment.name}")

    
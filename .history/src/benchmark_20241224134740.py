from argparse import ArgumentParser
import time
import numpy as np

from bisimulation_learning.shared import *
from bisimulation_learning.deterministic.experiment_runner import *
from bisimulation_learning.deterministic.experiments import *
from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *


experiments = [
    (tte_sf(10), exp_tte_sf_10),
    (tte_sf(100), exp_tte_sf_100),
    (tte_sf(1000), exp_tte_sf_1000),
    (tte_sf(2000), exp_tte_sf_2000),
    (tte_sf(5000), exp_tte_sf_5000),
    (tte_sf(10000), exp_tte_sf_10000),
    (tte_usf(10), exp_tte_usf_10),
    (tte_usf(100), exp_tte_usf_100),
    (tte_usf(1000), exp_tte_usf_1000),
    (tte_usf(2000), exp_tte_usf_2000),
    (tte_usf(5000), exp_tte_usf_5000),
    (tte_usf(10000), exp_tte_usf_10000),
    (con_sf(10), exp_con_sf_10),
    (con_sf(100), exp_con_sf_100),
    (con_sf(1000), exp_con_sf_1000),
    (con_sf(2000), exp_con_sf_2000),
    (con_sf(5000), exp_con_sf_5000),
    (con_sf(10000), exp_con_sf_10000),
   (con_usf(10), exp_con_usf_10),
    (con_usf(100), exp_con_usf_100),
   (con_usf(1000), exp_con_usf_1000),
    (con_usf(2000), exp_con_usf_2000),
    (con_usf(5000), exp_con_usf_5000),
    (con_usf(10000), exp_con_usf_10000)
]

def compute_branching_abstract_system(trs, tem, explicit_classes):
    theta, eta = bisimulation_learning(trs, tem, 1000, explicit_classes)
    gamma = compute_adjacency_matrix(trs, tem, theta)

def compare_times(branching, deterministic, iters = 10, explicit_classes = True):
    trs, tem = branching
    branching_times = []
    for i in range(iters):
        branching_start_time = time.time()
        compute_branching_abstract_system(trs, tem, explicit_classes)
        branching_end_time = time.time()
        branching_times.append(branching_end_time - branching_start_time)
        print(f"--- Branching Formula {i}: {branching_times[-1]}s expired ")
    brn_avg = np.average(branching_times)
    print(f"--- Branching Formulas - Average expired time is {brn_avg}s")

        trs, tem = branching
    branching_times = []
    for i in range(iters):
        branching_start_time = time.time()
        compute_branching_abstract_system(trs, tem, explicit_classes)
        branching_end_time = time.time()
        branching_times.append(branching_end_time - branching_start_time)
        print(f"--- Branching Formula {i}: {branching_times[-1]}s expired ")
    brn_avg = np.average(branching_times)
    print(f"--- Branching Formulas - Average expired time is {brn_avg}s")

    deterministic_times = []
    exp = deterministic()
    for i in range(iters):
        branching_start_time = time.time()
        run_experiment(exp)
        branching_end_time = time.time()
        deterministic_times.append(branching_end_time - branching_start_time)
        print(f"--- Deterministic Formula {i}: {deterministic_times[-1]}s expired ")
    det_avg = np.average(deterministic_times)
    print(f"--- Deterministic Formulas - Average expired time is {det_avg}s")
    return exp.name, brn_avg, det_avg

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

    for (branching, deterministic) in experiments:
        experiment = deterministic()
        print(f"Running experiment {experiment.name}")
        name, brn_avg, det_avg = compare_times(branching, deterministic, iters, explicit_classes)
        print(f"End experiment {experiment.name}")
        if output_file is not None:
            with open(output_file, 'a') as out:
                out.write(f"{name}  & {det_avg} & {brn_avg} \\\\\n")

    
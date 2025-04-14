from argparse import ArgumentParser
import time
import numpy as np
import pandas as pd

from bisimulation_learning.shared import *
# from bisimulation_learning.deterministic.experiment_runner import *
from bisimulation_learning.deterministic.experiments import *
from bisimulation_learning.fact_det.experiments import *
from bisimulation_learning.fact_det.cegis_solver import *
set_param('smt.random_seed', 42)

term_experiments = [
    exp_term_loop_1(),
    exp_term_loop_2(),
    exp_audio_compr(),
    exp_euclid(),
    exp_greater(),
    exp_smaller(),
    exp_conic(),
    exp_disjunction(),
    exp_parallel(),
    exp_quadratic(),
    exp_cubic(),
    exp_nlr_cond()
]

all_experiments = [
    exp_term_loop_1(),
    exp_term_loop_2(),
    exp_audio_compr(),
    exp_euclid(),
    exp_greater(),
    exp_smaller(),
    exp_conic(),
    exp_disjunction(),
    exp_parallel(),
    exp_quadratic(),
    exp_cubic(),
    exp_nlr_cond(),
    exp_tte_sf_10(),
    exp_tte_sf_100(),
    exp_tte_sf_1000(),
    exp_tte_sf_2000(),
    exp_tte_sf_5000(),
    exp_tte_sf_10000(),
    exp_tte_usf_10(),
    exp_tte_usf_100(),
    exp_tte_usf_1000(),
    exp_tte_usf_2000(),
    exp_tte_usf_5000(),
    exp_tte_usf_10000(),
    exp_con_sf_10(),
    exp_con_sf_100(),
    exp_con_sf_1000(),
    exp_con_sf_2000(),
    exp_con_sf_5000(),
    exp_con_sf_10000(),
    exp_con_usf_10(),
    exp_con_usf_100(),
    exp_con_usf_1000(),
    exp_con_usf_2000(),
    exp_con_usf_5000(),
    exp_con_usf_10000()
]

def compute_branching_abstract_system(trs, tem, explicit_classes):
    theta, eta = bisimulation_learning(trs, tem, 1000, explicit_classes)
    gamma = compute_adjacency_matrix(trs, tem, theta)

def compare_times(exp, iters = 10, explicit_classes = True, verbose = False):

    deterministic_times = []
    for i in range(iters):
        branching_start_time = time.time()
        run_experiment(exp)
        branching_end_time = time.time()
        deterministic_times.append(branching_end_time - branching_start_time)
        if verbose:
            print(f"--- Deterministic Formula {i}: {deterministic_times[-1]}s expired ")
    det_avg = np.average(deterministic_times)
    det_std = np.std(deterministic_times)
    print(f"--- Deterministic Formulas - Average expired time is {det_avg}s - STD: {det_std}")
    return exp.name, det_avg, det_std

def run_experiments(experiments, iters = 10, timeout = 500, global_rank = False, verbose=False):
    df = pd.DataFrame(columns=["Experiment", "Avg", "STD"])
    for experiment in experiments:
        print(f"Running experiment {experiment.name}")
        try:
            name, det_avg, det_std = compare_times(experiment, iters, not global_rank, verbose=verbose)
            print(f"End experiment {experiment.name}\n")
            df.loc[len(df)] = [name, det_avg, det_std]
        except Exception as e:
            print(f"Experiment {experiment.name} had an error: {e}")
            df.loc[len(df)] = [experiment.name, "error", ""]
    return df

def run_smoke_test():
    run_experiments([exp_term_loop_1()], iters=1, timeout = 10, global_rank=False, verbose = True)

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
    iters = int(iters)
    explicit_classes = not args.global_rank
    if explicit_classes:
        print(f"Running with {iters} iters with a ranking function for each partition")
    else:
        print(f"Running with {iters} iters with a global ranking function")

    df = run_experiments(all_experiments, iters)

    df.to_csv("deterministic_bl.csv")

    

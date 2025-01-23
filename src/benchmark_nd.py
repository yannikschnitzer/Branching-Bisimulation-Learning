from argparse import ArgumentParser
import time
import numpy as np
import pandas as pd

from bisimulation_learning.shared import *
from bisimulation_learning.deterministic.experiment_runner import *
from bisimulation_learning.deterministic.experiments import *
from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *

experiments = [
    # (term_loop_1(), "term_loop_1"),
    # (term_loop_2(), "term_loop_2"),
    # (audio_compr(), "audio_compr"),
    # (euclid(), "euclid"),
    # (greater(), "greater"),
    # (smaller(), "smaller"),
    # (conic(), "conic"),
    # (disjunction(), "disjunction"),
    # (parallel(), "parallel"),
    # (quadratic(), "quadratic"),
    # (cubic(), "cubic"),
    # (nlr_cond(), "nlr_cond"),

    # (tte_sf(10), "tte_sf_10"),
    # (tte_sf(100), "tte_sf_100"),
    # (tte_sf(1000), "tte_sf_1000"),
    # (tte_sf(2000), "tte_sf_2000"),
    # (tte_sf(5000), "tte_sf_5000"),
    # (tte_sf(10000), "tte_sf_10000"),

    # (tte_usf(10), "tte_usf_10"),
    # (tte_usf(100), "tte_usf_100"),
    # (tte_usf(1000), "tte_usf_1000"),
    # (tte_usf(2000), "tte_usf_2000"),
    # (tte_usf(5000), "tte_usf_5000"),
    # (tte_usf(10000), "tte_usf_10000"),
    # (con_sf(10), "con_sf_10"),
    # (con_sf(100), "con_sf_100"),
    # (con_sf(1000), "con_sf_1000"),
    # (con_sf(2000), "con_sf_2000"),
    # (con_sf(5000), "con_sf_5000"),
    # (con_sf(10000), "con_sf_10000"),

    # (con_usf(10), "con_usf_10"),
    # (con_usf(100), "con_usf_100"),
    # (con_usf(1000), "con_usf_1000"),
    # (con_usf(2000), "con_usf_2000"),
    # (con_usf(5000), "con_usf_5000"),
    # (con_usf(10000), "con_usf_10000"),


    # (term_loop_nd(), "term_loop_nd"),
    # (term_loop_nd_2(), "term_loop_nd_2"),
    # (term_loop_nd_y(), "term_loop_nd_y"),
    (quadratic_nd(), "quadratic_nd"),
    (cubic_nd(), "cubic_nd"),
    (nlr_cond_nd(), "nlr_cond_nd"),
    # (P1(), "P1"),
    # (P2(), "P2"),
    # (P3(), "P3"),
    # (P4(), "P4"),
    # (P5(), "P5"),
    # (P6(), "P6"),
    # (P7(), "P7"),
    # (P17(), "P17"),
    # (P18(), "P18"),
    # (P19(), "P19"),
    # (P20(), "P20"),
    # (P21(), "P21"),
    # (P25(), "P25"),
]

experiments_robot = [
    robots
]

def compute_branching_abstract_system(trs, tem, explicit_classes):
    theta, eta = bisimulation_learning(trs, tem, 1000, explicit_classes)
    gamma = compute_adjacency_matrix(trs, tem, theta)

def compare_times(exp, iters = 10):
    trs, tem = exp
    branching_times_impl = []
    for i in range(iters):
        try:
            branching_start_time = time.time()
            compute_branching_abstract_system(trs, tem, False)
            branching_end_time = time.time()
            branching_times_impl.append(branching_end_time - branching_start_time)
            if verbose:
                print(f"--- Branching Implicit Formula {i}: {branching_times_impl[-1]}s expired ")
        except Exception as e:
            print(f"--- Branching Implicit Formula {i} error: {e}")
    impl_avg = np.average(branching_times_impl)
    impl_std = np.std(branching_times_impl)
    print(f"--- Branching Implicit Formulas - Average expired time is {impl_avg}s - STD: {impl_std}")

    branching_times_expl = []
    for i in range(iters):
        try:
            branching_start_time = time.time()
            compute_branching_abstract_system(trs, tem, True)
            branching_end_time = time.time()
            branching_times_expl.append(branching_end_time - branching_start_time)
            if verbose:
                print(f"--- Branching Explicit Formula {i}: {branching_times_expl[-1]}s expired ")
        except Exception as e:
            print(f"--- Branching Explicit Formula {i} error: {e}")
    expl_avg = np.average(branching_times_expl)
    expl_std = np.std(branching_times_expl)
    print(f"--- Branching Explicit Formulas - Average expired time is {expl_avg}s - STD: {expl_std}")

    return (impl_avg, impl_std, expl_avg, expl_std)

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog = "Branching Bisimulation Learning - Deterministic Benchmarks",
        description = "Runs iteratively all the deterministic examples with branching and deterministic approaches comparing time averages.",
        epilog = "Copyright?"
    )
    arg_parser.add_argument("-i", "--iters")
    arg_parser.add_argument("-g", "--global-rank", action="store_true") # store_true means that if not given, counts as False
    arg_parser.add_argument("-v", "--verbose", action="store_true")
    args = arg_parser.parse_args()
    
    iters = args.iters or 10 # default iterations is 10
    iters = int(iters)
    verbose = args.verbose
    explicit_classes = not args.global_rank
    if explicit_classes:
        print(f"Running with {iters} iters with a ranking function for each partition")
    else:
        print(f"Running with {iters} iters with a global ranking function")


    df = pd.DataFrame(columns=["Experiment", "Monolithic Avg", "Monolithic STD", "Piecewise Avg", "Piecewise STD"])
    for exp, name in experiments:
        try:
            print(f"Running experiment {name}")
            impl_avg, impl_std, expl_avg, expl_std = compare_times(exp, iters)
            print(f"End experiment {name}\n")
            df.loc[len(df)] = [name, impl_avg, impl_std, expl_avg, expl_std]
        except Exception as e:
            print(f"Experiment {name} unexpected error: {e}")
    
    df.to_csv("benchmarks_bl_br.csv")

    
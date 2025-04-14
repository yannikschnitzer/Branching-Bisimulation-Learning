from argparse import ArgumentParser
import time
import signal # we are on unix
import numpy as np
import pandas as pd

from bisimulation_learning.shared import *
from bisimulation_learning.deterministic.experiment_runner import *
from bisimulation_learning.deterministic.experiments import *
from bisimulation_learning.fintely_branching.experiments import *
from bisimulation_learning.fintely_branching.cegis_solver import *

term_experiments = [
    (term_loop_1(), "term_loop_1"),
    (term_loop_2(), "term_loop_2"),
    (audio_compr(), "audio_compr"),
    (euclid(), "euclid"),
    (greater(), "greater"),
    (smaller(), "smaller"),
    (conic(), "conic"),
    (disjunction(), "disjunction"),
    (parallel(), "parallel"),
    (quadratic(), "quadratic"),
    (cubic(), "cubic"),
    (nlr_cond(), "nlr_cond")
]

term_loop_nd_exps = [
    (term_loop_nd(), "term_loop_nd"),
    (term_loop_nd_2(), "term_loop_nd_2"),
    (term_loop_nd_y(), "term_loop_nd_y")
]

cond_term_nd_exps = [
    (quadratic_nd(), "quadratic_nd"),
    (cubic_nd(), "cubic_nd"),
    (nlr_cond_nd(), "nlr_cond_nd"),
    # (conic_nd(), "conic_nd"),
    # (disjunction_nd(), "disjunction_nd"),
]

robot_exps = [
    (two_robots_axis(), "two_robots_axis"),
    (two_robots_axis_actions(), "two_robots_axis_actions"),
    (two_robots_axis_actions_quadratic(), "two_robots_axis_actions_quadratic")
]

industrial_exps = [
    (P1(), "P1"),
    (P2(), "P2"),
    (P3(), "P3"),
    (P4(), "P4"),
    (P5(), "P5"),
    (P6(), "P6"),
    (P7(), "P7"),
    (P17(), "P17"),
    (P18(), "P18"),
    (P19(), "P19"),
    (P20(), "P20"),
    (P21(), "P21"),
    # (P22(), "P22"),
    # (P23(), "P23"),
    # (P24(), "P24"),
    (P25(), "P25"),
    # (P28(), "P28"),

]

nd_inf_experiments = [
    *term_loop_nd_exps,
    *cond_term_nd_exps,
    *industrial_exps,
    *robot_exps
]

t2_experiments = [
    *term_loop_nd_exps,
    *industrial_exps,
    (P28(), "P28"),
]


nd_fin_experiments = [
    *term_loop_nd_exps,
    *industrial_exps
]

all_experiments = [
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
    # (quadratic_nd(), "quadratic_nd"),
    # (cubic_nd(), "cubic_nd"),
    # (nlr_cond_nd(), "nlr_cond_nd"),
    # (conic_nd(), "conic_nd"),
    # (disjunction_nd(), "disjunction_nd"),
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
    # (P22(), "P22"),
    # (P23(), "P23"),
    # (P24(), "P24"),
    # (P25(), "P25"),
    # (P28(), "P28"),
    # (two_robots_axis(), "two_robots_axis"),
    # (two_robots_axis_actions(), "two_robots_axis_actions"),
    # (two_robots_axis_actions_quadratic(), "two_robots_axis_actions_quadratic"),
]

experiments_robot = [
    robots
]

def timeout_handler(signum, frame):
    raise Exception("Timeout occurred.")

def compute_branching_abstract_system(trs, tem, explicit_classes, verbose=False):
    theta, eta = bisimulation_learning(trs, tem, 1000, explicit_classes)
    gamma = compute_adjacency_matrix(trs, tem, theta)
    if verbose : print("Theta:", theta, "Eta:", eta, "Adjacency Matrix:", gamma)
    #visualize_branching(theta, tem)

def compare_times(exp, iters = 10, verbose=False):
    trs, tem = exp
    branching_times_impl = []
    for i in range(iters):
        try:
            branching_start_time = time.time()
            compute_branching_abstract_system(trs, tem, False, verbose and i == iters-1)
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
            compute_branching_abstract_system(trs, tem, True, verbose and i == iters-1)
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

def run_bisimulation_learning_experiment(exp, explicit_classes = True, iters = 10, timeout = 300, verbose=False):
    trs, tem = exp
    branching_times_impl = []
    for i in range(iters):
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)
            branching_start_time = time.time()
            compute_branching_abstract_system(trs, tem, explicit_classes, verbose and i == iters-1)
            signal.alarm(0)
            branching_end_time = time.time()
            branching_times_impl.append(branching_end_time - branching_start_time)
            if verbose:
                print(f"--- Branching Implicit Formula {i}: {branching_times_impl[-1]}s expired ")
        except Exception as e:
            print(f"--- Branching Implicit Formula {i} error: {e}")
    avg = np.average(branching_times_impl)
    std = np.std(branching_times_impl)
    print(f"--- Branching Implicit Formulas - Average expired time is {avg}s - STD: {std}")
    return avg, std

def run_experiments(experiments, explicit_classes, iters = 10, timeout = 300, verbose=False):
    df = pd.DataFrame(columns=["Experiment", "Avg", "STD"])
    for exp, name in experiments:
        try:
            print(f"Running experiment {name}")
            avg, std = run_bisimulation_learning_experiment(exp, explicit_classes, iters, timeout, verbose=verbose)
            print(f"End experiment {name}\n")
            df.loc[len(df)] = [name, avg, std]
        except Exception as e:
            print(f"Experiment {name} unexpected error: {e}")
    return df

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
    for exp, name in all_experiments:
        try:
            print(f"Running experiment {name}")
            impl_avg, impl_std, expl_avg, expl_std = compare_times(exp, iters, verbose = verbose)
            print(f"End experiment {name}\n")
            df.loc[len(df)] = [name, impl_avg, impl_std, expl_avg, expl_std]
        except Exception as e:
            print(f"Experiment {name} unexpected error: {e}")
    
    df.to_csv("benchmarks_bl_br.csv")

    
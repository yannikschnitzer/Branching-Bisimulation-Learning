"""
    Runs the CPAChecker baseline experiments.
"""
import numpy as np
import pandas as pd
from cpa.CPA_runner import *

__author__ = "Yannik Schnitzer"
__copyright__ = "Copyright 2024, Yannik Schnitzer"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "yannik.schnitzer@cs.ox.ac.uk"
__status__ = "Experimental - Artifact Evaluation"

def run_cpa_smoketest():
    run_cpa_experiment(exp_term_loop_1_term())

def run_cpa_experiments():
    run_cpa_experiment(exp_term_loop_1_term())
    run_cpa_experiment(exp_term_loop_1_nonterm())
    run_cpa_experiment(exp_term_loop_2_term())
    run_cpa_experiment(exp_term_loop_2_nonterm())
    run_cpa_experiment(exp_audio_compr_term())
    run_cpa_experiment(exp_audio_compr_nonterm())
    run_cpa_experiment(exp_euclid_term())
    run_cpa_experiment(exp_euclid_nonterm())
    run_cpa_experiment(exp_greater_term())
    run_cpa_experiment(exp_greater_nonterm())
    run_cpa_experiment(exp_smaller_term())
    run_cpa_experiment(exp_smaller_nonterm())
    run_cpa_experiment(exp_conic_term())
    run_cpa_experiment(exp_conic_nonterm())
    run_cpa_experiment(exp_disjunction_term())
    run_cpa_experiment(exp_parallel_term())
    run_cpa_experiment(exp_quadratic_term())
    run_cpa_experiment(exp_cubic_term())
    run_cpa_experiment(exp_cubic_nonterm())
    run_cpa_experiment(exp_nlr_cond_term())
    run_cpa_experiment(exp_nlr_cond_nonterm())

def exp_term_loop_1_term():
    exp = CPA_Experiment(
        "term-loop-1-term",
        "term-loop-1-term.c"
    )
    return exp

def exp_term_loop_1_nonterm():
    exp = CPA_Experiment(
        "term-loop-1-nonterm",
        "term-loop-1-nonterm.c"
    )
    return exp

def exp_term_loop_2_term():
    exp = CPA_Experiment(
        "term-loop-2-term",
        "term-loop-2-term.c"
    )
    return exp

def exp_term_loop_2_nonterm():
    exp = CPA_Experiment(
        "term-loop-2-nonterm",
        "term-loop-2-nonterm.c"
    )
    return exp

def exp_audio_compr_term():
    exp = CPA_Experiment(
        "audio-compr-term",
        "audio_compression-term.c",
        print_res=True
    )
    return exp

def exp_audio_compr_nonterm():
    exp = CPA_Experiment(
        "audio-compr-nonterm",
        "audio_compression-nonterm.c",
        True
    )
    return exp

def exp_euclid_term():
    exp = CPA_Experiment(
        "euclid-term",
        "euclid-term.c",
        print_res=True
    )
    return exp

def exp_euclid_nonterm():
    exp = CPA_Experiment(
        "euclid-nonterm",
        "euclid-nonterm.c"
    )
    return exp

def exp_greater_term():
    exp = CPA_Experiment(
        "greater-term",
        "greater-term.c"
    )
    return exp

def exp_greater_nonterm():
    exp = CPA_Experiment(
        "greater-nonterm",
        "greater-nonterm.c"
    )
    return exp

def exp_smaller_term():
    exp = CPA_Experiment(
        "smaller-term",
        "smaller-term.c"
    )
    return exp

def exp_smaller_nonterm():
    exp = CPA_Experiment(
        "smaller-nonterm",
        "smaller-nonterm.c"
    )
    return exp

def exp_conic_term():
    exp = CPA_Experiment(
        "conic-term",
        "conic-term.c"
    )
    return exp

def exp_conic_nonterm():
    exp = CPA_Experiment(
        "conic-nonterm",
        "conic-nonterm.c"
    )
    return exp

def exp_disjunction_term():
    exp = CPA_Experiment(
        "disjunction-term",
        "disjunction-term.c"
    )
    return exp

def exp_parallel_term():
    exp = CPA_Experiment(
        "parallel-term",
        "parallel.c"
    )
    return exp

def exp_quadratic_term():
    exp = CPA_Experiment(
        "quadratic-term",
        "quadratic.c",
        print_res=True
    )
    return exp

def exp_cubic_term():
    exp = CPA_Experiment(
        "cubic-term",
        "cubic-term.c",
        print_res=True
    )
    return exp


def exp_cubic_nonterm():
    exp = CPA_Experiment(
        "cubic-nonterm",
        "cubic-nonterm.c",
        print_res=True
    )
    return exp


def exp_nlr_cond_term():
    exp = CPA_Experiment(
        "nlr-cond-term",
        "non-linear-cond-term.c",
        print_res=True
    )
    return exp

def exp_nlr_cond_nonterm():
    exp = CPA_Experiment(
        "nlr-cond-nonterm",
        "non-linear-cond-nonterm.c",
        print_res=True
    )
    return exp

term_experiments = [
    exp_term_loop_1_term(),
    exp_term_loop_2_term(),
    exp_audio_compr_term(),
    exp_euclid_term(),
    exp_greater_term(),
    exp_smaller_term(),
    exp_conic_term(),
    exp_disjunction_term(),
    exp_parallel_term(),
    exp_quadratic_term(),
    exp_cubic_term(),
    exp_nlr_cond_term(),
]

nonterm_experiments = [
    exp_term_loop_1_nonterm(),
    exp_term_loop_2_nonterm(),
    exp_audio_compr_nonterm(),
    exp_euclid_nonterm(),
    exp_greater_nonterm(),
    exp_smaller_nonterm(),
    exp_conic_nonterm(),
    exp_cubic_nonterm(),
    exp_nlr_cond_nonterm()
]

all_experiments = [
    exp_term_loop_1_term(),
    exp_term_loop_1_nonterm(),
    exp_term_loop_2_term(),
    exp_term_loop_2_nonterm(),
    exp_audio_compr_term(),
    exp_audio_compr_nonterm(),
    exp_euclid_term(),
    exp_euclid_nonterm(),
    exp_greater_term(),
    exp_greater_nonterm(),
    exp_smaller_term(),
    exp_smaller_nonterm(),
    exp_conic_term(),
    exp_conic_nonterm(),
    exp_disjunction_term(),
    exp_parallel_term(),
    exp_quadratic_term(),
    exp_cubic_term(),
    exp_cubic_nonterm(),
    exp_nlr_cond_term(),
    exp_nlr_cond_nonterm()
]

def run_cpa_experiment_iters(experiments, iters = 10, timeout=300):
    df = pd.DataFrame(columns=["Experiment", "Average", "STD"])
    for experiment in experiments:
        avg = None
        std = None
        try:
            times = []
            for _ in range(iters):
                runtime = run_cpa_experiment(experiment)
                times.append(runtime)
            avg = np.average(times)
            std = np.std(times)
        except Exception as e:
            print(f"Experiment {experiment.name} failed one iteration: {e}")
            avg = str(e)
            std = ""
        df.loc[len(df)] = [experiment.name, avg, std]
    return df

if __name__ == "__main__":
    df = run_cpa_experiment_iters(all_experiments)
    df.to_csv("cpa-benchmarks.csv")
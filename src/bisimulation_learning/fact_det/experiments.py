import numpy as np
import pandas as pd

import time
from bisimulation_learning.fact_det.cegis_solver import run_bisimulation_learning
from bisimulation_learning.deterministic.experiments import *
import bisimulation_learning.shared as shr

cond_term_experiments = [
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

clock_sync_experiments = [
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
    exp_con_usf_10000(),

]

def run_experiment(exp: shr.Experiment, iters, verbose):
    trs, tem = shr.experiment_to_dts(exp)
    times = []
    for i in range(iters):
        start = time.time()
        theta, gamma, eta = run_bisimulation_learning(trs, tem)
        stop  = time.time()
        if theta is not None:
            times.append(stop - start)
        else:
            print(f"theta, gamma, eta are None: '{theta}', '{gamma}', '{eta}'")
    avg = np.average(times)
    std = np.std(times)
    return avg, std


def run_cond_term_experiments(iters = 10, verbose = False):
    run_experiments(cond_term_experiments, "det_bl_cond_term", iters, verbose)

def run_clock_sync_experiments(iters = 10, verbose = False):
    run_experiments(clock_sync_experiments, "det_bl_clock_sync", iters, verbose)

def run_experiments(experiments, filename, iters = 10, verbose = False):
    df = pd.DataFrame(columns=['Experiment', 'Average', 'STD'])
    for exp in experiments:
        try:
            avg, std = run_experiment(exp, iters, verbose)
            print(f"Experiment {exp.name} avg = {avg}, std = {std}")
            df.loc[len(df)] = [exp.name, avg, std]
        except Exception as e:
            print(f"An exeception occurred running experiment {exp.name}: Reason = {e}")
    df.to_csv(f'{filename}.csv')
    

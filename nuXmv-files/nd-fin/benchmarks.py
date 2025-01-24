from argparse import ArgumentParser
import subprocess
import time
import re
import os
import numpy as np
import pandas as pd

# nuxmv -source chech-inf-state.scr P19.smv

experiments = [
    # {
    #     'experiment': "term-loop-nd.smv",
    #     'formulas': "term-loop-nd.ctl"
    # },
    # {
    #     'experiment': "term-loop-nd-2.smv",
    #     'formulas': "term-loop-nd-2.ctl"
    # },
    # {
    #     'experiment': "term-loop-nd-y.smv",
    #     'formulas': "term-loop-nd-y.ctl"
    # },
    # {
    #     'experiment': "quadratic-nd.smv",
    #     'formulas': "quadratic-nd.ctl"
    # },
    # {
    #     'experiment': "cubic-nd.smv",
    #     'formulas': "cubic-nd.ctl"
    # },
    # {
    #     'experiment': "nlr-cond-nd.smv",
    #     'formulas': "nlr-cond-nd.ctl"
    # },
    # {
    #     'experiment': "P1.smv",
    #     'formulas': "P1.ctl"
    # },
    # {
    #     'experiment': "P2.smv",
    #     'formulas': "P2.ctl"
    # },
    # {
    #     'experiment': "P3.smv",
    #     'formulas': "P3.ctl"
    # },
    # {
    #     'experiment': "P4.smv",
    #     'formulas': "P4.ctl"
    # },
    # {
    #     'experiment': "P5.smv",
    #     'formulas': "P5.ctl"
    # },
    # {
    #     'experiment': "P6.smv",
    #     'formulas': "P6.ctl"
    # },
    # {
    #     'experiment': "P7.smv",
    #     'formulas': "P7.ctl"
    # },
    # {
    #     'experiment': "P17.smv",
    #     'formulas': "P17.ctl"
    # },
    # {
    #     'experiment': "P18.smv",
    #     'formulas': "P18.ctl"
    # },
    # {
    #     'experiment': "P19.smv",
    #     'formulas': "P19.ctl"
    # },
    # {
    #     'experiment': "P20.smv",
    #     'formulas': "P20.ctl"
    # },
    # {
    #     'experiment': "P21.smv",
    #     'formulas': "P21.ctl"
    # },
    {
        'experiment': "P25.smv",
        'formulas': "P25.ctl"
    },
]

def run_nuxmv_experiment(exp: str) -> bytes:
    cmd = f"nuxmv -source check-inf-state.scr {exp}"
    outb = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, timeout=500)
    return outb

def measure_nuxmv_experiment(exp: str, formula_idx: int, formula: str):
    file_to_check = f"{formula_idx}-{exp}"
    ctl_footer = f"    ctlSPEC {formula}"
    cmd = f"""
    rm -f "{file_to_check}" \\
        && cat "{exp}" >> "{file_to_check}" \\
        && echo "{ctl_footer}" >> "{file_to_check}" 
    """
    res = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, timeout=1)
    if verbose:
        print(f"Commands: \n {cmd}")
        print(f"Commands: \n {res.decode('utf-8')}")
        print(f"Before start {exp} [{formula}]")
    start_time = time.time()
    outb = run_nuxmv_experiment(file_to_check)
    stop_time = time.time()
    if verbose:
        print(f"After stop {exp} [{formula}]")
        print(outb.decode("utf-8"))
    return stop_time - start_time

def measure_nuxmv_ctl_experiment(exp, formula_idx, formula, output: pd.DataFrame):
    times = []
    try:
        for i in range(iters):
            time = measure_nuxmv_experiment(exp, formula_idx, formula)
            times.append(time)
            if verbose:
                print(f"--- Experiment {exp} Formula {formula} - {i}th run expired in {times[-1]}s")
        avg = np.average(times)
        std = np.std(times)
        print(f"--- Experiment {exp} Formula {formula} \n\taverage = {avg} \n\tstd = {std}")
        output.loc[len(output)] = [exp, formula, avg, std]
    except subprocess.TimeoutExpired:
        print(f"Experiment {exp} Formula {formula}: OOT")
    except Exception:
        print(f"Skipped experiment {exp} Formula {formula} one iteration failed")
        pass

def run_nuxmv_experiments():
    output = pd.DataFrame({
        'Experiment': [],
        'Formula': [],
        'Runtime': [],
        'StD': []
    })
    for exp in experiments:
        try:
            with open(exp['formulas']) as f_formulas:
                formulas = [line.rstrip() for line in f_formulas]
                for idx, formula in enumerate(formulas):
                    measure_nuxmv_ctl_experiment(exp['experiment'], idx, formula, output)
        except Exception as e:
            print(f"Skipped experiment {exp} one iteration failed\nReason was: {e}")
    return output

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog = "Branching Bisimulation Learning - Nondeterministic Benchmarks",
        description = "Runs iteratively all the nondeterministic examples with branching and deterministic approaches comparing time averages.",
        epilog = "Copyright?"
    )
    arg_parser.add_argument("-i", "--iters")
    # arg_parser.add_argument("-n", "--negated", action="store_true")
    arg_parser.add_argument("-v", "--verbose", action="store_true")
    args = arg_parser.parse_args()
    
    iters = args.iters or 10 # default iterations is 10
    iters = int(iters)
    verbose = args.verbose
    os.system("")
    output = run_nuxmv_experiments()
    output.to_csv("nuxmv-benchmarks.csv")
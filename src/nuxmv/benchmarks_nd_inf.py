from argparse import ArgumentParser
import subprocess
import time
import re
import os
import numpy as np
import pandas as pd

# nuxmv -source chech-inf-state.scr P19.smv

# Nondeterministic infinite state with LTL properties
experiments = [
    {
        'experiment': "term-loop-nd.smv",
        'formulas': "term-loop-nd.ltl"
    },
    {
        'experiment': "term-loop-nd-2.smv",
        'formulas': "term-loop-nd-2.ltl"
    },
    {
        'experiment': "term-loop-nd-y.smv",
        'formulas': "term-loop-nd-y.ltl"
    },
    {
        'experiment': "quadratic-nd.smv",
        'formulas': "quadratic-nd.ltl"
    },
    {
        'experiment': "cubic-nd.smv",
        'formulas': "cubic-nd.ltl"
    },
    {
        'experiment': "nlr-cond-nd.smv",
        'formulas': "nlr-cond-nd.ltl"
    },
    {
        'experiment': "P1.smv",
        'formulas': "P1.ltl"
    },
    {
        'experiment': "P2.smv",
        'formulas': "P2.ltl"
    },
    {
        'experiment': "P3.smv",
        'formulas': "P3.ltl"
    },
    {
        'experiment': "P4.smv",
        'formulas': "P4.ltl"
    },
    {
        'experiment': "P5.smv",
        'formulas': "P5.ltl"
    },
    {
        'experiment': "P6.smv",
        'formulas': "P6.ltl"
    },
    {
        'experiment': "P7.smv",
        'formulas': "P7.ltl"
    },
    {
        'experiment': "P17.smv",
        'formulas': "P17.ltl"
    },
    {
        'experiment': "P18.smv",
        'formulas': "P18.ltl"
    },
    {
        'experiment': "P19.smv",
        'formulas': "P19.ltl"
    },
    {
        'experiment': "P20.smv",
        'formulas': "P20.ltl"
    },
    {
        'experiment': "P21.smv",
        'formulas': "P21.ltl"
    },
    {
        'experiment': "P25.smv",
        'formulas': "P25.ltl"
    },
    {
        'experiment': "two-robots.smv",
        'formulas': "two-robots.ltl"
    },
    {
        'experiment': "two-robots-actions.smv",
        'formulas': "two-robots-actions.ltl"
    },
    {
        'experiment': "two-robots-quadratic.smv",
        'formulas': "two-robots-quadratic.ltl"
    },
]

nuxmvHome = "/CAV25/Branching-Bisimulation-Learning/nuXmv-files/nd-inf"

def run_nuxmv_experiment(exp: str, timeout = 300) -> bytes:
    cmd = f"nuxmv -source {nuxmvHome}/check-inf-state.scr {nuxmvHome}/{exp}"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = p.communicate(timeout)
        return out
    except subprocess.TimeoutExpired as e:
        p.kill()
        raise e

def measure_nuxmv_experiment(exp: str, formula_idx: int, formula: str, timeout=300):
    file_to_check = f"{formula_idx}-{exp}"
    ltl_footer = f"    LTLSPEC {formula}"
    cmd = f"""
    rm -f "{file_to_check}" \\
        && cat "{exp}" >> "{file_to_check}" \\
        && echo "{ltl_footer}" >> "{file_to_check}" 
    """
    res = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
    if verbose:
        print(f"Commands: \n {cmd}")
        print(f"Commands: \n {res.decode('utf-8')}")
        print(f"Before start {exp} [{formula}]")
    start_time = time.time()
    outb = run_nuxmv_experiment(file_to_check, timeout)
    stop_time = time.time()
    if verbose:
        print(f"After stop {exp} [{formula}]")
        print(outb.decode("utf-8"))
    return stop_time - start_time

def measure_nuxmv_ltl_experiment(exp, formula_idx, formula, output: pd.DataFrame, iters = 10, timeout = 300):
    times = []
    try:
        for i in range(iters):
            time = measure_nuxmv_experiment(exp, formula_idx, formula, timeout)
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

def run_nuxmv_experiments(iters = 10, timeout = 300):
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
                    measure_nuxmv_ltl_experiment(exp['experiment'], idx, formula, output, iters, timeout)
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
    output = run_nuxmv_experiments(iters)
    output.to_csv("nuxmv-benchmarks.csv")
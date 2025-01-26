from argparse import ArgumentParser
import subprocess
import time
import re
import os
import numpy as np
import pandas as pd

# nuxmv -source chech-inf-state.scr P19.smv

experiments = [
    {
        'experiment': "term-loop-nd.smv",
        'formulas': "term-loop-nd.ctl"
    },
    {
        'experiment': "term-loop-nd-2.smv",
        'formulas': "term-loop-nd-2.ctl"
    },
    {
        'experiment': "term-loop-nd-y.smv",
        'formulas': "term-loop-nd-y.ctl"
    },
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
    {
        'experiment': "P1.smv",
        'formulas': "P1.ctl"
    },
    {
        'experiment': "P2.smv",
        'formulas': "P2.ctl"
    },
    {
        'experiment': "P3.smv",
        'formulas': "P3.ctl"
    },
    {
        'experiment': "P4.smv",
        'formulas': "P4.ctl"
    },
    {
        'experiment': "P5.smv",
        'formulas': "P5.ctl"
    },
    {
        'experiment': "P6.smv",
        'formulas': "P6.ctl"
    },
    {
        'experiment': "P7.smv",
        'formulas': "P7.ctl"
    },
    {
        'experiment': "P17.smv",
        'formulas': "P17.ctl"
    },
    {
        'experiment': "P18.smv",
        'formulas': "P18.ctl"
    },
    {
        'experiment': "P19.smv",
        'formulas': "P19.ctl"
    },
    {
        'experiment': "P20.smv",
        'formulas': "P20.ctl"
    },
    {
        'experiment': "P21.smv",
        'formulas': "P21.ctl"
    },
    {
        'experiment': "P22.smv",
        'formulas': "P22.ctl"
    },
    {
        'experiment': "P23.smv",
        'formulas': "P23.ctl"
    },
    {
        'experiment': "P24.smv",
        'formulas': "P24.ctl"
    },
    {
        'experiment': "P25.smv",
        'formulas': "P25.ctl"
    },
    {
        'experiment': "P26.smv",
        'formulas': "P26.ctl"
    },
    {
        'experiment': "P27.smv",
        'formulas': "P27.ctl"
    },
    {
        'experiment': "P28.smv",
        'formulas': "P28.ctl"
    },
]

def run_nuxmv_experiment(exp: str) -> bytes:
    cmd = f"nuxmv -source check-inf-state.scr {exp}"
    outb = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, timeout=500)
    return outb

def run_nuxmv_experiment_(exp: str) -> bytes:
    p = subprocess.Popen(["/usr/bin/nuxmv", "-source", "check-inf-state.scr", exp], shell=True, stderr=subprocess.DEVNULL)
    try:
        p.wait(500)
        return p.stdout
    except subprocess.TimeoutExpired as e:
        p.terminate()
        raise e

def measure_nuxmv_experiment(exp: str, formula_idx: int, formula: str, progr_state_size: int):
    file_to_check = f"{formula_idx}-size{progr_state_size}-{exp}"
    ctl_footer = f"    CTLSPEC {formula}"
    state_size = 2**progr_state_size
    type = f"-{state_size}..{state_size-1}"
    substitution = "${var//integer/'%s'}" % type
    cmds = [
        f"""rm -f "{file_to_check}" """,
        f"""var=$(< "{exp}");echo "{substitution}" >> "{file_to_check}" """,
        f"""echo "{ctl_footer}" >> "{file_to_check}" """
    ]
    if verbose:
        print(f"Commands: \n {cmds}")
        print(f"Before start {exp} {state_size} [{formula}]")
    for cmd in cmds:
        res = subprocess.run(cmd, shell=True, timeout=10, capture_output=True, executable='/bin/bash')
        if verbose:
            print(f"Commands: \n {cmd} output was {res.stdout} :+: {res.stderr}")
    start_time = time.time()
    outb = run_nuxmv_experiment(file_to_check)
    stop_time = time.time()
    if verbose:
        print(f"After stop {exp} [{formula}]")
        print(outb.decode("utf-8"))
    return stop_time - start_time

def measure_nuxmv_ctl_experiment(exp, formula_idx, formula, progr_state_size, output: pd.DataFrame):
    times = []
    try:
        for i in range(iters):
            time = measure_nuxmv_experiment(exp, formula_idx, formula, progr_state_size)
            times.append(time)
            if verbose:
                print(f"--- Experiment {exp} Formula {formula} - {i}th run expired in {times[-1]}s")
        avg = np.average(times)
        std = np.std(times)
        print(f"--- Experiment {exp} Formula {formula} \n\taverage = {avg} \n\tstd = {std}")
        output.loc[len(output)] = [exp, formula, avg, std]
    except subprocess.TimeoutExpired:
        print(f"Experiment {exp} Formula {formula}: OOT")
    except Exception as e:
        print(f"Skipped experiment {exp} Formula {formula} one iteration failed: {e}")
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
                    for progr_state_size in [12, 14, 16]:
                        measure_nuxmv_ctl_experiment(exp['experiment'], idx, formula, progr_state_size, output)
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
    output.to_csv("nuxmv-ctl.csv")
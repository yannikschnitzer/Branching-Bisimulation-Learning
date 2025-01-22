from argparse import ArgumentParser
import subprocess
import time
import re
import os
import numpy as np
import pandas as pd

# ultimate-ltl P19.c

experiments = [
    {
        'experiment': "term-loop-nd.c",
        'formulas': "term-loop-nd.ltl"
    },
    {
        'experiment': "term-loop-nd-2.c",
        'formulas': "term-loop-nd-2.ltl"
    },
    {
        'experiment': "term-loop-nd-y.c",
        'formulas': "term-loop-nd-y.ltl"
    },
    {
        'experiment': "quadratic-nd.c",
        'formulas': "quadratic-nd.ltl"
    },
    {
        'experiment': "cubic-nd.c",
        'formulas': "cubic-nd.ltl"
    },
    {
        'experiment': "nlr-cond-nd.c",
        'formulas': "nlr-cond-nd.ltl"
    },
    {
        'experiment': "P1.c",
        'formulas': "P1.ltl"
    },
    {
        'experiment': "P2.c",
        'formulas': "P2.ltl"
    },
    {
        'experiment': "P3.c",
        'formulas': "P3.ltl"
    },
    {
        'experiment': "P4.c",
        'formulas': "P4.ltl"
    },
    {
        'experiment': "P5.c",
        'formulas': "P5.ltl"
    },
    {
        'experiment': "P6.c",
        'formulas': "P6.ltl"
    },
    {
        'experiment': "P7.c",
        'formulas': "P7.ltl"
    },
    {
        'experiment': "P17.c",
        'formulas': "P17.ltl"
    },
    {
        'experiment': "P18.c",
        'formulas': "P18.ltl"
    },
    {
        'experiment': "P19.c",
        'formulas': "P19.ltl"
    },
    {
        'experiment': "P20.c",
        'formulas': "P20.ltl"
    },
    {
        'experiment': "P21.c",
        'formulas': "P21.ltl"
    },
    {
        'experiment': "P25.c",
        'formulas': "P25.ltl"
    },
]

def run_ultimate_ltl_experiment(exp: str, formula: str, formula_idx: int):
    file_to_check = f"{formula_idx}-{exp}"
    ltl_header = f"""//#Safe\n//@ ltl invariant positive: {formula};"""
    cmd = f"""
    rm -f "{file_to_check}" \\
        && echo "{ltl_header}" >> "{file_to_check}" \\
        && cat "{exp}" >> "{file_to_check}" \\
        && ultimate-ltl "{file_to_check}"
    """
    outb = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, timeout=500)
    out = outb.decode("utf-8")
    time_pattern = r"Automizer plugin needed (\d+\.\d+)"
    matches = re.findall(time_pattern, out)
    return float(matches[0])

def measure_ultimate_ltl_experiment(exp: str, formula: str, formula_idx: str, output: pd.DataFrame):
    times = []
    try:
        for i in range(iters):
            time = run_ultimate_ltl_experiment(exp, formula, formula_idx)
            times.append(time)
            if verbose:
                print(f"--- Experiment {exp} Formula {formula} - {i}th run expired in {times[-1]}s")
        avg = np.average(times)
        std = np.std(times)
        output.loc[len(output)] = [exp, formula, avg, std]
        print(f"--- Experiment {exp} Formula {formula} \n\taverage = {avg} \n\tstd = {std}")
    except subprocess.TimeoutExpired:
        print(f"Experiment {exp} Formula {formula}: OOT")

def run_ultimate_ltl_experiments(iters, verbose=False) -> pd.DataFrame:
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
                    measure_ultimate_ltl_experiment(exp['experiment'], formula, idx, output)
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
    output = run_ultimate_ltl_experiments(iters, verbose=verbose)
    output.to_csv("ultimate-ltl.csv")

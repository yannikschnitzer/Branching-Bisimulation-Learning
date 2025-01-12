from argparse import ArgumentParser
import subprocess
import time
import re
import os
import numpy as np

# nuxmv -source chech-inf-state.scr P19.smv

experiments = [
    "loop-nd.smv",
    "loop-nd-2.smv",
    "loop-nd-y.smv",
    "P1.smv",
    "P2.smv",
    "P3.smv",
    "P4.smv",
    "P5.smv",
    "P6.smv",
    "P7.smv",
    "P17.smv",
    "P18.smv",
    "P19.smv",
    "P20.smv",
    "P21.smv",
    "P22.smv",
    "P23.smv",
    "P24.smv",
    "P25.smv",
    "P26.smv",
    "P27.smv",
    "P28.smv"
]

def run_nuxmv_experiment(exp: str):
    cmd = f"nuxmv -source chech-inf-state.scr {exp}"
    outb = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, timeout=500)

def measure_nuxmv_experiment(exp):
    start_time = time.time()
    run_nuxmv_experiment(exp)
    stop_time = time.time()
    return start_time, stop_time


def run_nuxmv_experiments(iters, verbose=False):
    for exp in experiments:
        times = []
        try:
            for i in range(iters):
                start_time, stop_time = measure_nuxmv_experiment(exp)
                times.append(stop_time - start_time)
                if verbose:
                    print(f"--- Experiment {exp} - {i}th run expired in {times[-1]}s")
            avg = np.average(times)
            std = np.std(times)
            print(f"--- Experiment {exp} \n\taverage = {avg} \n\tstd = {std}")
        except subprocess.TimeoutExpired:
            print(f"Experiment {exp}: OOT")
        except Exception:
            print(f"Skipped experiment {exp} one iteration failed")
            pass



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
    run_nuxmv_experiments(iters, verbose=verbose)
from argparse import ArgumentParser
import subprocess
import time
import re
import os
import numpy as np

# ultimate-ltl P19.c

experiments = [
    # "term-loop-nd.c",
    # "term-loop-nd-2.c",
    # "term-loop-nd-y.c",
    "quadratic-nd.c",
    "cubic-nd.c",
    "nlr-cond-nd.c",
    # "P1.c",
    # "P2.c",
    # "P3.c",
    # "P4.c",
    # "P5.c",
    # "P6.c",
    # "P7.c",
    # "P17.c",
    # "P18.c",
    # "P19.c",
    # "P20.c",
    # "P21.c",
    # "P22.c",
    # "P23.c",
    # "P24.c",
    # "P25.c",
    # "P26.c",
    # "P27.c",
    # "P28.c"
]

def measure_ultimate_ltl_experiment(exp: str):
    cmd = f"ultimate-ltl {exp}"
    outb = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, timeout=500)
    out = outb.decode("utf-8")
    time_pattern = r"Automizer plugin needed (\d+\.\d+)"
    matches = re.findall(time_pattern, out)
    return float(matches[0])


def run_ultimate_ltl_experiments(iters, verbose=False):
    for exp in experiments:
        times = []
        try:
            for i in range(iters):
                time = measure_ultimate_ltl_experiment(exp)
                times.append(time)
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
    run_ultimate_ltl_experiments(iters, verbose=verbose)
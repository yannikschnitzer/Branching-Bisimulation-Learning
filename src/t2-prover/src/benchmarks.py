from argparse import ArgumentParser
import subprocess
import time
import re
import os
import numpy as np


experiments = [
    {
        'name': "P1.t2",
        'formula': "[AG](varA != 1 || [AF](varR == 1))"
    },
    {
        'name': "P17.t2",
        'formula': "[AG]([AF](varW >= 1))"
    },
    {
        'name': "P18.t2",
        'formula': "[EF]([EG](varW < 1))"
    },
    {
        'name': "P19.t2",
        'formula': "[AG]([EF](varW >= 1))"
    },
    {
        'name': "P20.t2",
        'formula': "[EF]([AG](varW < 1))"
    },
    {
        'name': "P21.t2",
        'formula': "[AG]([AF](varW == 1))"
    },
    {
        'name': "P22.t2",
        'formula': "[EF]([EG](varW != 1))"
    },
    {
        'name': "P23.t2",
        'formula': "[AG]([EF](varW == 1))"
    }
]

def run_t2_experiment(exp):
    cmd = f"""
    mono src/bin/Debug/T2.exe \\
        test/cav13-ctl-examples/{exp['name']} \\
        --CTL '{exp['formula']}' 
    """
    outb = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
    out = outb.decode("utf-8")
    match = re.search("Temporal proof succeeded", out)
    if match is None:
        print("Alarm! Alarm!")
        print(out)

def run_t2_experiments(iters, verbose=False):
    for exp in experiments:
        times = []
        for i in range(iters):
            start_time = time.time()
            run_t2_experiment(exp)
            stop_time = time.time()
            times.append(stop_time - start_time)
            if verbose:
                print(f"--- Experiment {exp} - {i}th run expired in {times[-1]}s")
        avg = np.average(times)
        std = np.std(times)
        print(f"--- Experiment {exp} \n\taverage = {avg} \n\tstd = {std}")



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog = "Branching Bisimulation Learning - Nondeterministic Benchmarks",
        description = "Runs iteratively all the nondeterministic examples with branching and deterministic approaches comparing time averages.",
        epilog = "Copyright?"
    )
    arg_parser.add_argument("-i", "--iters")
    arg_parser.add_argument("-v", "--verbose", action="store_true")
    args = arg_parser.parse_args()
    
    iters = args.iters or 10 # default iterations is 10
    iters = int(iters)
    verbose = args.verbose
    os.system("")
    run_t2_experiments(iters, verbose)
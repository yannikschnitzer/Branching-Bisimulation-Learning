from argparse import ArgumentParser
import subprocess
import time
import re
import os
import numpy as np

# mono src/bin/Debug/T2.exe bl_tests/term_loop_nd_2.t2 --CTL '[EG]([AF](varX == 0))'
# mono src/bin/Debug/T2.exe bl_tests/term_loop_nd_2.t2 --CTLStar 'G(F(varX == 0))'

experiments = [
    {
        'name': "test/cav13-ctl-examples/P1.t2",
        'formula': "[AG](varA != 1 || [AF](varR == 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P2.t2",
        'formula': "[EF](varA == 1 && [EG](varR != 5))"
    },
    {
        'name': "test/cav13-ctl-examples/P3.t2",
        'formula': "[AG](varA != 1 || [EF](varR == 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P4.t2",
        'formula': "[EF](varA == 1 && [AG](varR != 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P5.t2",
        'formula': "[AG](varS != 1 || [AF](varU == 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P6.t2",
        'formula': "[EF](varS == 1 || [EG](varU != 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P7.t2",
        'formula': "[AG](varS != 1 || [EF](varU == 1))"
    },
    # {
    #     'name': "test/cav13-ctl-examples/P8.t2",
    #     'formula': "[EF](varS == 1 && [AG](varU != 1))"
    # },
    # {
    #     'name': "test/cav13-ctl-examples/P9.t2",
    #     'formula': "[AG](varA != 1 || [AF](varR == 1))"
    # },
    # {
    #     'name': "test/cav13-ctl-examples/P10.t2",
    #     'formula': "[EF](varA == 1 && [EG](varR != 1))"
    # },
    # {
    #     'name': "test/cav13-ctl-examples/P11.t2",
    #     'formula': "[AG](varA != 1 || [EF](varR == 1))"
    # },
    # {
    #     'name': "test/cav13-ctl-examples/P12.t2",
    #     'formula': "[EF](varA == 1 && [AG](varR != 1))"
    # },
    # {
    #     'name': "test/cav13-ctl-examples/P13.t2",
    #     'formula': "[EG](varP1 != 1) || [EG](varP2 != 1)"
    # },
    # {
    #     'name': "test/cav13-ctl-examples/P14.t2",
    #     'formula': "[EG](varP1 != 1) || [EG](varP2 != 1)"
    # },
    # {
    #     'name': "test/cav13-ctl-examples/P15.t2",
    #     'formula': "[EF](varP1 == 1) && [EF](varP2 == 1)"
    # },
    # {
    #     'name': "test/cav13-ctl-examples/P16.t2",
    #     'formula': "[AG](varP1 != 1) || [AG](varP2 != 1)"
    # },
    {
        'name': "test/cav13-ctl-examples/P17.t2",
        'formula': "[AG]([AF](varW >= 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P18.t2",
        'formula': "[EF]([EG](varW < 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P19.t2",
        'formula': "[AG]([EF](varW >=1))"
    },
    {
        'name': "test/cav13-ctl-examples/P20.t2",
        'formula': "[EF]([AG](varW < 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P21.t2",
        'formula': "[AG]([AF](varW == 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P22.t2",
        'formula': "[EF]([EG](varW != 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P23.t2",
        'formula': "[AG]([EF](varW == 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P24.t2",
        'formula': "[EF]([AG](varW != 1))"
    },
    {
        'name': "test/cav13-ctl-examples/P25.t2",
        'formula': "(varC > 5) -> ([AF](varR > 5))"
    },
    {
        'name': "test/cav13-ctl-examples/P26.t2",
        'formula': "(varC > 5) && [EG](varR <= 5)"
    },
    {
        'name': "test/cav13-ctl-examples/P27.t2",
        'formula': "(varC <= 5) || [EF](varR > 5)"
    },
    {
        'name': "test/cav13-ctl-examples/P28.t2",
        'formula': "(varC > 5) && [AG](varR <= 5)"
    },
    {
        'name': "bl_tests/term_loop_nd.t2",
        'formula': "[EG](varX > 1 || varX < -1)"
    },
    {
        'name': "bl_tests/term_loop_nd_2.t2",
        'formula': "[EG]([AF](varX == 0))"
    },
    {
        'name': "bl_tests/term_loop_nd_y.t2",
        'formula': "[EG]([AF](varX == 0))"
    }
]

def run_t2_experiment(exp, ltl=False):
    formula = exp['formula']
    star = 'Star' if ltl else ''
    cmd = f"""
    mono src/bin/Debug/T2.exe \\
        {exp['name']} \\
        --CTL{star} '{formula}' 
    """
    outb = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
    out = outb.decode("utf-8")
    match = re.search("Temporal proof", out)
    if match is None:
        print("Alarm! Alarm!")
        raise Exception(out)

def measure_t2_experiment(exp, ltl):
    start_time = time.time()
    run_t2_experiment(exp, ltl)
    stop_time = time.time()
    return start_time, stop_time


def run_t2_experiments(iters, verbose=False, negated=False, ltl=False):
    for exp in experiments:
        formula = exp['formula']
        if negated:
            formula = f"!({formula})"
        if ltl:
            formula = re.sub(r"\[[AE](.)\]", r"\1", formula)
        exp['formula'] = formula
        times = []
        try:
            for i in range(iters):
                start_time, stop_time = measure_t2_experiment(exp, ltl)
                times.append(stop_time - start_time)
                if verbose:
                    print(f"--- Experiment {exp} - {i}th run expired in {times[-1]}s")
            avg = np.average(times)
            std = np.std(times)
            print(f"--- Experiment {exp} \n\taverage = {avg} \n\tstd = {std}")
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
    arg_parser.add_argument("-n", "--negated", action="store_true")
    arg_parser.add_argument("--ltl", action="store_true")
    arg_parser.add_argument("-v", "--verbose", action="store_true")
    args = arg_parser.parse_args()
    
    iters = args.iters or 10 # default iterations is 10
    iters = int(iters)
    negated = args.negated
    ltl     = args.ltl
    verbose = args.verbose
    os.system("")
    run_t2_experiments(iters, verbose=verbose, negated=negated, ltl=ltl)
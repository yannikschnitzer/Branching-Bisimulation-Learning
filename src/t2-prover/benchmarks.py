from argparse import ArgumentParser
import subprocess
import time
import re
import os
import numpy as np
import pandas as pd

# mono src/bin/Debug/T2.exe bl_tests/term_loop_nd_2.t2 --CTL '[EG]([AF](varX == 0))'
# mono src/bin/Debug/T2.exe bl_tests/term_loop_nd_2.t2 --CTLStar 'G(F(varX == 0))'

experiments = [
    {
    'name': 'bl_tests/term_loop_nd.t2',
    'formula': 'G(varX > 1 || varX < -1)'
    },
    {
    'name': 'bl_tests/term_loop_nd.t2',
    'formula': 'F(G(varX <= 1) || G(varX >= -1))'
    },
    {
    'name': 'bl_tests/term_loop_nd.t2',
    'formula': 'G(F(varX > 1))'
    },
    {
    'name': 'bl_tests/term_loop_nd.t2',
    'formula': '[EG](varX > 1 || varX < -1)'
    },
    {
    'name': 'bl_tests/term_loop_nd.t2',
    'formula': '!([EG](varX > 1 || varX < -1))'
    },
    {
    'name': 'bl_tests/term_loop_nd.t2',
    'formula': '[AF]([AG](varX <= 1) && [AG] (varX >= -1))'
    },
    {
    'name': 'bl_tests/term_loop_nd.t2',
    'formula': 'A F(G(F(varX <= 1)) || G(F(varX >= -1)))'
    },



    {
    'name': 'bl_tests/term_loop_nd_2.t2',
    'formula': "G(F(varX == 0))"
    },
    {
    'name': 'bl_tests/term_loop_nd_2.t2',
    'formula': "F(G(varX <= 1) || G(varX >= -1))"
    },
    {
    'name': 'bl_tests/term_loop_nd_2.t2',
    'formula': "[EG]([AF](varX == 0))"
    },
    {
    'name': 'bl_tests/term_loop_nd_2.t2',
    'formula': "!([EG]([AF](varX == 0))"
    },
    {
    'name': 'bl_tests/term_loop_nd_2.t2',
    'formula': "[AF]([AG](varX <= 1) && [AG] (varX >= -1))"
    },
    {
    'name': 'bl_tests/term_loop_nd_2.t2',
    'formula': "A F(E G( F(varX <= 1)) && A G (F (varX >= -1)))'"
    },

    


    {
    'name': 'bl_tests/term_loop_nd_y.t2',
    'formula': "[EG]([AF](varX == 0))"
    },
    {
    'name': 'bl_tests/term_loop_nd_y.t2',
    'formula': "!([EG]([AF](varX == 0)))"
    },
    {
    'name': 'bl_tests/term_loop_nd_y.t2',
    'formula': "G(F(varX == 0))"
    },
    {
    'name': 'bl_tests/term_loop_nd_y.t2',
    'formula': "E G(F(varX == 0) && F(G (varX != 0)))"
    },



    {
    'name': "test/cav13-ctl-examples/P1.t2",
    'formula': "[AG](varA != 1 || [AF](varR == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P1.t2",
    'formula': "!([AG](varA != 1 || [AF](varR == 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P1.t2",
    'formula': "G(varA != 1 || F(varR == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P1.t2",
    'formula': "E G(F(varA != 1 || F(varR == 1)))"
    },



    {
    'name': "test/cav13-ctl-examples/P2.t2",
    'formula': "[EF](varA == 1 && [EG](varR != 5))"
    },
    {
    'name': "test/cav13-ctl-examples/P2.t2",
    'formula': "!([EF](varA == 1 && [EG](varR != 5)))"
    },
    {
    'name': "test/cav13-ctl-examples/P2.t2",
    'formula': "F(varA == 1 && G(varR != 5))"
    },
    {
    'name': "test/cav13-ctl-examples/P2.t2",
    'formula': "E G (F(varA == 1 && E G(varR != 5)))"
    },


    {
    'name': "test/cav13-ctl-examples/P3.t2",
    'formula': "[AG](varA != 1 || [EF](varR == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P3.t2",
    'formula': "!([AG](varA != 1 || [EF](varR == 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P3.t2",
    'formula': "G(varA != 1 || F(varR == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P3.t2",
    'formula': "E F( G(varA != 1 || A G(varR == 1)))"
    },



    {
    'name': "test/cav13-ctl-examples/P4.t2",
    'formula': "[EF](varA == 1 && [AG](varR != 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P4.t2",
    'formula': "!([EF](varA == 1 && [AG](varR != 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P4.t2",
    'formula': "F(varA == 1 && G(varR != 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P4.t2",
    'formula': "E G (F(varA == 1 && E G(varR != 1)))"
    },


    {
    'name': "test/cav13-ctl-examples/P5.t2",
    'formula': "[AG](varS != 1 || [AF](varU == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P5.t2",
    'formula': "!([AG](varS != 1 || [AF](varU == 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P5.t2",
    'formula': "G(varS != 1 || F(varU == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P5.t2",
    'formula': "E F (G(varS != 1 || A F(varU == 1)))"
    },



    {
    'name': "test/cav13-ctl-examples/P6.t2",
    'formula': "[EF](varS == 1 || [EG](varU != 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P6.t2",
    'formula': "!([EF](varS == 1 || [EG](varU != 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P6.t2",
    'formula': "F(varS == 1 || G(varU != 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P6.t2",
    'formula': "E G (F(varS == 1 && E F(varU != 1)))"
    },


    {
    'name': "test/cav13-ctl-examples/P7.t2",
    'formula': "[AG](varS != 1 || [EF](varU == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P7.t2",
    'formula': "!([AG](varS != 1 || [EF](varU == 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P7.t2",
    'formula': "G(varS != 1 || F(varU == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P7.t2",
    'formula': "E G(varS != 1 || F(varU == 1) || E F(varU == 1))"
    },


    {
    'name': "test/cav13-ctl-examples/P17.t2",
    'formula': "[AG]([AF](varW >= 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P17.t2",
    'formula': "!([AG]([AF](varW >= 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P17.t2",
    'formula': "G(F(varW >= 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P17.t2",
    'formula': "E G( F(varW >= 1) || A G (E F(varW >= 1)))"
    },

    {
    'name': "test/cav13-ctl-examples/P18.t2",
    'formula': "[EF]([EG](varW < 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P18.t2",
    'formula': "!([EF]([EG](varW < 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P18.t2",
    'formula': "F(G(varW < 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P18.t2",
    'formula': "E F(F(varW >= 1)) || A F (E G(varW < 1)))"
    },


    {
    'name': "test/cav13-ctl-examples/P19.t2",
    'formula': "[AG]([EF](varW >=1))"
    },
    {
    'name': "test/cav13-ctl-examples/P19.t2",
    'formula': "!([AG]([EF](varW >=1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P19.t2",
    'formula': "G(F(varW >=1))"
    },
    {
    'name': "test/cav13-ctl-examples/P19.t2",
    'formula': "E G(F(varW >=1) || E F (A G(varW >=1)))"
    },

    {
    'name': "test/cav13-ctl-examples/P20.t2",
    'formula': "[EF]([AG](varW < 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P20.t2",
    'formula': "!([EF]([AG](varW < 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P20.t2",
    'formula': "F(G(varW < 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P20.t2",
    'formula': "E F(G(varW >= 1)) || A G(F(varW >= 1))"
    },

    {
    'name': "test/cav13-ctl-examples/P21.t2",
    'formula': "[AG]([AF](varW == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P21.t2",
    'formula': "!([AG]([AF](varW == 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P21.t2",
    'formula': "G(F(varW == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P21.t2",
    'formula': "E F(G(varW >= 1)) || A G(F(varW >= 1))"
    },

    {
    'name': "test/cav13-ctl-examples/P22.t2",
    'formula': "[EF]([EG](varW != 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P22.t2",
    'formula': "!([EF]([EG](varW != 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P22.t2",
    'formula': "F(G(varW != 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P22.t2",
    'formula': "E F(G(varW >= 1)) || A G(F(varW >= 1))"
    },

    {
    'name': "test/cav13-ctl-examples/P23.t2",
    'formula': "[AG]([EF](varW == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P23.t2",
    'formula': "!([AG]([EF](varW == 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P23.t2",
    'formula': "G(F(varW == 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P23.t2",
    'formula': "E F(G(varW >= 1)) || A G(F(varW >= 1))"
    },

    {
    'name': "test/cav13-ctl-examples/P24.t2",
    'formula': "[EF]([AG](varW != 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P24.t2",
    'formula': "!([EF]([AG](varW != 1)))"
    },
    {
    'name': "test/cav13-ctl-examples/P24.t2",
    'formula': "F(G(varW != 1))"
    },
    {
    'name': "test/cav13-ctl-examples/P24.t2",
    'formula': "E F(G(varW >= 1)) || A G(F(varW >= 1))"
    },

    {
    'name': "test/cav13-ctl-examples/P25.t2",
    'formula': "(varC > 5) -> ([AF](varR > 5))"
    },
    {
    'name': "test/cav13-ctl-examples/P25.t2",
    'formula': "(varC > 5) && ![AF](varR > 5)"
    },
    {
    'name': "test/cav13-ctl-examples/P25.t2",
    'formula': "(varC > 5) -> (F(varR > 5))"
    },
    {
    'name': "test/cav13-ctl-examples/P25.t2",
    'formula': "E G (F(varC == 5) || G (varC > 5) && F (G (varR > 5)))"
    },

    {
    'name': "test/cav13-ctl-examples/P26.t2",
    'formula': "(varC > 5) && [EG](varR <= 5)"
    },
    {
    'name': "test/cav13-ctl-examples/P26.t2",
    'formula': "!((varC > 5) && [EG](varR <= 5))"
    },
    {
    'name': "test/cav13-ctl-examples/P26.t2",
    'formula': "(varC > 5) && G(varR <= 5)"
    },
    {
    'name': "test/cav13-ctl-examples/P26.t2",
    'formula': "E G (F(varC == 5) || G (varC > 5) && F (G (varR > 5)))"
    },

    {
    'name': "test/cav13-ctl-examples/P27.t2",
    'formula': "(varC <= 5) || [EF](varR > 5)"
    },
    {
    'name': "test/cav13-ctl-examples/P27.t2",
    'formula': "!((varC <= 5) || [EF](varR > 5))"
    },
    {
    'name': "test/cav13-ctl-examples/P27.t2",
    'formula': "(varC <= 5) || F(varR > 5)"
    },
    {
    'name': "test/cav13-ctl-examples/P27.t2",
    'formula': "E G (F(varC == 5) || G (varC > 5) && F (G (varR > 5)))"
    },

    {
    'name': "test/cav13-ctl-examples/P28.t2",
    'formula': "(varC > 5) && [AG](varR <= 5)",
    },
    {
    'name': "test/cav13-ctl-examples/P28.t2",
    'formula': "!((varC > 5) && [AG](varR <= 5))",
    },
    {
    'name': "test/cav13-ctl-examples/P28.t2",
    'formula': "(varC > 5) && G(varR <= 5)",
    },
    {
    'name': "test/cav13-ctl-examples/P28.t2",
    'formula': "E G (F(varC == 5) || G (varC > 5) && F (G (varR > 5)))",
    },

]

def run_subprocess(name, flag, formula, timeoutFlag, timeout=300):
    command = ' '.join(["/usr/bin/mono", "src/bin/Debug/T2.exe", name, flag, formula, timeoutFlag])
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = p.communicate(timeout=timeout)
        return out
    except subprocess.TimeoutExpired as e:
        p.kill()
        raise e

def run_t2_experiment(exp, timeout):
    formula = exp['formula']
    ctlstar = not re.search(r"\[", formula) # syntax for ctlstar does not contain square brackets
    star = 'Star' if ctlstar else ''
    options = [
        exp['name'],
        f"--CTL{star}",
        f"'{formula}'",
        f"--timeout={timeout+50}" # we give a little more timeout than specified here so that we can manage the exception internally
    ]
    outb = run_subprocess(*options, timeout=timeout)
    # outb = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
    out = outb.decode("utf-8")
    match = re.search("Temporal proof", out)
    if match is None:
        raise Exception(f"Check was unsuccessful: T2-output was '{out}'")

def measure_t2_experiment(exp, iters=10, tolerance = 5, timeout=300):
    times = []
    skipped = 0
    for i in range(iters):
        try:
            start_time = time.time()
            run_t2_experiment(exp, timeout=timeout)
            stop_time = time.time()
            times.append(stop_time - start_time)
            if verbose:
                print(f"--- Experiment {exp} - {i}th run expired in {stop_time - start_time}s")
        except subprocess.TimeoutExpired as e:
            # propagate exception, don't try again
            print("Timeout expired")
            raise e
        except Exception as e:
            print(f"Discarding one run of {exp}: exception was '{e}' \n \t skipped until now = {skipped + 1}")
            skipped += 1
            if skipped > tolerance:
                print(f"Raising exception now")
                raise e
    avg = np.average(times)
    std = np.std(times)
    print(f"--- Experiment {exp} \n\taverage = {avg} \n\tstd = {std}")
    return avg, std

def run_t2_experiments(iters, verbose=False, tolerance=5, timeout=300):
    df = pd.DataFrame(columns=["Experiment", "Average", "StD"])
    for exp in experiments:
        try:
            avg, std = measure_t2_experiment(exp, iters=iters, timeout=timeout, tolerance=tolerance)
            df.loc[len(df)] = [exp, avg, std]
        except subprocess.TimeoutExpired:
            df.loc[len(df)] = [exp, "OOT", ""]
        except Exception as e:
            df.loc[len(df)] = [exp, str(e), ""]
    return df



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog = "Branching Bisimulation Learning - Nondeterministic Benchmarks",
        description = "Runs iteratively all the T2 benchmarks."
    )
    arg_parser.add_argument("-i", "--iters", help="The number of times to repeat the benchmarks. Default is 10")
    arg_parser.add_argument("--timeout", help="The allowed maximun running time. Default is 300")
    arg_parser.add_argument("-t", "--tolerance", help="The maximum number of times that a benchmark can break before being excluded from the report. Default is 5")
    arg_parser.add_argument("-v", "--verbose", action="store_true", help="Prints additional information during execution")
    args = arg_parser.parse_args()
    
    iters = args.iters or 10 # default iterations is 10
    iters = int(iters)
    tolerance = int(args.tolerance or 5)
    timeout = int(args.timeout or 300)
    verbose = args.verbose
    os.system("")
    df = run_t2_experiments(iters, verbose=verbose, tolerance=tolerance, timeout=timeout)
    df.to_csv(f"t2-benchmarks-{time}.csv")
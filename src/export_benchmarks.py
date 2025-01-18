
import pandas as pd

from time import time
from argparse import ArgumentParser

def get_experiments(command):
    match command:
        case "det-sync" | "s" | "sync":
            return []
        case "det-term" | "t" | "term":
            return []
        case "branching" | "b" | "brn" | "branch":
            return []
        case _:
            raise Exception(f"Command {command} is not one of the allowed. Please run this script with -h to see which ones are allowed.")
    
def get_tool_runner(tool):
    match tool:
        case "det-bl":
            return lambda x: x
        case _:
            raise Exception(f"Tool {tool} is not one of the allowed. Please run this script with -h to see which ones are allowed.")

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Bisimulation Learning - Benchmarks",
        description="Runs iteratively all the benchmarks"
    )
    parser.add_argument("benchmarks", help="""
    Benchmark set to use. You can choose between: 
        1. s || det-sync  : Deterministic synchronization
        2. t || det-term  : Deterministic termination
        3. b || branching : Nondeterministic benchmarks
    """)
    parser.add_argument("-v", "--verbose", action="store_true", help="Print additional information")
    parser.add_argument("-i", "--iters", help="Number of iterations per run. Default is 10")
    parser.add_argument("-e", "--export", help="Export results in .csv")
    parser.add_argument("-t", "--tools", nargs="+", help="""
    Tools to run the benchmarks. Please note that some benchmark sets are unavailable for certain tools (refer to the following list):
        1. det-bl    : Deterministic Bisimulation Learning (avail: det-sync, det-term)
        2. brn-bl    : Branching Bisimulation Learning (available for all benchmark sets)
        3. nuxmv     : nuXmv 2.1.0 (IC3) (available for all benchmark sets)
        4. nuxmv-bdd : nuXmv 2.1.0 (BDDs) (avail: det-clock)
        5. cpa       : CPAchecker 4.0 (avail: det-term)
        6. ultimate  : Ultimate Automizer (avail: det-term, non-det (as Ultimate LTL Automizer))
        7. t2        : T2-temporal prover (avail: non-det)
    """)
    args = parser.parse_args()

    # global namespace
    benchmarks = args.benchmarks
    iters      = args.iters      or 10
    tools      = args.tools      or []
    export     = args.export
    verbose    = args.verbose

    df = pd.DataFrame()
    experiments = get_experiments(benchmarks)
    runners = [get_tool_runner(tool) for tool in tools]

    for runner in runners:
        results = runner(experiments)
        df[show_name] = results
    
    if export:
        tls = '_'.join(tools)
        df.to_csv(f"results_{int(time())}_{benchmarks}_{tls}.csv")




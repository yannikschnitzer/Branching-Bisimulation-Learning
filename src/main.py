from argparse import ArgumentParser
import nuxmv.nuxmv_experiments as nuxmv_det
from time import time

usage = """
You can run different datasets specifying the tool and the property to check. Note that Bisumulation Learning doesn't run a property check: in some cases, you can run it in "branching" mode and "deterministic" mode. Please, consider the following availability schema:
- 'clock': the finite state clock synchronisation protocols (table 1). Possible tools allowed:
    - 'nuxmv' with modes 'ic3' and 'bdd' and formulas 'safe' and 'synch'
    - 'bisimulation-learning' with modes 'det' and 'brn'
- 'term': the infinite state termination dataset (table 2). Possible tools allowed:
    - 'nuxmv' ('ic3' only) with formulas 'term' and 'nonterm'
    - 'cpa' with formulas 'term' and 'nonterm'
    - 'ultimate' with formulas 'term' and 'nonterm'
    - 'bisimulation-learning' with modes 'det' and 'brn'
- 'nd-inf': the infinite state, (bounded) branching dataset with the formulas to be checked (table 3). Possible tools allowed:
    - 'nuxmv' ('ic3' only)
    - 'ultimate'
    - 'bisimulation-learning' ('brn' mode only)
- 'nd-inf-t2': the infinite state, (bounded) branching dataset for T2 comparison (table 4). Possible tools allowed:
    - 't2'
    - 'bisimulation-learning' ('brn' mode only)
- 'nd-fin': the finite state, (bounded) branching dataset (table 5). Please note that this allows to set the systems' size with the --size flag. Possible tools allowed:
    - 'nuxmv' ('bdd' mode only)
    - 'bisimulation-learning' ('brn' mode only)
"""

def run_nuxmv_benchmarks(args):
    if args.mode not in ['ic3', 'bdd']:
        raise Exception(f"Mode {args.mode} not available for nuxmv")
    if args.dataset == 'clock':
        args.formula = args.formula or 'safe'
        if args.formula not in ['safe', 'synch']:
            raise Exception(f"Formula {args.formula} not available for clock dataset on nuxmv tool")
    if args.dataset == 'term':
        if args.mode != 'ic3':
            raise Exception(f"Mode {args.mode} not available on term dataset")
        args.formula = args.formula or 'term'
        if args.formula not in ['term', 'nonterm']:
            raise Exception(f"Formula ${args.formula} not available for term dataset on nuxmv tool")
    if args.dataset == 'nd-inf' and args.mode != 'ic3':
        raise Exception(f"Mode {args.mode} not available on term dataset")
    if args.dataset == 'nd-fin' and args.mode != 'bdd':
        raise Exception(f"Mode {args.mode} not available on term dataset")
    set_output_filename(args)
    if args.dataset in ['clock', 'term']:
        # if its a deterministic dataset get it from nuxmv_det
        dataset = []
        phi = 'g' if args.formula == 'safe' else 'gf'
        for prt in ['tte', 'con']:
            for st in ['sf', 'usf']:
                for size in ['10', '100', '1000', '2000', '5000', '10000']:
                    exp = getattr(nuxmv_det, f'exp_{prt}_{st}_{size}_{phi}_{args.mode}')
                    dataset.append(exp())
        # dataset built just with the relevant ones
        df = nuxmv_det.run_nuxmv_experiments_iters(
            experiments=dataset,
            iters=args.iters,
            timeout=args.timeout)
        return df
    else:
        return None
        



def validate_bisimulation_learning(args):
    if args.mode not in ['det', 'brn']:
        raise Exception(f"Mode {args.mode} not available for bisimulation learning")
    if args.dataset == 'nd-inf' and args.mode != 'brn':
        raise Exception(f"Mode {args.mode} not available on term dataset")
    if args.dataset == 'nd-fin' and args.mode != 'brn':
        raise Exception(f"Mode {args.mode} not available on term dataset")

def run_clock_benchmarks(args):
    if args.tool not in ['nuxmv', 'bisimulation-learning']:
        raise Exception(f"Tool {args.tool} not allowed for clock dataset")
    else:
        if args.tool == 'nuxmv':
            args.mode = args.mode or 'ic3'
            run_nuxmv_benchmarks(args)
        else:
            args.mode = args.mode or 'det'
            validate_bisimulation_learning(args)

def run_benchmarks(args):
    args.dataset = args.dataset or 'clock'
    args.iters = int(args.iters or 10)
    args.timeout = int(args.timeout or 300)
    if args.tool == 'bl':
        args.tool = 'bisimulation-learning'
    match args.dataset:
        case 'clock':
            run_clock_benchmarks(args)
        case _:
            raise Exception(f"Dataset {args.dataset} not implemented yet.")

def set_output_filename(args):
    if args.output is None:
        args.output = args.output or f"{time()}-{args.dataset}-{args.tool}"
        if args.mode is not None:
            args.output += "-" + args.mode
        if args.formula is not None:
            args.output += "-" + args.formula
        if args.size is not None:
            args.output += "-" + args.size
        
if __name__ == "__main__":
    parser = ArgumentParser("CAV 25 Artifact Evaluation",
        usage=usage)
    parser.add_argument("-d", "--dataset", required=True, help="""
    The dataset to evaluate. Possible values: 'clock', 'term', 'nd-inf', 'nd-fin', 'nd-inf-t2'.
    """)
    parser.add_argument("-t", "--tool", required=True, help="The tool to run on the experiments. Possible values are: 'nuxmv-ic3', 'nuxmv-bdd', 'cpa', 'ultimate', 'bisimulation-learning'")
    parser.add_argument("-f", "--formula", help="The formula to evaluate on the experiments. On 'clock' and 'term' datasets only. Not available on 'bisimulation-learning'. Please refer on the help message for compatibility with the dataset.")
    parser.add_argument("-m", "--mode", help="The tool's mode. Available values: 'ic3', 'bdd' for 'nuxmv' and 'det', 'brn' for 'bisimulation-learning'")
    parser.add_argument("-s", "--size", help="Sizes for the nondeterministic finite state systems. Available state sizes are 9, 11, 13, 15 and 17")
    parser.add_argument("-i", "--iters", help="Number of iterations to run a single test to get the average. Default value is 10")
    parser.add_argument("--timeout", help="Timeout of a single test, in seconds. Default 300 seconds")
    parser.add_argument("-o", "--output", help="Output csv file. Default is CURRENT_DATE-DATASET-TOOL[-MODE][-FORMULA][-SIZE].csv")

    args = parser.parse_args()

    try:
        df = run_benchmarks(args)
        df.to_csv(args.output)
    except Exception as e:
        print("Error:", e)
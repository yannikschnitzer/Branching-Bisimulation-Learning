#! /usr/bin/python3
from argparse import ArgumentParser
import nuxmv.nuxmv_experiments as nuxmv_det
import nuxmv.benchmarks_nd_inf as nuxmv_nd_inf
import nuxmv.benchmarks_nd_fin as nuxmv_nd_fin
import cpa.CPA_experiments as cpa
import ultimate.ultimate_experiments as ultimate_det
import ultimate_ltl.benchmarks as ultimate_nd_inf
print("Preparing deterministic benchmarks...")
import benchmark_det as bl_det
print("Preparing nondeterministic benchmarks...")
import benchmark_nd as bl_brn
from time import time

usage = """
You can run different datasets specifying the tool and the property to check. Please, consider the following availability schema:
- 'clock': the finite state clock synchronisation protocols (table 1). Possible tools allowed:
    - 'nuxmv' with modes 'ic3' and 'bdd' and formulas 'safe' and 'synch'
    - 'bisimulation-learning' (accepted alias: 'bl') with modes 'det' and 'brn'
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

def pretty_print(args):
    and_rank_function ="one single global ranking function" if args.global_rank else "a function for each class (i.e. 'piecewise' ranking function)"
    out = f"""Running benchmarks with following configuration:
    - Dataset: {args.dataset}
    - Tool: {args.tool} {'with ' + and_rank_function if args.tool == 'bisimulation-learning' else ''}"""
    
    if args.formula is not None:
        out += f"\n    - Formula: {args.formula}"
    if args.mode is not None:
        out += f"\n    - Mode: {args.mode}"
    if args.size is not None:
        out += f"\n    - Size: {args.size}"

    out += f"""

    Each test will be repeated {args.iters} times with a maximum running time of {args.timeout} seconds.
    Output file: {args.output}
    """
    return out


def set_output_filename(args):
    if args.output is None:
        args.output = args.output or f"{args.tool}-{args.dataset}"
        if args.mode is not None:
            args.output += "-" + args.mode
        if args.formula is not None:
            args.output += "-" + args.formula
        if args.size is not None:
            args.output += "-" + str(args.size)
        args.output += f"-{int(time())}.csv"

def validate(args):
    args.iters = int(args.iters or 10)
    args.timeout = int(args.timeout or 300)
    if args.tool == 'bl':
        args.tool = 'bisimulation-learning'
    match args.dataset:
        case 'clock':
            return validate_clock(args)
        case 'term':
            return validate_term(args)
        case 'nd-inf':
            return validate_nd_inf(args)
        case 'nd-fin':
            return validate_nd_fin(args)
        case 'nd-inf-t2':
            return validate_nd_inf_t2(args)
        case _:
            raise Exception(f"Dataset {args.dataset} is not a valid dataset")

def validate_clock(args):
    if args.tool == 'nuxmv':
        args.mode = args.mode or 'ic3'
        if args.mode not in ['ic3', 'bdd']:
            raise Exception(f"Mode {args.mode} not available for nuxmv / clock")
        args.formula = args.formula or 'safe'
        if args.formula not in ['safe', 'synch']:
            raise Exception(f"Formula {args.formula} not available nuxmv / clock")
    elif args.tool == 'bisimulation-learning':
        args.mode = args.mode or 'brn'
        if args.mode not in ['brn', 'det']:
            raise Exception(f"Mode {args.mode} not available for bisimulation learning / clock")
    else:
        raise Exception(f"Tool {args.tool} not valid for 'clock' dataset")
    return args

def validate_term(args):
    if args.tool == 'nuxmv':
        print(f"[INFO] Only available mode for nuxmv / term is 'ic3': setting up...")
        args.mode = 'ic3'
    if args.tool in ['nuxmv', 'cpa', 'ultimate']:
        args.formula = args.formula or 'term'
        if args.formula not in ['term', 'nonterm']:
            raise Exception(f"Formula {args.formula} not available {args.tool} / term")
    elif args.tool == 'bisimulation-learning':
        args.mode = args.mode or 'brn'
        if args.mode not in ['brn', 'det']:
            raise Exception(f"Mode {args.mode} not available for bisimulation learning / term")
    else:
        raise Exception(f"Tool {args.tool} not valid for 'term' dataset")
    return args

    
def validate_nd_inf(args):
    if args.tool == 'nuxmv':
        print(f"[INFO] Only available mode for nuxmv / nd-inf is 'ic3': setting up...")
        args.mode = 'ic3'
    elif args.tool == 'bisimulation-learning':
        print(f"[INFO] Only available mode for bisimulation learning / nd-inf is 'brn': setting up...")
        args.mode = 'brn'
    elif args.tool == 't2':
        raise Exception(f"T2 has a dedicated dataset: 'nd-inf-t2. Try run the program with that dataset: please note that T2 also might require a different container to run. See the README for more information.")
    elif args.tool != 'ultimate':
        raise Exception(f"Tool {args.tool} not valid for 'nd-inf' dataset")
    return args

def validate_nd_inf_t2(args):
    if args.tool == 'bisimulation-learning':
        print(f"[INFO] Only available mode for bisimulation learning / nd-inf-t2 is 'brn': setting up...")
        args.mode = 'brn'
    elif args.tool in ['ultimate', 'cpa', 'nuxmv']:
        raise Exception(f"This is the t2 dedicated dataset. Other tools should run on the general 'nd-inf' dataset. Try run the program with that dataset: please note that T2 also requires a different container to run. See the README for more information.")
    elif args.tool != 't2':
        raise Exception(f"Tool {args.tool} not valid for 'nd-inf-t2' dataset")
    return args

def validate_nd_fin(args):
    if args.tool == 'nuxmv':
        print(f"[INFO] Only available mode for nuxmv / nd-fin is 'bdd': setting up...")
        args.mode = 'bdd'
        args.size = int(args.size or 9)
    elif args.tool == 'bisimulation-learning':
        print(f"[INFO] Only available mode for bisimulation learning / nd-fin is 'brn': setting up...")
        args.mode = 'brn'
    else:
        raise Exception(f"Tool {args.tool} not valid for 'nd-fin' dataset")
    return args


def run_nuxmv_det_benchmarks(args, experiments):
    return nuxmv_det.run_nuxmv_experiments_iters(
        experiments=experiments,
        iters=args.iters,
        timeout=args.timeout,
        verbose=args.verbose
    )

def run_nuxmv_nd_inf_benchmarks(args):
    return nuxmv_nd_inf.run_nuxmv_experiments(
        iters=args.iters,
        timeout=args.timeout,
        verbose=args.verbose
    )

def run_nuxmv_nd_fin_benchmarks(args):
    return nuxmv_nd_fin.run_nuxmv_experiments(
        iters=args.iters,
        timeout=args.timeout,
        verbose=args.verbose,
        allowed_sizes=[args.size]
    )

def run_cpa_benchmarks(args, experiments):
    return cpa.run_cpa_experiment_iters(
        experiments=experiments,
        iters=args.iters,
        timeout=args.timeout,
        verbose=args.verbose
    )

def run_ultimate_det_benchmarks(args, experiments):
    return ultimate_det.run_ultimate_experiment_iters(
        experiments=experiments,
        iters=args.iters,
        timeout=args.timeout,
        verbose=args.verbose
    )

def run_ultimate_nd_inf_benchmarks(args):
    return ultimate_nd_inf.run_ultimate_ltl_experiments(
        iters=args.iters,
        timeout=args.timeout,
        verbose=args.verbose
    )

def run_det_bisimulation_learning(args, experiments):
    return bl_det.run_experiments(
        experiments=experiments,
        iters=args.iters, 
        timeout=args.timeout,
        verbose=args.verbose
    )

def run_brn_bisimulation_learning(args, experiments):
    return bl_brn.run_experiments(
        experiments=experiments,
        explicit_classes=not args.global_rank,
        iters=args.iters,
        timeout=args.timeout,
        verbose=args.verbose
    )
    

def run_clock_benchmarks(args):
    if args.tool == 'nuxmv':
        dataset = []
        phi = 'g' if args.formula == 'safe' else 'gf'
        for prt in ['tte', 'con']:
            for st in ['sf', 'usf']:
                for size in ['10', '100', '1000', '2000', '5000', '10000']:
                    exp = getattr(nuxmv_det, f'exp_{prt}_{st}_{size}_{phi}_{args.mode}')
                    dataset.append(exp())
        return run_nuxmv_det_benchmarks(args, dataset)
    elif args.mode == 'det':
        dataset = []
        for prt in ['tte', 'con']:
            for st in ['sf', 'usf']:
                for size in ['10', '100', '1000', '2000', '5000', '10000']:
                    exp = getattr(bl_det, f'exp_{prt}_{st}_{size}')
                    dataset.append(exp())
        return run_det_bisimulation_learning(args, dataset)
    else:
        dataset = []
        for prt in ['tte', 'con']:
            for st in ['sf', 'usf']:
                exp_fn = getattr(bl_brn, f'{prt}_{st}')
                for size in [10, 100, 1000, 2000, 5000, 10000]:
                    dataset.append((exp_fn(size), f'{prt}_{st}_{size}'))
        return run_brn_bisimulation_learning(args, dataset)

def run_term_benchmarks(args):
    match args.tool:
        case 'nuxmv':
            dataset = []
            if args.formula == 'term':
                dataset = nuxmv_det.term_experiments
            else:
                dataset = nuxmv_det.nonterm_experiments
            return run_nuxmv_det_benchmarks(args, dataset)
        case 'cpa':
            dataset = []
            if args.formula == 'term':
                dataset = cpa.term_experiments
            else:
                dataset = cpa.nonterm_experiments
            return run_cpa_benchmarks(args, dataset)
        case 'ultimate':
            dataset = []
            if args.formula == 'term':
                dataset = ultimate_det.term_experiments
            else:
                dataset = ultimate_det.nonterm_experiments
            return run_ultimate_det_benchmarks(args, dataset)
        case 'bisimulation-learning':
            if args.mode == 'brn':
                dataset = bl_brn.term_experiments
                return run_brn_bisimulation_learning(args, dataset)
            else:
                dataset = bl_det.term_experiments
                return run_det_bisimulation_learning(args, dataset)
        case _:
            raise Exception(f"[ERROR] Unexpected tool: {args.tool}")

def run_nd_inf_benchmarks(args):
    if args.tool == 'nuxmv':
        return run_nuxmv_nd_inf_benchmarks(args)
    elif args.tool == 'ultimate':
        return run_ultimate_nd_inf_benchmarks(args)
    else:
        dataset = bl_brn.nd_inf_experiments
        return run_brn_bisimulation_learning(args, dataset)

def run_nd_fin_benchmarks(args):
    if args.tool == 'nuxmv':
        return run_nuxmv_nd_fin_benchmarks(args)
    else:
        dataset = bl_brn.nd_fin_experiments
        return run_brn_bisimulation_learning(args, dataset)

def run_t2_benchmarks(args):
    if args.tool == 't2':
        raise Exception(f"T2 experiments are to be run in another container.")
    else:
        dataset = bl_brn.t2_experiments
        return run_brn_bisimulation_learning(args, dataset)

def run_benchmarks(args):
    match args.dataset:
        case 'clock':
            return run_clock_benchmarks(args)
        case 'term':
            return run_term_benchmarks(args)
        case 'nd-inf':
            return run_nd_inf_benchmarks(args)
        case 'nd-fin':
            return run_nd_fin_benchmarks(args)
        case 'nd-inf-t2':
            return run_t2_benchmarks(args)
        case _:
            raise Exception(f"Dataset {args.dataset} not implemented yet.")
        
if __name__ == "__main__":
    parser = ArgumentParser("CAV 25 Artifact Evaluation",
        usage=usage)
    parser.add_argument("-d", "--dataset", required=False, help="""
    The dataset to evaluate. Possible values: 'clock', 'term', 'nd-inf', 'nd-fin', 'nd-inf-t2'.
    """)
    parser.add_argument("-t", "--tool", required=False, help="The tool to run on the experiments. Possible values are: 'nuxmv-ic3', 'nuxmv-bdd', 'cpa', 'ultimate', 'bisimulation-learning'")
    parser.add_argument("-f", "--formula", help="The formula to evaluate on the experiments. On 'clock' and 'term' datasets only. Not available on 'bisimulation-learning'. Please refer on the help message for compatibility with the dataset.")
    parser.add_argument("-m", "--mode", help="The tool's mode. Available values: 'ic3', 'bdd' for 'nuxmv' and 'det', 'brn' for 'bisimulation-learning'")
    parser.add_argument("-s", "--size", help="Sizes for the nondeterministic finite state systems. Available state sizes are 9, 11, 13, 15 and 17")
    parser.add_argument("-i", "--iters", help="Number of iterations to run a single test to get the average. Default value is 10")
    parser.add_argument("--timeout", help="Timeout of a single test, in seconds. Default is 300 seconds")
    parser.add_argument("-o", "--output", help="Output csv file. Default is CURRENT_DATE-DATASET-TOOL[-MODE][-FORMULA][-SIZE].csv")
    parser.add_argument("--global-rank", action="store_true", help="In Branching Bisimulation Learning, it enables to use a single ranking function rather than a different ranking function for each class.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints additional messages. Useful for debugging.")
    parser.add_argument("--smoke", action="store_true", help="Runs a smoke test with a single iteration.")
    args = parser.parse_args()


    # args = validate(args)
    # set_output_filename(args)
    # print(pretty_print(args))
    # df = run_benchmarks(args)
    # df.to_csv(args.output)

    try:
        if args.smoke:
            print("Running smoke test...\n")

            print("Running Branching Bisimulation Learning smoke test....")
            bl_brn.run_smoke_test()

            print("Running Deterministic Bisimulation Learning smoke test....")
            bl_det.run_smoke_test()
            print("All smoke tests ran successfully :)")
        else:
            args = validate(args)
            set_output_filename(args)
            print(pretty_print(args))
            df = run_benchmarks(args)
            df.to_csv(args.output)
            print(f"Experiments ran successfully. Results stored in {args.output}")
    except Exception as e:
        print("Error:", e)
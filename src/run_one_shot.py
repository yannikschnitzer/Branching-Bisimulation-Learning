from experiment_runner import run_experiment
from conditional_termination_experiments import *


if __name__ == "__main__":
    run_experiment(exp_term_loop_1(), benchmark_time=True, verbose=True, type="one-shot")


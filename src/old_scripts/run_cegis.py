from bisimulation_learning.deterministic.experiment_runner import *
from bisimulation_learning.deterministic.experiments import *
from bisimulation_learning.deterministic.cegis_solver import *
from z3 import *

if __name__ == "__main__":
    solver = CEGIS_Solver()
    # run_experiment(exp_term_loop_2(), vis=True)
    # DIM 1 
    # run_experiment(exp_audio_compr(), vis=True)
    # run_experiment(exp_euclid(), vis=True)
    # run_experiment(exp_greater(), vis=True)
    # run_experiment(exp_smaller(), vis=True)
    # run_experiment(exp_conic(), vis=True)
    # run_experiment(exp_parallel(), vis=True)
    # exp = exp_disjunction()
    # theta, gamma, eta = solver.solve_experiment(exp)
    # print(theta, gamma, eta)
    # DIM 1 
    # run_experiment(exp_cubic(), vis=True)
    # DIM 1
    # run_experiment(exp_nlr_cond(), vis=True)
    # run_experiment(exp_tte_sf_1000(), vis=True)
    # run_experiment(exp_tte_usf_10(), vis=True)
    # run_experiment(exp_tte_usf_1000(), vis=True)
    run_experiment(exp_con_sf_10(), vis=True)
    # run_experiment(exp_con_usf_10(), vis=True)
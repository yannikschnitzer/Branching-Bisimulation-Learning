from experiment_runner import *
from conditional_termination_experiments import *

if __name__ == "__main__":
    solver = One_Shot_Solver()
    mp, ap, rp = solver.solve_experiment(exp_term_loop_1())
    print(f"""
    Model params (theta)     = {mp}
    Adjacency params (gamma) = {ap}
    Ranking params (theta)   = {rp}
    """)

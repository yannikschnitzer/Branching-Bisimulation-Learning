from experiment_runner import *
from conditional_termination_experiments import *

def run(constructor):
    solver = One_Shot_Solver()
    mp, ap, rp = solver.solve_experiment(constructor())
    print(f"""
    Model params (theta)     = {mp}
    Adjacency params (gamma) = {ap}
    Ranking params (theta)   = {rp}
    """)


if __name__ == "__main__":
    # run(exp_term_loop_2)
    run(exp_audio_compr)
    

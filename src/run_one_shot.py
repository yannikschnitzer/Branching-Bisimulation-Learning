from experiment_runner import *
from conditional_termination_experiments import *
from visualization import *

def run(constructor):
    solver = One_Shot_Solver()
    exp = constructor()
    mp, ap, rp = solver.solve_experiment(exp)
    print(f"""
    Model params (theta)     = {mp}
    Adjacency params (gamma) = {ap}
    Ranking params (theta)   = {rp}
    """)
    visualize(mp, exp, 0.2)
    


if __name__ == "__main__":
    run(exp_term_loop_2)
    # run(exp_audio_compr)
    

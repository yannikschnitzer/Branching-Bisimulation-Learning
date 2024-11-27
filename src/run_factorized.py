from bl_solver.bisimulation_learning import *
from run_factorized_one_shot import *

def run(constructor):
    ts, tem = constructor()
    theta, gamma, eta = bisimulation_learning(ts, tem)
    print(f"""
    Model params (theta)     = {theta}
    Adjacency params (gamma) = {gamma}
    Ranking params (theta)   = {eta}
    """)
    draw_template(gamma, tem)
    visualize_template(theta, tem)

if __name__ == "__main__":
    # run(audio_compr)
    run(euclid)

from bl_solver.template import *
from bl_solver.conditions import *

def one_shot_deterministic(
    transition_system: DeterminsticTransitionSystem,
    template: BDTTemplate
    ):
    
    model_params     = template.model_params
    adjacency_params = template.adjacency_params
    s                = template.m
    succ_s           = template.succ_m

    formulas = []

    print("Using deterministic formulas")
    ranking_params   = template.rank_params
    # formuals contain both cond_1 and cond_2
    formulas = encode_classification(
        transition_system=transition_system,
        template=template,
        proof_rules=conds_wbs_deterministic,
        theta=model_params,
        gamma=adjacency_params,
        eta=ranking_params,
        s=s,
        succ_s=succ_s
    )

    formula = ForAll([*s, *succ_s],
        And([simplify(phi) for phi in formulas])
    )

    solver = Solver()
    solver.add(formula)


    res = solver.check()
    if f"{res}" == "sat":
        print("Found a solution!")
        return True, extract_solution(solver, template)
    else:
        return False, None

def one_shot_namjoshi(
    transition_system: BranchingTransitionSystem,
    template: BDTTemplate,
    ):

    print("Using branching formulas namjoshi")

    model_params     = template.model_params
    s                = template.m
    succ_s           = template.succ_m
    w                = template.w
    ranking_params   = template.rank_params_branching_global

    formulas = encode_classification_branching(
        transition_system=transition_system,
        template=template,
        theta=model_params,
        eta=ranking_params,
        s=s, succ_s=succ_s, w=w,
        explicit_classes=False
    )

    formula = ForAll([*s, *succ_s, *w],
        And([simplify(phi) for phi in formulas])
    )

    solver = Solver()
    solver.add(formula)

    res = solver.check()

    if f"{res}" == "sat":
        print("Found a solution!")
        m = solver.model()
        theta = [m.evaluate(param) for param in model_params]
        rankp = [[m.evaluate(param) for param in l] for l in ranking_params]
        adj = compute_adjacency_matrix(transition_system, template, theta)
        return True, (theta, adj, rankp)
    else:
        return False, None

def encode_one_shot_additional(
    transition_system: DeterminsticTransitionSystem,
    template: BDTTemplate,
    theta, gamma, eta, 
    s, succ_s
    ):

    phis = []

    successor = transition_system.successor
    domain    = transition_system.domain
    f, g, h   = template.get_template_functions()

    for p in template.partitions:
        phis.append(Implies(
            And(g(gamma, p, p) == IntVal(1),
                f(theta, s) == p,
                successor(s, succ_s),
                domain(s), 
                domain(succ_s)
            ), 
            f(theta, succ_s) == p
        ))
    
    return phis
    

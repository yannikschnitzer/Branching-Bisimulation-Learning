import numpy as np

from bisimulation_learning.shared.utils import *
from bisimulation_learning.shared.binary_decision_trees import *

class DeterminsticTransitionSystem:
    def __init__(self, dim, successor, domain = None):
        self.dim = dim
        self.successor = successor
        if domain is None:
            def const_true(x):
                return True
            self.domain = const_true
        else:
            self.domain = domain
    
    def to_branching(self):
        def successors(x):
            return [self.successor(x)]
        return BranchingTransitionSystem(self.dim, successors, self.domain)

class BranchingTransitionSystem:
    def __init__(self, dim, successors, domain):
        self.dim = dim
        self.successors = successors
        self.domain = domain


class BDTTemplate:

    def __init__(self, 
        dim,
        bdt_classifier: BDTNodePoly,
        num_params, 
        num_coefficients, 
        num_partitions
        ):
        """
        Proposes a new template for a given transition system
        """

        # configuration of wanted abstract system
        self.num_partitions   = num_partitions
        self.num_coefficients = num_coefficients
        self.num_params       = num_params
        self.bdt_classifier   = bdt_classifier
        
        self.setup_smt_parameters(dim)
        self.setup_adjacency()

    def setup_smt_parameters(self, dim):
        """
            Function returns the requested number of SMT parameters.
            Sets up for the current object:
                - m: State variable of specified dimension
                - p,q: Abstract state variables
                - partitions: List of classes, i.e., abstract states, numbered from 0 to num_partitions - 1
                - adjacency_params: Booleans of the form a_i_j, for an abstract edge between partitions i and j
                - model_params: Real valued coefficients and predicate parameters for the BDT classifier templates
                - rank_params: Real valued coefficients and constatns for the ranking function templates
        """
        # dimension of state variable

        self.m = [Int("m_%s" % i) for i in range(dim)]
        self.succ_m = [Int("succ_m_%s" % i) for i in range(dim)]
        self.w = [Int("w_%s" % i) for i in range(dim)] # only for branching wfbs
        self.succ_w = [Int("succ_w_%s" % i) for i in range(dim)] # only for branching wfbs
        self.p = Int("p")
        self.q = Int("q")

        self.partitions = [i for i in range(self.num_partitions)]
        # NOTE: adjacency (and gamma as well) is not needed for branching systems
        self.adjacency_params = [[Bool("a_%s_%s" % (i, j)) for j in range(len(self.partitions))] for i in range(len(self.partitions))]
        self.model_params = [Real("p_%s" % i) for i in range(self.num_params)] + [Real("a_%s" % i) for i in range(self.num_coefficients)]
        self.rank_params = [[Real("u_%s_%s" % (d, i)) for d in range(dim)] + [Real("c_%s" % i)] for i in range(self.num_partitions)]
        
        # linear ranking function
        self.rank_params_branching_global = [[Real("u_0_%s" % d) for d in range(dim)], [Real("u_1_%s" % d) for d in range(dim)]]
    
    def setup_adjacency(self):
        """
            Initialize adjacency parameters
        """
        self.adj_exprs = [[self.adjacency(self.adjacency_params,p,q) for q in range(self.num_partitions)] for p in range(self.num_partitions)]

    def adjacency(self, params, p, q): 
        return self.generate_adjacency(p,q,0,0,params,self.num_partitions - 1)
   
    def generate_adjacency(self, p, q, i , j, params, mx):
        if i == mx and j == mx:
            return simplify(If(And(p == i, q == j),If(params[i][j],1,0),0))
        elif i <= mx and j < mx:
            return simplify(If(And(p == i, q == j), If(params[i][j],1,0), self.generate_adjacency(p,q,i,j+1,params,mx)))
        elif i < mx and j == mx:
            return simplify(If(And(p == i, q == j), If(params[i][j],1,0), self.generate_adjacency(p,q,i+1,0,params,mx)))
 
    def get_template_functions(self, branching = False):
        def f(theta, s):
            classification_formula, _ = self.bdt_classifier(theta, s, self.num_params, self.partitions)
            return classification_formula
        
        def g(gamma, p, q):
            return gamma[p][q]
        
        def h_det(eta, p, s):
            return np.dot(eta[p][:-1], s) + eta[p][-1]
        
        def h_brn(eta, s_0, s_1):
            # TODO do we need coefficient?
            return np.dot(eta[0], s_0) + np.dot(eta[1], s_1)
        
        if branching:
            return f, g, h_brn
        else:
            return f, g, h_det
        

def encode_classification(
    transition_system: DeterminsticTransitionSystem,
    template: BDTTemplate,
    proof_rules, # function taking all the parameters and returning a list of functions
    theta, gamma, eta, 
    s, succ_s
    ):

    f, g, h = template.get_template_functions(branching=False)

    phis = []

    for p in template.partitions:
        for q in template.partitions:
            phis += proof_rules(
                successor=transition_system.successor,
                domain=transition_system.domain,
                f=f,
                g=g,
                h=h,
                theta=theta,
                gamma=gamma,
                eta=eta,
                s=s,
                succ_s=succ_s,
                p=p,
                q=q
            )
                
    
    return phis


def compute_adjacency_matrix(
    transition_system: BranchingTransitionSystem,
    template: BDTTemplate, 
    theta
    ):

    partitions       = template.partitions
    model_params     = template.model_params
    rank_params      = template.rank_params_branching_global

    adjacency_matrix = [[False for c in partitions] for d in partitions]

    for c in partitions:
        for d in partitions:
            if c != d:
                adjacency_matrix[c][d] = quotient_has_transition(
                    transition_system,
                    template,
                    theta,
                    c, 
                    d
                )
            else:
                adjacency_matrix[c][d] = quotient_self_loop(
                    transition_system,
                    template,
                    theta,
                    c
                )

    return adjacency_matrix

def quotient_has_transition(
    transition_system: BranchingTransitionSystem, 
    template: BDTTemplate,
    theta,
    c, d
    ):
    assert(c != d)

    successors = transition_system.successors
    f, _, _ = template.get_template_functions()
    s = template.m
    
    solver = Solver()
    formula = And(
        f(theta, s) == c,
        Or([f(theta, u) == d for u in successors(s)])
    )
    solver.add(formula)
    res = solver.check()
    if f"{res}" == "sat":
        return True
    else:
        assert(f"{res}" == "unsat")
        return False

def quotient_self_loop(
    transition_system: BranchingTransitionSystem, 
    template: BDTTemplate,
    theta,
    c
    ):

    successors = transition_system.successors
    s = template.m

    f, _, _ = template.get_template_functions()
    
    solver = Solver()

    formula = And(
        f(theta, s) == c,
        And([f(theta, u) != c for u in successors(s)])
    )

    solver.add(formula)
    res = solver.check()
    if f"{res}" == "sat":
        return False
    else:
        assert(f"{res}" == "unsat")
        return True


def extract_quotient_cex(conds: list, s, succ_s):
    solver = Solver()
    solver.add(simplify(Or([simplify(Not(cond)) for cond in conds])))
    resc = solver.check()
    if f"{resc}" == "sat":
        model = solver.model()
        cex = [model.evaluate(d) for d in s]
        succ_cex = [model.evaluate(d) for d in succ_s]
        raise Exception(f"No quotient system was synthetized. Counterexample state was {cex} -> {succ_cex}")
    else:
        raise Exception(f"No solution for the quotient system nor counterexample found. Satisfiability result was {resc}")

def extract_solution(s: Solver, template: BDTTemplate, verbose = False):
    """
        Extract obtained solution from the solver
    """
    # sat = s.check()
    if verbose: print("Checking #Constraints:", len(s.assertions()))
    if verbose: print("Result:", sat)

    partitions       = template.partitions
    model_params     = template.model_params
    adjacency_params = template.adjacency_params
    rank_params      = template.rank_params

    m = s.model()
    adj = [ [ m.evaluate(adjacency_params[i][j]) for j in range(len(partitions)) ] for i in range(len(partitions)) ]
    params = [m.evaluate(param) for param in model_params]
    rankp = [[m.evaluate(param) for param in l] for l in rank_params]

    if verbose:
        print("Obtained BDT Parameters:")
        for i in range(len(params)):
            if not(type(params[i]) == ArithRef):
                print(model_params[i],":", decimal(params[i]))
            else:
                print(model_params[i],":", "-") #params[i])
        
        print("Obtained Ranking Parameters:")
        for i in range(len(rankp)):
            for j in range(len(rankp[i])):
                if not(type(rankp[i][j]) == ArithRef):
                    print(rank_params[i][j],":", decimal(rankp[i][j]))
                else:
                    print(rank_params[i][j],":", "-")#rankp[i][j])
    
    return params, adj, rankp

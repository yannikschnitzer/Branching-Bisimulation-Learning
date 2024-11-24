import numpy as np

from utils import *

from bl_solver.conditions import *
from bl_solver.transition_system import *

class ProposedTemplate:

    def __init__(self, dim, abstract_system):
        """
        Proposes a new template for a given transition system
        """
        self.setup_smt_parameters(dim, abstract_system)
        self.setup_adjacency()
        # TODO setup BDT classifier

    def setup_smt_parameters(self, dim, abstract_system  : AbstractSystem):
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

        # configuration of wanted abstract system
        self.num_partitions   = abstract_system.num_partitions
        self.num_coefficients = abstract_system.num_coefficients
        self.num_params       = abstract_system.num_params

        self.bdt_classifier   = abstract_system.bdt_classifier

        self.m = [Int("m_%s" % i) for i in range(dim)]
        self.succ_m = [Int("succ_m_%s" % i) for i in range(dim)]
        self.p = Int("p")
        self.q = Int("q")

        self.partitions = [i for i in range(self.num_partitions)]
        self.adjacency_params = [[Bool("a_%s_%s" % (i, j)) for j in range(len(self.partitions))] for i in range(len(self.partitions))]
        self.model_params = [Real("p_%s" % i) for i in range(self.num_params)] + [Real("a_%s" % i) for i in range(self.num_coefficients)]
        self.rank_params = [[Real("u_%s_%s" % (j, i)) for j in range(dim)] + [Real("c_%s" % i)] for i in range(self.num_partitions)]
    
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
 
    def get_template_functions(self):
        def f(theta, s):
            classification_formula, _ = self.bdt_classifier(theta, s, self.num_params, self.partitions)
            return classification_formula
        
        def g(gamma, p, q):
            return gamma[p][q]
        
        def h(eta, p, s):
            return np.dot(eta[p][:-1], s) + eta[p][-1]
        
        return f, g, h
        

def encode_classification(
    transition_system: TransitionSystem,
    proposed_template: ProposedTemplate,
    theta, gamma, eta, 
    s, succ_s
    ):

    f, g, h = proposed_template.get_template_functions()

    phis = []

    for p in proposed_template.partitions:
        for q in proposed_template.partitions:
            if q != p:
                # when they are equal we can 
                # we can omit both conditions
                phis.append(cond_1(
                    successor=transition_system.successor,
                    domain=transition_system.domain,
                    f=f,
                    g=g,
                    theta=theta,
                    gamma=gamma,
                    s=s,
                    succ_s=succ_s,
                    p=p,
                    q=q
                ))
                phis.append(cond_2(
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
                ))
    
    return phis
                    
def extract_solution(s: Solver, proposed_template: ProposedTemplate, verbose = True):
    """
        Extract obtained solution from the solver
    """
    sat = s.check()
    if verbose: print("Checking #Constraints:", len(s.assertions()))
    if verbose: print("Result:", sat)

    partitions       = proposed_template.partitions
    model_params     = proposed_template.model_params
    adjacency_params = proposed_template.adjacency_params
    rank_params      = proposed_template.rank_params

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

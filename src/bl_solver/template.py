from bl_solver.conditions import *

class ProposedTemplate:

    def __init__(self, transition_system):
        """
        Proposes a new template for a given transition system
        """
        self.transition_system = transition_system
        self.setup_smt_parameters()

    def setup_smt_parameters(self):
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
        dim = self.transition_system.state_dim
        num_partitions = self.transition_system.num_partitions
        
        # TODO
        num_coefficients = None
        num_params = None
        # TODO num coefficients and params?

        self.m = [Int("m_%s" % i) for i in range(dim)]
        self.succ_m = [Int("sycc_m_%s" % i) for i in range(dim)]
        self.p = Int("p")
        self.q = Int("q")

        self.partitions = [IntVal(i) for i in range(num_partitions)]
        self.adjacency_params = [[Bool("a_%s_%s" % (i, j)) for j in range(len(self.partitions))] for i in range(len(self.partitions))]
        self.model_params = [Real("p_%s" % i) for i in range(num_params)] + [Real("a_%s" % i) for i in range(num_coefficients)]
        self.rank_params = [[Real("u_%s_%s" % (j, i)) for j in range(dim)] + [Real("c_%s" % i)] for i in range(num_partitions)]

def encode_classification(
    proposed_template: ProposedTemplate,
    theta, gamma, eta, s, succ_s):

    transition_system = proposed_template.transition_system

    phis = []

    for p in proposed_template.partitions:
        for q in proposed_template.partitions:
            if q != p:
                # when they are equal we can 
                # we can omit both conditions
                phis.append(cond_1(
                    successor=transition_system.successor,
                    domain=transition_system.domain,
                    f=proposed_template.classify,
                    g=proposed_template.adjacent,
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
                    f=proposed_template.classify,
                    g=proposed_template.adjacent,
                    h=proposed_template.rank,
                    theta=theta,
                    gamma=gamma,
                    eta=eta,
                    s=s,
                    succ_s=succ_s,
                    p=p,
                    q=q
                ))
    
    return phis
                    
def extract_solution(s: Solver, proposed_template: ProposedTemplate):
    """
        Extract obtained solution from the solver
    """
    sat = s.check()
    if verbose: print("Checking #Constraints:", len(s.assertions()))
    if verbose: print("Result:", sat)
    ## TODO what if it is not satisfied?

    partitions   = proposed_template.partitions
    model_params = proposed_template.model_params
    rank_params  = proposed_template.rank_params

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

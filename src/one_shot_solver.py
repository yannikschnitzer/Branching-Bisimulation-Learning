
import time
from utils import *
from experiment import Experiment
from visualization import *
from z3 import *
from conditional_termination_succ_trees import *
import matplotlib.pyplot as plt

class Conditions:
    """
    Represents an instance of the conditions formulas for Theorem 3
    given a fixed transition system, i.e. passing as arguments of 
    the class constructor:
        - the successor function;
        - the domain constraint for the states of the given system;
        - the classification BDT.
    
    Condition functions' arguments are:
        - theta: parameters of the classification BDT, i.e. the parameters for f(theta; s);
        - gamma: parameters of adjacency, in this case a function s.t. gamma(p, q) == 1 iff g(p) = q;
        - eta: parameters for the ranking function;
    Those preceding arguments are the parameters for the formulas in the paper. Follow now the formula arguments:
        - s: the state to check te formula against
    Now follow the classification expectations:
        - p: the classification of s
        - q: the classification of T(s)
    """
    def __init__(self, successor, domain, classify):
        self.successor = successor
        self.domain = domain
        self.classify = classify

    # TODO rename in condition 2 (Phi_2)
    def condition_1(self, theta, gamma, eta, s, p, q):
        """
        Represents formula Phi_1 given state p and q to check, i.e. Condition 2 of Theorem 3.
        To see what the arguments are, refer to the class' description.

        Note that in this case, eta is unused since there is no ranking function
        but it is declared to make the function definition consistent as in the paper.
        """
        return Implies(
            And(self.classify(theta, s) == p, 
                self.classify(theta, self.successor(s)) == q, 
                self.domain(s), 
                self.domain(self.successor(s)), 
                (Not(p == q))
            ), 
            gamma(p, q) == 1
        )
    
    # TODO rename in condition 1
    def condition_2(self, theta, gamma, rank, s, p, q):
        """
        Represents Phi_2 given state p and q to check, i.e. Condition 3 of Theorem 3.
        To see what the arguments are, refer to the class' description.
        """
        return And(
            Implies(
                And(gamma(p, q) == 1, 
                    Not(p == q),
                    self.classify(theta, s) == p, 
                    self.domain(s), 
                    self.domain(self.successor(s))
                ), 
                Or( self.classify(theta, self.successor(s)) == q,
                    And(self.classify(theta, self.successor(s)) == p,
                        rank(p, s) > rank(p, self.successor(s))
                    )
                )    
            ),
            # TODO not quite sure from where is this from
            Implies(
                And(gamma(p, q) == 1, 
                    (p == q)
                ), 
                Implies(
                    And(self.classify(theta, s) == p, 
                        self.domain(s), 
                        self.domain(self.successor(s))
                    ), 
                    self.classify(theta, self.successor(s)) == p)
                )
        )


class One_Shot_Solver:
    """
        One-Shot SMT Solver for stutter-insensitive bisimulation conditions with ranking functions.

        Fixes one experiment and then solves it
    """
    def __init__(self, name = "One-Shot Solver"):
        self.name = name

    def solve_experiment(self, exp : Experiment, verbose = True):
        """
            One-shot solve a given experiment. Once an experiment it's fixed,
            it also fixes:
                - the classifier BDT
                - the number of BDT parameters and coefficients
                - the number of partitions
            (and hence, the self.classify function)
                - the transition (successor) function
                - the number of state variables
                - the domain of the state base
                - 

            Returns:
                - bdt_params: Obtained parameters for the given BDT template
                - abs_trans: Obtained abstract transition matrix
                - rank_params: Obtained parameters for the given ranking function templates.
        """
        # Model functions and parameter 
        ## f
        self.classifier = exp.classifier
        ## theta
        self.num_params = exp.num_params
        self.num_coefficients = exp.num_coefficients
        
        ## Number of states of abstract TS
        self.num_partitions = exp.num_partitions

        # Concrete transition system parameters
        self.successor = exp.successor
        self.domain = exp.domain
        self.dim = exp.dim # dimension of state variable

        # Initializes the parameters to learn and verify
        self.setup_smt_parameters()

        self.conditions = Conditions(self.successor, self.domain, self.classify)

        mp, ap, rank = self.solve()
        if verbose:
            print(f"One shot solver found following result")
            print(f"Model params = {mp}")
            print(f"Adjacency params = {ap}")
            print(f"Ranking params = {rank}")
        return mp, ap, rank

    def solve(self):

        # TODO it should be the same, shouldn't they?
        # self.num_partitions = len(self.partitions)
        # assert (self.num_partitions == len(self.partitions))

        # SMT Solver
        solver = Solver()

        # Add Stutter-Insensitive Bisimulation conditions with ranking functions
        self.cond_1_one_shot(solver)
        self.cond_2_one_shot(solver)

        mp, ap, rankp = extract_learner(solver, self.model_params, self.adjacency_params, self.rank_params, self.partitions)
        return mp, ap, rankp

    def cond_1_one_shot(self, solver):
        """
            Condition 1 of a stutter-insensitive bisimulation - Concrete transitions imply abstract transitions
        """
        phi_1 = self.conditions.condition_1(
            theta=self.model_params,
            gamma=self.gamma,
            eta=self.rank,
            s=self.m,
            p=self.p,
            q=self.q
        )
        solver.add(simplify(
            ForAll([*self.m, self.p, self.q], phi_1)
        ))

    def cond_2_one_shot(self, solver):
        """
            Condition 2 of a stutter-insensitive bisimulation with ranking functions - abstract transitons imply concrete transition or intra-class ranking transition
        """
        phi_2 = self.conditions.condition_2(
            theta=self.model_params,
            gamma=self.gamma,
            rank=self.rank,
            s=self.m,
            p=self.p,
            q=self.q
        )
        solver.add(simplify(
            ForAll([*self.m, self.p, self.q], phi_2)
        ))

    # TODO that can be extracted into another class to reproduce the code in CEGIS 
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
        self.m = [Int("m_%s" % i) for i in range(self.dim)]
        self.p = Int("p")
        self.q = Int("q")

        self.partitions = [IntVal(i) for i in range(self.num_partitions)]
        self.adjacency_params = [[Bool("a_%s_%s" % (i, j)) for j in range(len(self.partitions))] for i in range(len(self.partitions))]
        self.model_params = [Real("p_%s" % i) for i in range(self.num_params)] + [Real("a_%s" % i) for i in range(self.num_coefficients)]
        self.rank_params = [[Real("u_%s_%s" % (j, i)) for j in range(self.dim)] + [Real("c_%s" % i)] for i in range(self.num_partitions)]


    def classify(self, params, x):
        f, _ = self.classifier(params, x, self.num_params, self.partitions)
        return f

    def gamma(self, p, q):
        return self.adjacency(self.adjacency_params, p, q)

    def generate_adjacency(self, p, q, i , j, params, mx):
        if i == mx and j == mx:
            return simplify(If(And(p == i, q == j),If(params[i][j],1,0),0))
        elif i <= mx and j < mx:
            return simplify(If(And(p == i, q == j), If(params[i][j],1,0), self.generate_adjacency(p,q,i,j+1,params,mx)))
        elif i < mx and j == mx:
            return simplify(If(And(p == i, q == j), If(params[i][j],1,0), self.generate_adjacency(p,q,i+1,0,params,mx)))

    def adjacency(self, params, p, q): 
        return self.generate_adjacency(p,q,0,0,params,self.num_partitions - 1)
    
    def generate_rank(self, p, x, params, i):
        if i == len(params)-1: 
            return np.dot(params[i][:-1], x) + params[i][-1]
        return simplify(If(p == i, np.dot(params[i][:-1], x) + params[i][-1], self.generate_rank(p, x, params, i+1)))

    def rank(self, p, x):
        return self.generate_rank(p, x, self.rank_params, 0)

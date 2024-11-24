class TransitionSystem:
    def __init__(self, dim, successor, domain):
        self.dim = dim
        self.successor = successor
        self.domain = domain
    
class AbstractSystem:
    def __init__(self, 
        num_partitions, 
        num_params,
        num_coefficients, 
        bdt_classifier # function that returns both BDT and BDT.formula()
        ):

        self.num_partitions   = num_partitions
        self.num_params       = num_params 
        self.num_coefficients = num_coefficients
        self.bdt_classifier   = bdt_classifier

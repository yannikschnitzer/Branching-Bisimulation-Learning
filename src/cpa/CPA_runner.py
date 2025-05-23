"""
    CPAChecker experiments and commandline access.
"""
import subprocess
import re

__author__ = "Yannik Schnitzer"
__copyright__ = "Copyright 2024, Yannik Schnitzer"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "yannik.schnitzer@cs.ox.ac.uk"
__status__ = "Experimental - Artifact Evaluation"

class CPA_Experiment:
    def __init__(self, name, file, print_res = False):
        self.name = name
        self.file = file
        self.print_res = print_res

def run_cpa_experiment(exp : CPA_Experiment):
        """
            Runs CPA Checker with given experiment.
        """
        cmd = "cpa ../C-Programs/" + exp.file

        print("------------------------------------")
        print("Running Experiment: ", exp.name)
        out = subprocess.check_output(cmd, shell = True, text = True)
        time_pattern = r"Time for Analysis:\s+(\d+\.\d+)s"
        matches = re.findall(time_pattern, out)
        if matches:
            print("CPA Checker Analysis Time:", matches[0],"")
            return float(matches[0])
        else:
            raise Exception("Unknown error (time pattern got no matches)")

        if exp.print_res:
            res_pattern = r"Verification result: (TRUE|FALSE|UNKNOWN)"
            matches = re.findall(res_pattern, out)
            if matches:
                print("Verification result:", matches[0])
        print("------------------------------------")


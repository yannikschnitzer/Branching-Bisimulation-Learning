"""
    nuXmv exeperiments and command line access.
"""

import subprocess
import os
import multiprocessing
import time

__author__ = "Yannik Schnitzer"
__copyright__ = "Copyright 2024, Yannik Schnitzer"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "yannik.schnitzer@cs.ox.ac.uk"
__status__ = "Experimental - Artifact Evaluation"

class nuXmv_Experiment:
    def __init__(self, name, file, print_res = False):
        self.name = name
        self.file = file
        self.print_res = print_res


def run_subprocess(cmd: str, timeout=300) -> bytes:
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = p.communicate(timeout=timeout)
        return out
    except subprocess.TimeoutExpired as e:
        p.kill()
        raise e

def run_nuXmv_experiment(exp : nuXmv_Experiment, timeout = 300, verbose = False):
    """
        Runs nuXmv with given experiment.
    """
    cmd = "nuxmv -source ../nuXmv-files/" + exp.file
    

    if verbose:
        print("------------------------------------")
        print("Running Experiment: ", exp.name)
    
    t1 = time.perf_counter()
    # subprocess.check_output(cmd, shell = True, text = True, stderr=subprocess.DEVNULL, timeout=timeout)
    run_subprocess(cmd, timeout)
    t2 = time.perf_counter()
    
    runtime = t2 - t1
    if verbose:
        print("Runtime: ", runtime,"seconds")
        print("------------------------------------")
    return runtime


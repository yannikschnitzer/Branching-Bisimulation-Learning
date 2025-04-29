"""
    Ultimate Automizer experiments and commandline access.
"""

import subprocess
import os
import re

__author__ = "Yannik Schnitzer"
__copyright__ = "Copyright 2024, Yannik Schnitzer"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "yannik.schnitzer@cs.ox.ac.uk"
__status__ = "Experimental - Artifact Evaluation"

class Ultimate_Experiment:
    def __init__(self, name, file, print_res = False):
        self.name = name
        self.file = file
        self.print_res = print_res

def run_ultimate_experiment(exp : Ultimate_Experiment):
        """
            Runs Ultimate with given experiment.
        """
        cmd = "sudo update-java-alternatives --set java-1.21.0-openjdk-amd64 && ../../ultimate/releaseScripts/default/UAutomizer-linux/Ultimate -tc ../../ultimate/releaseScripts/default/UAutomizer-linux/config/AutomizerTermination.xml -i ../C-Programs/" + exp.file
        os.system("")
        print("------------------------------------")
        print("Running Experiment: ", exp.name)
        out = subprocess.check_output(cmd, shell = True, text = True, stderr=subprocess.DEVNULL)
        time_pattern = r"Automizer plugin needed (\d+\.\d+)"
        matches = re.findall(time_pattern, out)
        if matches:
            print("Ultimate Automizer Analysis Time:", matches[0],"")
            return float(matches[0])
        else:
            raise Exception("No match")

        if exp.print_res:
            res_pattern = r"TerminationAnalysisResult: (.*)"
            matches = re.findall(res_pattern, out)
            if matches:
                print("Verification result:", matches[0])
        print("------------------------------------")

def run_ultimate_experiment(exp: Ultimate_Experiment) -> float:
    """
    Runs Ultimate with the given experiment, first switching the system Java.
    Raises on any failure in switching Java or in parsing Ultimate’s output.
    """
    java_name = "java-1.21.0-openjdk-amd64"
    java_cmd = ["sudo", "update-java-alternatives", "--set", java_name]

    # 1) Switch Java and fail loudly if it doesn’t work
    try:
        print(f"Switching Java to {java_name!r}…")
        subprocess.check_call(java_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        # e.returncode is non-zero; e.output may be None here because check_call doesn’t capture it
        raise RuntimeError(f"Failed to switch Java (exit code {e.returncode}). "
                           f"Please try switching manually by running: sudo update-java-alternatives --set java-1.21.0-openjdk-amd64 ") from e

    # 2) Build the Ultimate command as a list
    base = os.path.join("..", "..", "ultimate", "releaseScripts", "default", "UAutomizer-linux")
    ultimate_exe = os.path.join(base, "Ultimate")
    config_file = os.path.join(base, "config", "AutomizerTermination.xml")
    input_file = os.path.join("..", "C-Programs", exp.file)

    cmd = [
        ultimate_exe,
        "-tc", config_file,
        "-i",  input_file
    ]

    print("------------------------------------")
    print(f"Running Experiment: {exp.name!r}")
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ultimate failed (exit {e.returncode}). Output:\n{e.output}") from e

    # 3) Parse the Automizer time
    time_pattern = r"Automizer plugin needed (\d+\.\d+)"
    m = re.search(time_pattern, out)
    if not m:
        raise RuntimeError("Could not find Automizer plugin time in Ultimate output.")
    analysis_time = float(m.group(1))
    print("Ultimate Automizer Analysis Time:", analysis_time)

    return analysis_time
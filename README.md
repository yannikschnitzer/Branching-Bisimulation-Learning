
# Branching Bisimulation Learning

This is the artifact for the paper **"Branching Bisimulation Learning"** (CAV 2025). 

The corresponding Git repository is: https://github.com/yannikschnitzer/Branching-Bisimulation-Learning

We claim the artifact to be available, functional and reusable. We describe the structure and usage below.




![alt text](https://i.postimg.cc/KjggVQ7r/quotient.png)
![alt text](https://i.postimg.cc/BQ064qJG/Screenshot-2025-04-04-at-10-45-36.png)
## Artifact Requirements

The artifact comes as `Dockerfiles`, which automatically set up a container containing all relevant files, software, and dependencies. Due to incompatible requirements for some of the baseline tools, we split the artfact into two seperate Dockerfiles, we elaborate their structure and usage below. 

The artifact contains our software and third-party software used internally or as baselines for comparison. Neither of them requires an excessive amount of resources. We recommend the following minimal specifications:
* **CPU**: Intel Xeon 3.3GHz 8-core 
* **RAM**: 16GB
* **Disk Space**: 32GB

**Remark**: To run the baseline comparison with the *Ultimate Automizer* tool, an x86 architecture is required.

The setup via Docker installs all required software and dependencies. As the baseline tools and some used libraries are extensive, this may take a while. On our machines, the setup took up to an hour to complete.

The artifact can run the experiments separately, i.e., produce the individual columns of the tables. This may require a significant amount of runtime, especially when experiments will time out. In our evaluation, we used a timeout of 500 seconds, implying that the complete experiments may take up to ~10 hours. For a quicker evaluation, we allow a custom timeout (e.g., 60 seconds) to be set, sufficient to show the orders of magnitude.

## Structure and Content

The artifact contains two `Dockerfiles`, one for the **T2** baseline tool and one for all other tools and baselines (due to requirement incompatability). The Dockerfiles automatically set up the environment for evaluation. The environment is structured as follows

* **CAV25** - Main Folder containing the artifact.
  * ***Branching-Bisimulation-Learning***: Repository containing our implementation and experiments.
    * **src**: Source code for our tool.
      * *run.py*: Main file for running experiments from command line.
      * *benchmark_det.py*: Main file for running Bisimulation Learning on deterministic experiments.
      * *benchmark_nd.py*: Main file for running Bisimulation Learning on non-deterministic (branching) experiments.
      * **bisimulation_learning**
        * **deterministic**
          * **experiments**: Definitions for the deterministic experiments (Table 1 and Table 2).
          <!--
                * *conditional_termination_succ_trees.py*: Contains one-step transitions functions and BDT templates for the conditional termination benchmarks (Table 2).
                * *clock_synchronization_succ_trees.py*: Contains one-step transitions functions and BDT templates for the conditional termination benchmarks (Table 1).
                * *conditional_termination_experiments.py*: Defines the experiments to run for producing the results in Table 2 (Bisimulation Learning column).
                *  *clock_synchronization_experiments.py*: Defines the experiments to run for producing the results in Table 1 (Bisimulation Learning column).
          -->
          * *cegis_solver.py*: Contains main algorithms and procedures for deterministic Bisimulation Learning. 
          * *experiment_runner.py*: Toolchain for running deterministic experiments, benchmarking time and subsequently saving/visualizing the results.
        * **finitely_branching**
          * **experiments** Definitions for the non-deterministic experiments (Table 3, Table 4 and Table 5).
          * *cegis_solver.py*: Contains main algorithms and procedures for non-deterministic Bisimulation Learning. 
          * *conditions.py*: Contains the conditions formulas for stuttering bisimulations.
        * **shared**
          * *experiment.py*: Experiment class for defining experiments and parameters.
          * *visualization.py*: Toolchain for visualizing the resulting partitions of 2D experiments.
          * *utils.py*: Utility functions for type conversion, result extraction and visualization.
          * *binary_decision_trees.py*: BDT class representing binary decision trees with aribtrary real-valued predicates and a special class for linear predicates.
          * *utils.py*: Some helper functions.
      *  **nuxmv**
         *  *nuxmv_experiments.py*: Experiment class for defining deterministic experiments and parameters that are passed to the nuXmv baseline tool.
         *  *nuXmv_runner.py*: Toolchain for running deterministic experiments and benchmarking time for nuXmv.
         * *benchmarks_nd_inf.py*: Contains definitions for the non-deterministic infinite-state space benchmarks base, and the toolchain to run them.
         * *benchmarks_nd_inf.py*: Contains definitions for the non-deterministic finite-state space benchmarks base, and the toolchain to run them.
      *  **ultimate**
         *  *ultimate_experiments.py*: Experiment class for defining deterministic experiments and parameters that are passed to the Ultimate Automizer baseline tool.
         *  *ultimate_runner.py*: Toolchain for running deterministic experiments and benchmarking time for the Ultimate Automizer.
      *  **ultimate-ltl**
         * *benchmarks.py*: Contains definitions for the non-deterministic benchmarks base, the LTL formulas and the toolchain to run them with.
      *  **cpa**
         *  *CPA_experiments.py*: Experiment class for defining experiments and parameters that are passed to the CPAChecker baseline tool.
         *  *CPA_runner.py*: Toolchain for running experiments and benchmarking time for the CPAChecker.
      *  **<span style="color:red">t2-prover</span>**: A separate folder for T2 benchmarks. It has its own readme and the **<span style="color:red">second Dockerfile</span>**.
     *  **nuXmv-Files**: Contains the used benchmarks as SMV files to be used with the nuXmv model checker. 
     *  **C-Programs**: Contains the sued benchmarks as C programs to be used with Ultimate Automizer and CPA Checker.
  * ***nuXMv-2.0.0***: Baseline tool **nuXmv** used for symbolic model checking via BDDs and IC3 for infinite state systems. Also used for termination analysis.
  * ***ultimate***: Baseline tool **Ultimate Automizer**  used for termination analysis of C programs. 
  * ***CPA-Checker***: Baseline tool **CPA Checker** used for termination analysis of C programs.


## Getting Started

After unpacking the artifact, the main `Dockerfile` in the **/CAV25** base directory can be turned into an image by running:

```bash
docker build -t bisimulation-learning .
```

in the directoy of the file. As described above, the setup may take a while to install all dependencies and baseline tools (in the range of 2h, depending on your system). 

The image can be run in a container by executing:

```bash
docker run --name=bisimulation-learning -it bisimulation-learning 
```

After the setup, the container should start in the `CAV25/Branching-Bisimulation-Learning/src` folder, whose structure is described in the **Structure and Content** section.

---

The main file for running all experiments is `CAV25/Branching-Bisimulation-Learning/src/run.py`, which can be run from the `src` directory with:
```bash
python3 run.py 
```

or, since it is itself an executable:

```bash
./run.py
```

The `run.py` file can take multiple arguments defining which experiments to run:

### Smoke-Test 

The smoke test will run one benchmark in every toolchain, i.e., CEGIS, Ultimate Automizer, CPAChecker, and nuXmv. To run the smoke test, execute the `run.py` with the argument `--smoke`:

```bash
./run.py --smoke
```

If finished successfully, the evaluation script should print:
```
All smoke tests ran successfully :)
```

Note that the T2 baseline tool has its own smoke test as described in its README in the `src/t2-prover` directory.

### Running Experiments

We have split the experiments into tools and benchmark times, which can be executed individually to build the tables in the Appendix, which make up the datapoints for the plots in Figures 6-8. To run the experiment, run the `run.py` with the respective arguments:

```bash
./run.py -arg1 [-arg2 ...]
```

You can run different datasets specifying the tool and the property to check. For example, `./run.py -d clock -t bisimulation-learning` will run the deterministic clock experiments with Branching Bisimulation Learning (i.e. the last column for Table 1). 

**You can view a list of all available arguments by running `./run.py -h`.**

Please, consider the following availability schema:
- `clock`: the finite state clock synchronisation protocols (Table 1). Possible tools allowed:
    - `nuxmv` with modes `ic3` and `bdd` and formulas `safe` and `synch`
    - `bisimulation-learning` with modes `det` and `brn`
- `term`: the infinite state termination dataset (Table 2). Possible tools allowed:
    - `nuxmv` (`ic3` only) with formulas `term` and `nonterm`
    - `cpa` with formulas `term` and `nonterm`
    - `ultimate` with formulas `term` and `nonterm`
    - `bisimulation-learning` with modes `det` and `brn`
- `nd-inf`: the infinite state, (bounded) branching dataset with the formulas to be checked (Table 3). Possible tools allowed:
    - `nuxmv` (`ic3` only)
    - `ultimate`
    - `bisimulation-learning` (`brn` mode only)
- `nd-inf-t2`: the infinite state, (bounded) branching dataset for T2 comparison (Table 4). Please note that due to specific requirements T2 needs a separate container to run. Possible tools allowed:
    - `bisimulation-learning` (`brn` mode only)
- `nd-fin`: the finite state, (bounded) branching dataset (Table 5). Please note that this allows to set the systems' size with the --size flag. Possible tools allowed:
    - `nuxmv` (`bdd` mode only)
    - `bisimulation-learning` (`brn` mode only)

You find a complete list of arguments and possible values with:
```bash
./run.py --help
```

By default, all examples are run 10 times and their average runtime + standard deviation are reported, this can be adapted with the `--iters i` argument.

We provide some examples:

**Deterministic Clock Synchronization (Table 1)**:
```bash
./run.py -d clock -t nuxmv -m bdd -f safe
```
This command will produce numbers for the third column of Table 1.

**Deterministic Conditional Termination (Table 2)**:
```bash
./run.py -d term -t cpa
```
This command will produce numbers for the third column in Table 2.

**Non-Deterministic Infinite State base (Table 3)**:
```bash
./run.py -d nd-inf -t nuxmv
```
This command will produce numbers for the nuXmv (IC3) column in Table 3.

**T2 benchmarks (Table 4)**:
```bash
./run.py -d nd-inf-t2 -t bl
```
This command will produce numbers for the Bisimulation Learning column in Table 4.

**T2 has specific dependency needs in contrast with other tool's. For this reason, it is provided within a different container. You find the related manual on how to get the numbers for the T2 column in the `src/t2-prover` folder.**

**Non-Deterministic Finite State base (Table 5)**:
```bash
./run.py -d nd-fin -t nuxmv -size 11 
```
This command will produce numbers for the nuXmv (BDD) column in Table 5, **for systems with 2^11 states**.


If finished successfully, the evaluation script should print:
```
Experiments ran successfully. Results stored in some-file.csv
```
and you can find the benchmarks data in the specified `.csv` file.

## Evaluation 
### Runtime

The time required to run all experiments depends on the timeouts. The default timeout is 500 seconds, which may cause the experiments to run for more than 10 hours. You may specify a shorter timeout with the `--timeout [time in sec]` argument.

**The expected runtimes or rather their magnitudes can be found in Tables 1-5 in the Appendix A of the paper.** 


### Results / Quotients
The results for Bisimulation Learning are the parameters for the BDT templates, ranking functions, and the abstract transition function. **These can be viewed for branching bisimulation learning by adding the `--verbose` or `-v` option to the experiment call.** This will print the resulting parameters for partition tempate (theta), ranking function (eta) and also the adjacency matrix which uniquely describes the resulting quotient. A visualization for BDTs with the obtained parameters is being developed. If the prints contain symbolic values such as `u_0_1_0` or `p_1`, this corresponds to parameters that are not being used and whose values are therefore irrelevant.
 

### Randomness and Nondeterminism

We note that our approach (Branching Bisimulation Learning) is subject to two kinds of uncertainties. First, the obtained results depend on the initial samples, which we control by fixing a seed for the random generator (or do not use initial samples at all). **However, our learning approach depends on the sequence of counterexamples generated by the Verifier, i.e., an SMT solver. Since these are not controllable, our results may change in every run.** We tried to be conservative in our evaluation, and results should all lie within the same order of magnitude. 

The main claims that the artifact should validate despite nondeterminism are: 
* No significant runtime increase for learning bisimulations in the finite state clock synchronization benchmarks **(Figure 6 and Table 1)** when scaling the state spaces compared to the direct verification using nuXmv, which will become infeasbile for large benchmarks. 

* Comparable runtime, i.e., the same order of magnitude for the conditional termination benchmarks **(Figure 7 and Table 2)**, while producing a more informative result. Bisimulation learning provides a bisimulation and a separation into terminating and non-terminating states. At the same time, the baseline tools can only prove termination or nontermination for the entire state space and, therefore, need to be handed separate benchmarks.

* Runtime Comparable to Ultimate and T2 for LTL and CTL verification of infinite state non-deterministic benchmarks and better runtime than T2 for CTL* verification **(Figure 8 and Table 3 + 4)**.
  
### Correctness

The abstractions obtained for the used benchmarks are very simple (mostly < 10 states). They can be assessed visually (i.e., by viewing the adjacency matrix of the quotient) or by evaluating the resulting parameters (a BDT visualization is in progress).


## Reusability beyond this paper
The artifact is easy to use and extends beyond the purposes of this paper. To include a new experiment, all that is to do is define the one-step transition function of the form: 

```python
def successor(x):
    y_1 = f_1(x)
    ...
    y_k = f_k(x)

    return [y_1, ..., y_k]
```
which maps a current state $x\in \mathbb{R}^n$ to a list of its $k$ successors (remember that we assume transition systems with $k$-bounded branching) $y_i \in \mathbb{R}^n$ for $1 \leq i \leq k$, and an initial BDT template of the form 

```python
def bdt_term(params, x, num_params, partitions):
        b = BDTNodePoly([a_1,...],x, p_1, 
                BDTNodePoly([a_2,...]], x, p_2,
                                BDTLeave(c_1), BDTLeave(c_2)),
                ...
                )
        return b.formula(), b
```
defining the used label-preserving binary decision tree. An automated parser for labelling functions into a BDT of a specified size is in progress. 

With these two ingredients, one can follow the style of the `src/benchmark_nd.py` and easily define a new experiment to run with Bisimulation Learning. 

#### Resuability outside the artifact

Since the core artifact is a simple Python script, it can be used on any system with Python installed and even in a Jupyter Notebook. 


## Dependencies and Libraries
Bisimulation Learning builds up on the following dependencies and libraries (most recent versions):

  * [Z3 Solver](https://github.com/Z3Prover/z3) (Version 4.14.2) - SMT Solver used for Bisimulation Learning. Used in Learner and Verifier.
  * [NumPy](https://github.com/numpy/numpy) (Version 2.2.0) - Used internally for tensor and list operations.

The links to the used baseline tools are:

  * [Ultimate Automizer](https://github.com/ultimate-pa/ultimate) (Version 097f781)
  * [CPAChecker](https://cpachecker.sosy-lab.org/index.php) (Version 2.3)
  * [nuXmv](https://nuxmv.fbk.eu/) (Version 2.1.0)

## License

Copyright (c) 2025  Yannik Schnitzer, Christian Micheletti

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Instructions for T2

T2 is included as a baseline tool for CTL/CTL* verification of infinite-state systems. However, please note that T2 has not been actively maintained for approximately seven years ([see this repository](https://github.com/mmjb/T2)) and depends on legacy libraries and software versions. Despite this, we include it as it remains the only available tool supporting CTL/CTL* verification for infinite-state systems.

To accommodate the legacy dependencies, we provide a separate Dockerfile and Docker image. The Dockerfile was sourced from https://github.com/Marti2203/T2-temporal. Since T2 is not actively maintained, we cannot guarantee the full functionality or stability of the T2 setup. However, we have made every effort to streamline its usage by supplying convenient wrapper scripts.

---

**Disclaimer on usablity of T2**: 
Given the lack of recent maintenance, T2 is currently not fully reliable, especially for CTL* formula verification. In our experience, the tool may occasionally crash internally or fail to produce a result, sometimes in a non-deterministic manner. To mitigate this, we automatically retry the command execution several times until either a valid result is obtained or a maximum number of retries or a timeout is reached.

If you observe errors being printed, these originate from T2 itself and are part of the expected behavior within our retry mechanism; they are not indicative of issues with the artifact itself.



## Setup


You can build the T2-temporal prover image running

```bash
docker build -t t2-benchmarks .
```

in this directory. The image can be run in a container by executing:

```bash
docker run --name=t2-benchmarks -it t2-benchmarks 
```

## Run T2 / Smoke test

The `T2.exe` should be built in debug mode. To verify it, go in the `/opt/T2` folder and run:

```sh
mono src/bin/Debug/T2.exe test/cav13-ctl-examples/P1.t2 --CTL '[AG](varA != 1 || [AF](varR == 1))'
```

it should print a successful message:

```
Temporal proof succeeded
```

## Run benchmarks for Bisimulation Learning 

Bisimulation Learning benchmarks are defined in the `benchmarks.py` file. You can run them with:
```bash
python3 benchmarks.py
```

The test bench should take around half an hour to complete. If that's too long, you can adjust iteration and timeout settings:

```bash
python3 benchmarks.py -i 5 --timeout 60
```
This command will run five times each experiment with a timeout of 60 seconds.

# Instructions for T2

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

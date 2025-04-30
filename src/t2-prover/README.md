# Instructions for T2

T2 is included as a baseline tool for CTL/CTL* verification of infinite-state systems. However, please note that T2 has not been actively maintained for approximately seven years ([see this repository](https://github.com/mmjb/T2)) and depends on legacy libraries and software versions. Despite this, we include it as it remains the only available tool supporting CTL/CTL* verification for infinite-state systems.

To accommodate the legacy dependencies, we provide a separate Dockerfile and Docker image. The Dockerfile was sourced from https://github.com/Marti2203/T2-temporal. Since T2 is not actively maintained, we cannot guarantee the full functionality or stability of the T2 setup. However, we have made every effort to streamline its usage by supplying convenient wrapper scripts.

---

**Disclaimer on usablity of T2**: 
Given the lack of recent maintenance, T2 is currently not fully reliable, especially for CTL* formula verification. In our experience, the tool may occasionally crash internally or fail to produce a result, sometimes in a non-deterministic manner (probably some internal concurrency problems). To mitigate this, we automatically retry the command execution several times until either a valid result is obtained or a maximum number of retries or a timeout is reached.

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

### New!
---
We provide a pre-built Docker image as a compressed .tar archive, in line with artifact submission requirements and to help avoid potential build issues. The image was built on an Ubuntu 22.04 x86_64 machine.

To load the image, decompress and import it using:
```
gunzip -c t2-benchmarks.tar.gz 

docker load < t2-benchmarks.tar
```

Once loaded, the image should behave identically to one built from the provided Dockerfile.


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
python3 benchmarks.py [-arg1 ...]
```

The available arguments are:
 - ` -i ITERS, --iters ITERS` :The number of times to repeat the benchmarks. Default is 5
  - `--timeout TIMEOUT`:     The allowed maximun running time. Default is 300
  - `-t TOLERANCE, --tolerance TOLERANCE`:
                        The maximum number of times that a benchmark can break (T2 internally) before being excluded from the report. Default is 5
  - `-v, --verbose `:        Prints additional information during execution

The test bench should take around an hour to complete. If that's too long, you can adjust iteration and timeout settings:

```bash
python3 benchmarks.py -i 5 --timeout 60
```
This command will run five times each experiment with a timeout of 60 seconds. 

## Disclaimer on T2 usability and error messages

As noted in the preamble, T2 is no longer actively maintained and may fail to reliably produce results due to internal errors. These failures tend to occur in a non-deterministic manner, making them difficult to reproduce or diagnose consistently. Nevertheless, we include T2 in our artifact as it remains the only available tool supporting CTL/CTL* verification for infinite-state systems.

To mitigate these issues, we have made our execution scripts more robust. When a T2 error occurs, it is reported explicitly; such errors are due to limitations of the tool itself and not of the artifact. In response, we automatically rerun the failed execution up to a specified number of retries or until a timeout is reached.

Since the errors are non-deterministic, they may not manifest in the same way across different environments or reruns. We have made every effort to ensure our reporting is fair and transparent, reflecting the behavior observed during our experiments.
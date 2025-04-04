# Instructions

## Setup the T2-temporal prover image

Build the docker image from https://github.com/Marti2203/T2-temporal

```sh
git clone https://github.com/Marti2203/T2-temporal.git
cd T2-temporal
docker build -t t2-temporal .
```

This image can be used in a standalone Using it as a local image is useful for quickly rebuilding the image with the stuff useful for benchmarking and testing.

## Build the benchmark image

Now you can run the `Dockerfile` in this folder, which will pull the local image `T2-temporal` as a layer and add the benchmarks script. 

To work with it, use either the usual `docker build` command or 

```sh
./rebuild.sh
```
This script will clean the old docker image and container.

The `T2.exe` should be yet built in debug mode. To verify it, go in the `/opt/T2` folder and run.

## Verify installation

```sh
mono src/bin/Debug/T2.exe test/cav13-ctl-examples/P1.t2 --CTL '[AG](varA != 1 || [AF](varR == 1))'
```

it should print a successful message:

```
Temporal proof succeeded
```



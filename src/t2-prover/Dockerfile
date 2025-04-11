FROM --platform=linux/amd64 ubuntu:20.04

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y

RUN sed -i "$ a deb http://dk.archive.ubuntu.com/ubuntu/ xenial main " /etc/apt/sources.list
RUN sed -i "$ a deb http://dk.archive.ubuntu.com/ubuntu/ xenial main " /etc/apt/sources.list

# install experiment dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends  \
 g++-5 git python python3 python3-pip build-essential mono-complete mono-devel mono-xbuild fsharp wget curl apt-transport-https

RUN cd /usr/bin && rm gcc && ln -s gcc-5 gcc && rm g++ && ln -s g++-5 g++

WORKDIR /opt/

RUN git clone https://bitbucket.org/spacer/code spacer-t2
WORKDIR /opt/spacer-t2
RUN git checkout spacer-t2 && ./configure && cd build && make -j 8 && make -j 8 install

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /opt
RUN wget http://nuget.org/nuget.exe


WORKDIR /opt

# RUN mkdir T2
# 
RUN git clone https://github.com/mmjb/T2.git
COPY . T2/

ENV T2DIR=/opt/T2

WORKDIR /opt/spacer-t2
RUN cd src/api/dotnet && xbuild && cp obj/Debug/Microsoft.Z3.* /opt/T2/src/
RUN cp build/libz3.so /opt/T2/src/

WORKDIR /opt/T2/src

RUN mono /opt/nuget.exe restore

RUN xbuild

WORKDIR /opt/T2

RUN pip install -r requirements.txt

ENTRYPOINT [ "/bin/bash" ]

# Run T2 as follows (replace "Debug" by "Release" for the release build)
#       $ mono "$T2DIR/src/bin/Debug/T2.exe"
#     For example, to execute the testsuite:
#       $ pushd "$T2DIR/test" && mono "$T2DIR/src/bin/Debug/T2.exe" -tests

# RUN python3 benchmarks.py
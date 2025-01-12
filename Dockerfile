FROM --platform=linux/amd64 ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get autoremove -y

RUN apt-get install -y git build-essential && \
    apt-get install -y sudo && \
    apt-get install -y software-properties-common && \
    apt-get install -y wget

RUN apt-get install -y openjdk-21-jdk && \
    # apt-get install -y maven && \ 
    apt-get install -y zip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt install -y python3.10 && \
    apt-get install -y python3-pip && \
    apt-get install -y curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    pip3 install --upgrade pip && \
    mkdir CAV25

# Ultimate needs maven>=3.9.0
RUN wget https://dlcdn.apache.org/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.tar.gz
RUN tar -xvzf apache-maven-3.9.9-bin.tar.gz
ENV PATH="$PATH:$PWD/apache-maven-3.9.9/bin"

# Install nuXmv
WORKDIR /CAV25
RUN wget https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.0.0-linux64.tar.gz && \
    tar -xvzf download.php\?file\=nuXmv-2.0.0-linux64.tar.gz && \
    rm download.php\?file\=nuXmv-2.0.0-linux64.tar.gz 

# Install Ultimate
WORKDIR /CAV25
RUN git clone --depth=1 https://github.com/ultimate-pa/ultimate.git
WORKDIR /CAV25/ultimate/releaseScripts/default
RUN ./makeFresh.sh

# Install CPAChecker
WORKDIR /CAV25
RUN wget https://cpachecker.sosy-lab.org/CPAchecker-2.3-unix.zip && \
    unzip CPAchecker-2.3-unix.zip && \
    rm CPAchecker-2.3-unix.zip  && \
    apt-get install -y openjdk-17-jdk openjdk-17-jre

# Intstall Z3
WORKDIR /
RUN git clone --depth=1 https://github.com/Z3Prover/z3.git 
WORKDIR /z3
RUN python3 ./scripts/mk_make.py
WORKDIR /z3/build
RUN make && \
    make install

RUN ln -s /CAV25/nuXmv-2.0.0-Linux/bin/nuXmv /usr/bin/nuxmv

# To run ultimate-ltl
WORKDIR /
RUN wget http://www.lsv.fr/~gastin/ltl2ba/ltl2ba-1.3.tar.gz
RUN tar -xvzf ltl2ba-1.3.tar.gz
WORKDIR /ltl2ba-1.3
RUN make
RUN ln -s /ltl2ba-1.3/ltl2ba /usr/bin/ltl2ba


# Get artifact and libraries 
WORKDIR /CAV25 
RUN mkdir Bisimulation-Learning
COPY . ./Bisimulation-Learning
# RUN git clone https://github.com/yannikschnitzer/Bisimulation-Learning.git 
RUN pip install -r Bisimulation-Learning/requirements.txt

RUN mv /CAV25/Bisimulation-Learning/src/ultimate-ltl/ultimate-ltl /usr/local/bin/
RUN chmod 757 /usr/local/bin/ultimate-ltl

WORKDIR /CAV25/Bisimulation-Learning/src/ultimate-ltl


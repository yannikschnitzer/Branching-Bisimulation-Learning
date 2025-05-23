FROM ubuntu:22.04

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

# Install Ultimate
WORKDIR /CAV25
RUN git clone --depth=1 https://github.com/ultimate-pa/ultimate.git
WORKDIR /CAV25/ultimate/releaseScripts/default
RUN ./makeFresh.sh
RUN rm -rf /CAV25/ultimate/trunk/examples

# To run ultimate-ltl
WORKDIR /
RUN wget http://www.lsv.fr/~gastin/ltl2ba/ltl2ba-1.3.tar.gz
RUN tar -xvzf ltl2ba-1.3.tar.gz
WORKDIR /ltl2ba-1.3
RUN make
RUN ln -s /ltl2ba-1.3/ltl2ba /usr/bin/ltl2ba

# Install nuXmv
WORKDIR /CAV25
RUN wget https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz
RUN tar xf download.php\?file\=nuXmv-2.1.0-linux64.tar.xz && \
    rm download.php\?file\=nuXmv-2.1.0-linux64.tar.xz 

RUN ln -s /CAV25/nuXmv-2.1.0-linux64/bin/nuXmv /usr/bin/nuxmv


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

# Get artifact and libraries 

ARG BL_HOME=/CAV25/Branching-Bisimulation-Learning

WORKDIR ${BL_HOME}
COPY requirements.txt ${BL_HOME}
RUN pip install -r ${BL_HOME}/requirements.txt

COPY . ${BL_HOME}

RUN mv ${BL_HOME}/src/ultimate_ltl/ultimate-ltl /usr/local/bin/
RUN chmod 757 /usr/local/bin/ultimate-ltl

RUN mv ${BL_HOME}/src/cpa/cpa /usr/local/bin/
RUN chmod 757 /usr/local/bin/cpa

WORKDIR ${BL_HOME}/src/
RUN chmod +x run.py


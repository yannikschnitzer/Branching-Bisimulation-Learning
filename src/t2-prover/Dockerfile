FROM t2-temporal

WORKDIR /opt/T2

COPY src/requirements.txt .

RUN pip install -r requirements.txt


COPY src/. .
# RUN python3 benchmarks.py >> benchmarks.log

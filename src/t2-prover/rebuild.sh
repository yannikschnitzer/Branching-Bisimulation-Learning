docker container remove t2-benchmarks
docker image remove t2-benchmarks
docker build -t t2-benchmarks . \
  && docker builder prune -f \
  && docker run --name=t2-benchmarks -it t2-benchmarks 
# python3 benchmarks.py >> benchmarks.txt
# docker stop t2-benchmarks

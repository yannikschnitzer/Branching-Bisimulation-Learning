sudo docker container remove t2-benchmarks
sudo docker image remove t2-benchmarks
sudo docker build -t t2-benchmarks . \
  && sudo docker builder prune -f \
  && sudo docker run --name=t2-benchmarks -it t2-benchmarks 
# python3 benchmarks.py >> benchmarks.txt
# sudo docker stop t2-benchmarks

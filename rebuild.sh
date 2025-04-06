docker container remove bisimulation-learning
docker image remove bisimulation-learning
docker build -t bisimulation-learning . \
  && docker builder prune -f \
  && docker run --name=bisimulation-learning -it bisimulation-learning 


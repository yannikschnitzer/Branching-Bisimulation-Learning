sudo docker container remove bisimulation-learning
sudo docker image remove bisimulation-learning
sudo docker build -t bisimulation-learning .
sudo docker builder prune
sudo docker run --name=bisimulation-learning -i bisimulation-learning 


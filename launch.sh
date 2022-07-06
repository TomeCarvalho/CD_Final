docker build --tag projecto_final .
docker run -d --name worker1 projecto_final
sleep 3
docker run -d --name worker2 projecto_final
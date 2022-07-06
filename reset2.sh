docker stop worker1
docker stop worker2
docker stop worker3
docker rm worker1
docker rm worker2
docker rm worker3
docker build -t projecto_final .
docker run -d --name worker1 projecto_final
docker run -d --name worker2 projecto_final
docker run -d --name worker3 projecto_final
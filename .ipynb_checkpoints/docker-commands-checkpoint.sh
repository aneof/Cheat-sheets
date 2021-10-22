# build an image and give it a tag
docker build -t imagename .

# check status of currently running images
docker ps 

# list available docker images
docker image ls 

# force stop and delete docker image
docker rm -f imageid

# run image (-d run in background) (-p on which port (local:host)) 
docker run -dp 3000:3000 imagetag

# log in docker hub
docker login -u aneof

# rename (give tag to) docker image
docker tag getting-started aneof/getting-started

# push to dockerhub
docker push aneof/getting-started

# create named volume to persist data
docker volume create volumename
# docker automatically recognises it needs to create the volume
docker run -dp 3000:3000 -v volumename:/path/to/save imagetag

# create network 
docker network create networkname
# connect to the network and give an alias that will be resolved by other connecting containers
docker run -d --network networkname imagetag --network-alias alias

# run a command inside the image (-it makes it interactive by creating bash shell in container)
docker exec -it containerid linuxcommand

# start up application stack from yaml file
docker-compose up -d

# check the logs (-f for live following)
docker-compose logs -f

# stop and delete (--volumes to also delete volumes)
docker-compose down --volumes

# inspect the layers of the image (--no-trunc to remove truncation)
# each dockerfile command is a separate layers
docker image history imagetag

# BEST PRACTICES
# split dockerfile commands to enable layer caching and make the container reload faster
# use multi-stage builds to make the final container lighter

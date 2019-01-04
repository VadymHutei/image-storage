# image-storage

## create container
docker build -t storage .
docker run --name storage -d -p 80:80 -v /home/storage:/app/test storage
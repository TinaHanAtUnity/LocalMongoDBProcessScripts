# How to set up local mongo database 
## Prerequisite
- Docker ([macOS](https://docs.docker.com/docker-for-mac/install/))
- Mongo shell command tool ([instruction](https://docs.mongodb.com/manual/mongo/))
- Access to [exchange-mongodb-backups-prd](https://console.cloud.google.com/storage/browser/exchange-mongodb-backups-prd/ads-exchange-creative;tab=objects?orgonly=true&project=unity-ads-exchange-prd&prefix=)
- Google cloud SDK(https://cloud.google.com/sdk/install)

## How to set up local mongoDB
- Stop all running container in Docker using
```bash
docker kill $(docker ps -q)
```
- Run mongoDB using Docker
```bash
docker run -d --name anyName --restart=always -p 27017:27017 mongo
```
- Download the latest backup data from [here](https://console.cloud.google.com/storage/browser/exchange-mongodb-backups-prd/ads-exchange-creative;tab=objects?orgonly=true&project=unity-ads-exchange-prd&prefix=)
copy the URI of the file and use the following command to download it
```bash
gsutil cp gs://exchange-mongodb-backups-prd/ads-exchange-creative/ads-exchange-creative-1595548800.gz .
```
- Resotre downloaded gzip file to local mongoDB
```bash
mongorestore --gzip --archive=${BACKUP_FILE_GZ} --nsFrom “${DB_NAME}.*” --nsTo “${DB_NAME_RESTORE}.*”
```
for example
```bash
mongorestore --gzip --archive="ads-exchange-creative-1595548800.gz" --nsFrom "creatives" --nsTo "creatives"
```

## How to use the script
After local mongoDB is good to go, using python3 to run the python script
```dash
python3 xxxx.py
```
There will be a progress bar to show how much it has done for now, usually it will take 10 minutes to finish.
After it prints out the following info, the local database is ready to use
<img width="906" alt="Screen Shot 2020-07-23 at 9 51 50 PM" src="https://user-images.githubusercontent.com/41215433/88361930-98dd0500-cd2f-11ea-98c8-a83976c6a562.png">

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
After local mongoDB is installed and restored data from the downloaded file, using python3 to run the python script
```dash
python3 xxxx.py
```
There will be a progress bar to show how much it has done for now, usually it will take 10 minutes to finish.
After it prints out the following info, the local database is ready to use
<img width="906" alt="Screen Shot 2020-07-23 at 9 51 50 PM" src="https://user-images.githubusercontent.com/41215433/88361930-98dd0500-cd2f-11ea-98c8-a83976c6a562.png">

## What does the script do?
- The script iterates all files in `advertiser` collection and add every files (original creative) to a new collection called `allCreatives`

## Data object sample in `allCreative` collection
```dash
original creatives from `advertiser` collection stored in `allCreatives` in the following format
{
	"_id" : ObjectId("5f1a666a1c202f0d934dbfcf"),
	"creativeId" : "5909c6fd6bdc2a00115c2a75",
	"checksum" : "",
	"status" : "processed",
	"moderationStatus" : "approved",
	"organizationId" : "56cdf719b209521800a91f33",
	"gameId" : 500000004,
	"timeStamp" : "2019-12-03::12-02"
}
```
- After the above process, the script iterates all creatives in `creatives` collection and add every creative to `allCreative` 
```dash
creatives from `creatives` collection (creatives sent to Theorem) stored in `allCreative` in the following format
{
	"_id" : ObjectId("5f1a666a1c202f0d934dbfcf"),
	"creativeId" : "5909c6fd6bdc2a00115c2a75",
	"checksum" : "",
	"status" : "SUCESS",
	"decision" : "GO",
	"organizationId" : "56cdf719b209521800a91f33",
	"gameId" : 500000004,
}
```

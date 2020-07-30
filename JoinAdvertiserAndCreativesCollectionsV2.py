from pymongo import MongoClient

def establishLocalMongo():
    client = MongoClient('mongodb://localhost:27017', authSource='creatives')
    cqsDB = client['creatives']
    advertiserDB = client['ads-advertiser-campaigns']
    creatives = cqsDB['creatives']
    advertiser = advertiserDB['campaigns']
    allCreatives = cqsDB['allCreatives']
    validChecksum = cqsDB['validChecksum']
    return creatives, advertiser, allCreatives, validChecksum

creatives, advertiser, allCreatives, validChecksum = establishLocalMongo()

# add all the files in advertiser collection to allCreatives collection
items = []
for i, campaign in enumerate(advertiser.find()):
    orgId = str(campaign['organizationId'])
    gameId = campaign['gameId']
    timeStamp = campaign['updatedAt'].strftime('%Y-%m-%d::%H-%M')
    for files in campaign['creatives']:
        status = str(files['status'])
        moderationStatus = str(files['moderation']['status'])
        updatedAt = files['updatedAt'].strftime('%Y-%m-%d::%H-%M')
        createdAt = files['createdAt'].strftime('%Y-%m-%d::%H-%M')
        for creative in files['files']:
            try: 
                checksum = creative['checksum']
            except:
                checksum = ''
            item = {'creativeId': str(creative['_id']), 'checksum': checksum, 'status': status, 'moderationStatus': moderationStatus, 'organizationId': orgId, 'gameId': gameId, 'createdAt': createdAt, 'updatedAt': updatedAt}
            items.append(item)

allCreatives.insert_many(items)

items = []
# add all the creatives in creatives collection to allCreatives collection
for i, creative in enumerate(creatives.find()):
    try:
        checksum = creative['checksum']
    except:
        checksum = ''
    try:
        orgId = creative['organizationId']
    except:
        orgId = ''
    try:
        gameId = creative['gameId']
    except:
        gameId = ''
    try:
        status = creative['status']
    except:
        status = ''
    try:
        decision = creative['decision']
    except:
        decision = ''
    item = {'creativeId': creative['creativeId'], 'status': status, 'decision': decision, 'checksum': checksum, 'organizationId': orgId, 'gameId': gameId}
    items.append(item)

allCreatives.insert_many(items)
print("writing local database.....")

#extracting non empty checksum creatives from allCreatives
nonEmptyChecksums = []
for (i, creative) in enumerate(allCreatives.find()):
    if creative['checksum'] != "":
        nonEmptyChecksums.append(creative)
validChecksum.insert_many(nonEmptyChecksums)

print('Done. Now you can query the "allCreatives" collection using checksum or creativeId')

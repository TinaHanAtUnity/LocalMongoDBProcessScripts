from pymongo import MongoClient
import time

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration >= total:
        print()

def establishLocalMongo():
    client = MongoClient('mongodb://localhost:27017', authSource='creatives')
    db = client['creatives']
    creatives = db['creatives']
    advertiser = db['advertiser']
    allCreatives = db['allCreatives']
    return creatives, advertiser, allCreatives

creatives, advertiser, allCreatives = establishLocalMongo()

# add all the files in advertiser collection to allCreatives collection
items = []
l_advertiser = advertiser.estimated_document_count()
l_creatives = creatives.estimated_document_count()
l = l_advertiser + l_creatives
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i, campaign in enumerate(advertiser.find()):
    orgId = campaign['organizationId']
    gameId = campaign['gameId']
    timeStamp = campaign['updatedAt'].strftime('%Y-%m-%d::%H-%M')
    for files in campaign['creatives']:
        status = files['status']
        moderationStatus = files['moderation']['status']
        for creative in files['files']:
            item = {'creativeId': creative['_id'], 'checksum': creative['checksum'], 'status': status, 'moderationStatus': moderationStatus, 'organizationId': orgId, 'gameId': gameId, 'timeStamp': timeStamp}
            items.append(item)
    if (i % 50000 == 0) :
        allCreatives.insert_many(items)
        items = []

    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)


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
    if (i % 50000 == 0) :
        allCreatives.insert_many(items)
        items = []

    printProgressBar(i + 1 + l_advertiser, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

allCreatives.insert_many(items)

print('Done. Now you can query the "allCreatives" collection using checksum or creativeId')

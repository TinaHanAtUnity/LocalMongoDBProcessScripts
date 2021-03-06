from pymongo import MongoClient

def establishLocalMongo():
    client = MongoClient('mongodb://localhost:27017', authSource='creatives')
    db = client['creatives']
    validChecksum = db['validChecksum']
    return validChecksum

validChecksum = establishLocalMongo()

orgIds = set() 
blockedChecksums = set()
with open("./blockedIds") as fp:
    for line in fp:
        orgIds.add(line.rstrip('\n'))
for creative in validChecksum.find():
    orgId = creative['organizationId']
    checksum = creative['checksum']
    if orgId in orgIds:
        blockedChecksums.add(checksum)

suspiciousChecksums = []
for checksum in blockedChecksums:
    for creative in validChecksum.find({"checksum":checksum}):
        try:
            decision = creative['decision']
        except:
            decision = ""
        if decision != "":
            print("The following creatives have the same checksum" + checksum)
            for c in validChecksum.find({"checksum":checksum}):
                print(c)
            break

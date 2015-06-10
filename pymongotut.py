from pymongo import MongoClient
import pymongo
from datetime import datetime

'''
-------------------------------------------------------------------------------
The official pymongo tutorial was followed below
http://docs.mongodb.org/getting-started/python/
-------------------------------------------------------------------------------
'''

'''
-------------------------------------------------------------------------------
Connecting to a remote MongoDB server, currently running on a Raspberry Pi 2
-------------------------------------------------------------------------------
'''

client = MongoClient("mongodb://192.168.2.8:27017")

'''
If MongoDb is running on local machine you can use:
client = MongoClient()
'''

'''
-------------------------------------------------------------------------------
Connect to a database named 'test'
-------------------------------------------------------------------------------
'''

db = client.test

'''
or dictionary style access can also be used
db = client['test']
'''

'''
-------------------------------------------------------------------------------
Connect to a collection within the database
-------------------------------------------------------------------------------
'''
coll = db.restaurants

'''
or a dictionary style access can also be used for collections
coll = db['restaurants']
'''

'''
-------------------------------------------------------------------------------
Getting all the documents in the restaurants collection
-------------------------------------------------------------------------------
'''

#cursor = db.restaurants.find()

'''
a dictionary style access can be used with methods
'''


'''
cursor = db['restaurants'].find()

for document in cursor:
    print document

'''

'''
-------------------------------------------------------------------------------
Inserting a Document
-------------------------------------------------------------------------------
'''

item = {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    }


result = db.restaurants.insert_one(item)
print 'The item was inserted with id:'+str(result.inserted_id)

'''
-------------------------------------------------------------------------------
Querying
-------------------------------------------------------------------------------
'''

'''
Let's find the inserted item using different keys
'''

cursor = db.restaurants.find({"_id": result.inserted_id})
print '---------------'
print 'Item found using _id:'+str(cursor)
for document in cursor:
    print document

'''
-------------------------------------------------------------------------------
Query by a top level field
-------------------------------------------------------------------------------
'''

cursor = db.restaurants.find({"name": "Vella"})
print '---------------'
print 'Item found using name:'+str(cursor)
for document in cursor:
    print document

'''
-------------------------------------------------------------------------------
Query by an embedded document
-------------------------------------------------------------------------------
'''

cursor = db.restaurants.find({"address.zipcode":"10075"})
print '---------------'
print 'Item found using name:'+str(cursor)
for document in cursor:
    print document


'''
-------------------------------------------------------------------------------
Query by an field in array
-------------------------------------------------------------------------------
'''
'''
Find all documents: restraunts in zip 10075 with a B rating and called Vella
'''
cursor = db.restaurants.find({"grades.grade":"B","address.zipcode":"10075","name":"Vella"})
print '---------------'
print 'Item zipcode and grade:'+str(cursor)
for document in cursor:
    print document


'''
-------------------------------------------------------------------------------
Specify conditions using operators
-------------------------------------------------------------------------------
'''
'''
{ <field1>: { <operator1>: <value1> } }
'''
'''
Find restaurants with grade scores greater than 30 and in zipcode 11369
'''
cursor = db.restaurants.find({"grades.score":{"$gt":30},"address.zipcode":"11369"})
print '---------------'
print 'Item greater than 30 score:'+str(cursor)
for document in cursor:
    print document

'''
Find restaurants with grade scores less than 10 and in zipcode 11369
'''
cursor = db.restaurants.find({"grades.score":{"$lt":30},"address.zipcode":"11369"})
print '---------------'
print 'Item less than 10 score:'+str(cursor)
for document in cursor:
    print document

'''
Find indian restaurants with grade scores less than 10  or greater than 30 in zipcode 10075
'''
cursor = db.restaurants.find({"cuisine":"Indian","address.zipcode":"10075","$or":[{"grades.score":{"$lt":10}},{"grades.score":{"$gt":30}}]})
print '---------------'
print 'Indian restaurants:'+str(cursor)
for document in cursor:
    print document


'''
Find indian restaurants with grade scores less than 10  or greater than 30 in zipcode 10075 and 11369
'''
print '------------------------------------------------------------'
print 'Indian restaurants in 10075 or 11369 with scores <10 and >30'
print '------------------------------------------------------------'
cursor = db.restaurants.find({"cuisine":"Indian","address.zipcode":{"$in":["10075","11369","11216"]},"$or":[{"grades.score":{"$lt":10}},{"grades.score":{"$gt":30}}]})
print '---------------'
print 'Indian restaurants:'+str(cursor)
for document in cursor:
    print document

'''
Find indian restaurants with grade scores less than 10  or greater than 30 in zipcode 10075, sorted by score
'''
cursor = db.restaurants.find({"cuisine":"Indian","$or":[{"grades.score":{"$lt":10}},{"grades.score":{"$gt":30}}]}).sort("grades.score",pymongo.ASCENDING)
print '---------------'
print 'Indian restaurants:'+str(cursor)
for document in cursor:
    print document


'''
-------------------------------------------------------------------------------
Updating Data/Documents
-------------------------------------------------------------------------------
'''
'''
Updating a top level field
'''

result = db.restaurants.update_one({"name":"Juni"},{"$set":{"cuisine":"American (Old)"}})

print 'How many results matched the search criteria: ' + str(result.matched_count)
print 'How many documents were updated: ' + str(result.modified_count)

cursor = db.restaurants.find({"name":"Juni"})
for document in cursor:
    print document


'''
Updating an embedded field
'''

cursor = db.restaurants.find({"restaurant_id":"41156888"})
for document in cursor:
    print document


print 'Updating restaurant address'
result = db.restaurants.update_one({"restaurant_id":"41156888"},{"$set":{"address.street":"East 31st Street"}})
print 'How many results matched the search criteria: ' + str(result.matched_count)
print 'How many documents were updated: ' + str(result.modified_count)


cursor = db.restaurants.find({"restaurant_id":"41156888"})
for document in cursor:
    print document


'''
Updating multiple documents
'''
print 'Updating multiple documents'

result = db.restaurants.update_many(
    {"address.zipcode": "10016", "cuisine": "Other"},
    {
        "$set": {"cuisine": "Category To Be Determined"}
    }
)

print 'How many results matched the search criteria: ' + str(result.matched_count)
print 'How many documents were updated: ' + str(result.modified_count)


cursor = db.restaurants.find({"address.zipcode": "10016", "cuisine": "Category To Be Determined"})
for document in cursor:
    print document


'''
Replacing a document
'''
print '----------------------------------------------'
print 'Replacing a document'
print 'Find the first document matching criteria and modify the document schema'
cursor = db.restaurants.find_one({"restaurant_id": "41704620"})
print cursor



result = db.restaurants.replace_one(
    {"_id": cursor['_id']},
    {
        "name": "Vella 2",
        "address": {
            "coord": [-73.9557413, 40.7720266],
            "building": "1480",
            "street": "2 Avenue",
            "zipcode": "10075"
        },
        "restaurant_id":"41704620"
    }
)

print 'How many results matched the search criteria: ' + str(result.matched_count)
print 'How many documents were updated: ' + str(result.modified_count)

cursor = db.restaurants.find({"restaurant_id": "41704620"})
for document in cursor:
    print document

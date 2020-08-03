import os
from flask import Flask
from mongoengine import *
import json
import urllib.parse
import pymongo

app = Flask(__name__)

## Pull in CloudFoundry's production settings
# https://github.com/cloudfoundry-attic/vcap/blob/master/docs/python.md
if 'VCAP_SERVICES' in os.environ:
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    # XXX: avoid hardcoding here
    mongo_srv = vcap_services['documentdb'][0]
    cred = mongo_srv['credentials']
    host = cred['INSTANCE_ENDPOINT']
    user = cred['DB_USERNAME']
    pw = cred['DB_PASSWORD']
    port = cred['PORT']
    #mongodb://{}:{}@{}:{}
    mongo_url = "mongodb://{}:{}@{}:{}/".format(user,urllib.parse.quote_plus(pw),host,port)
else:
    host = "localhost"
    user = ""
    pw = ""
    mongo_url = "mongodb://localhost"

# from: https://docs.aws.amazon.com/documentdb/latest/developerguide/connect_programmatically.html
# #client = pymongo.MongoClient('mongodb://<sample-user>:<password>@sample-cluster.node.us-east-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred') 
# client = pymongo.MongoClient(mongo_url) 

# ##Specify the database to be used
# db = client.sample_database

# ##Specify the collection to be used
# col = db.sample_collection

# ##Insert a single document
# col.insert_one({'hello':'Amazon DocumentDB'})

# ##Find the document that was previously written
# x = col.find_one({'hello':'Amazon DocumentDB'})

# ##Print the result to the screen
# print(x)

# ##Close the connection
# client.close()

# # create a connection to the MongoDB
# print(mongo_url)
connection = connect('sophia', host=mongo_url)

class User(Document):
    user = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

# fill the DB with some dummy stuff
User(user='donald', first_name='Donald', last_name='Duck').save()
User(user='dagobert', first_name='Dagobert', last_name='Duck').save()
User(user='mickey', first_name='Mickey', last_name='Mouse').save()
User(user='super', first_name='Super', last_name='Man').save()


### ----------------------------------------------------------------------- ###

@app.route('/')
def hello():
    return 'Hello World! This is the test app for python and MongoDB'


@app.route('/env')
def env():
    #return os.environ.keys
    strReturn = ""
    for param in os.environ.keys():
        strReturn += "%20s %s<br>" % (param,os.environ[param])
    return strReturn

@app.route('/cred')
def creds():
    strReturn = "host: %s<br> user: %s<br> pw: %s<br>url: %s" % (host,user,pw, mongo_url)
    return strReturn

@app.route('/<username>/show')
def show(username):
    strReturn = ""
    for usr in User.objects(user=username):
        strReturn += "Hello %s %s, how are you today?<br>" % (usr.first_name, usr.last_name)
    return strReturn


### ---- start flask 
port = os.getenv('VCAP_APP_PORT', '8000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))


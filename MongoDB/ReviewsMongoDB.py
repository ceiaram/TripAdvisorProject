import pymongo
import dns # required for connecting with SRV
import pandas as pd
# client = pymongo.MongoClient("mongodb+srv://ceiaram:gQhW4xB59kC7a7Do@tripadvisordb.qw0eojr.mongodb.net/?retryWrites=true&w=majority")
client = pymongo.MongoClient("mongodb+srv://ceiaram:Xn704K3WQ0So6s09@tripadvisordb.qw0eojr.mongodb.net/?retryWrites=true&w=majority")
db = client.test


#use database named "organisation"
db = client["OrangeCountyHotels"]

# Import all reviews from 587 hotels 
for x in range(587):
    #Creating a collection
    collection = db['Reviews']

    # Import data
    df = pd.read_csv('./Temp/' + str(x) + '.csv')
    tmp = df.to_dict(orient='records')
    if(len(tmp) != 0):
        collection.insert_many(tmp)
   
print('Done')
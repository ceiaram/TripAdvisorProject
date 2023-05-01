import pymongo
import dns # required for connecting with SRV
import pandas as pd
# client = pymongo.MongoClient("mongodb+srv://ceiaram:gQhW4xB59kC7a7Do@tripadvisordb.qw0eojr.mongodb.net/?retryWrites=true&w=majority")
client = pymongo.MongoClient("mongodb+srv://ceiaram:Xn704K3WQ0So6s09@tripadvisordb.qw0eojr.mongodb.net/?retryWrites=true&w=majority")
db = client.test


#use database named "organisation"
db = client["OrangeCountyHotels"]

#Creating a collection
collection = db['HotelData']

# Import data
df = pd.read_csv('hotelData.csv')
tmp = df.to_dict(orient='records')
collection.insert_many(tmp) 
   
print('Done')
import pymongo
import dns # required for connecting with SRV
import nltk
import statistics


# Connect to database, 24hr timeout
client = pymongo.MongoClient("mongodb+srv://ceiaram:Xn704K3WQ0So6s09@tripadvisordb.qw0eojr.mongodb.net/?retryWrites=true&w=majority", socketTimeoutMS=86400000)
db = client.test

# Get database named "OrangeCountyHotels"
db = client["OrangeCountyHotels"]


count_about_section = 0
num_words_about_section = []
num_of_sentences_about_section = []

# Get collection
collection_hotels = db['HotelData']
for x in range(587):
    my_query = {'Index' : x}
    hotel_doc = collection_hotels.find(my_query)

    for doc in hotel_doc:
        if doc['Hotel About Section']:
            about_section = doc['Hotel About Section']
            if about_section != "none" and isinstance(about_section, str):
                count_about_section = count_about_section + 1

                # Get number of words found in about section review 
                num_words = len(about_section.split())
                num_words_about_section.append(int(num_words))

                # split the text into sentences using nltk
                sentences = nltk.sent_tokenize(about_section)
                num_of_sentences_about_section.append(len(sentences))

            else:
                continue

# Get the average of words and sentences list 
average_num_words_about_section = statistics.mean(num_words_about_section)
average_num_of_sentences_about_section = statistics.mean(num_of_sentences_about_section)

print("Number of hotels that had an about section: " + str(count_about_section))
print("Among the " + str(count_about_section) + " self-descriptions, on average, it contains " + str(average_num_words_about_section) 
      + "words and " + str(average_num_of_sentences_about_section) + " sentences")
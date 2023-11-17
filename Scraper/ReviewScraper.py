import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

user_agent = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

# hotel_review_links = []
page_contents = []
review_contents = []

#Review data
helpful_votes = []
contributions = []
overall_ratings = []
location_ratings = []
cleanliness_ratings = []
service_ratings = []
value_ratings = []
rooms_ratings = []
sleep_quality_ratings = []
review_summary_headings = []
review_summaries = []
date_of_stays = []
room_tips = []
trip_types = []
manager_responses = []


def get_page_contents(reviewPageUrl):
    print("Getting page contents")
    page = requests.get(reviewPageUrl, headers = user_agent)
    return BeautifulSoup(page.text, 'html.parser')

def get_review_contents(soup):
    for review in soup.find_all('div',{'class':'YibKl MC R2 Gi z Z BB pBbQr'}):
        review_contents.append(review)

def get_helpful_votes(soup, index):
    word = 'helpful'
    found = False

    for helpful_vote in soup.find_all('span',{'class':'phMBo'}):
        if word in helpful_vote.text.strip():
            helpful_votes.insert(index, helpful_vote.text.strip())
            found = True
            print("HELPFUL VOTE FOUND")
            break
            
    if found == False:
        print("HELPFUL VOTE NOT FOUND")
        helpful_votes.insert(index, 'none')

def get_num_of_bubbles(list,list_data, index):
    found = False
    data = ['5.0 of 5 bubbles','4.0 of 5 bubbles', '3.0 of 5 bubbles', 
     '2.0 of 5 bubbles','1.0 of 5 bubbles']

    if(list_data == 'bubble_50'):
        list.insert(index, data[0])
        found = True
        print("DATA FOUND")
        
    if(list_data == 'bubble_40'):
        list.insert(index, data[1])
        found = True
        print("DATA FOUND")
        
    if(list_data == 'bubble_30'):
        list.insert(index, data[2])
        found = True
        print("DATA FOUND")
        
    if(list_data == 'bubble_20'):
        list.insert(index, data[3])
        found = True
        print("DATA FOUND")
        
    if(list_data == 'bubble_10'):
        list.insert(index, data[4])
        found = True
        print("DATA FOUND")

    if found == False:
        print("DATA NOT FOUND") 
        list.insert(index, 'none')  
    

def get_contributions(soup, index):
    word = 'contributions'
    word2 = 'contribution'
    found = False
    for contribution in soup.find_all('span',{'class':'phMBo'}):
        if (word in contribution.text.strip()) or (word2 in contribution.text.strip()):
            contributions.insert(index, contribution.text.strip())
            found = True
            print("CONTRIBUTION FOUND") 
            break

    if found == False:
        print("CONTRIBUTION NOT FOUND") 
        contributions.insert(index, 'none')

def get_overall_ratings(soup, index):
    found = False
    for overall_rating in soup.find_all('div',{'class':'Hlmiy F1'}):
          span = overall_rating.find('span')
          if(span):
            get_num_of_bubbles(overall_ratings, span["class"][1], index)
            found = True
            print("OVERALL RATINGS FOUND") 
            break
    if found == False:
        print("OVERALL RATINGS NOT FOUND") 
        overall_ratings.insert(index, 'none')  

def get_review_summary_headings(soup, index):
    found = False
    for review_summary_heading in soup.find_all('a',{'class':'Qwuub'}):
        if (review_summary_heading.find('span')):
            review_summary_headings.insert(index, review_summary_heading.text.strip())
            found = True
            print("REVIEW SUMMARIES FOUND") 
            break
    if found == False:
        print("REVIEW SUMMARIES NOT FOUND") 
        review_summary_headings.insert(index, 'none')

def get_review_summary(soup, index):
    found = False
    for review_summary in soup.find_all('q',{'class':'QewHA H4 _a'}):
        if (review_summary.find('span')):
            review_summaries.insert(index, review_summary.find('span').text.strip())
            found = True
            print("REVIEW SUMMARIES FOUND") 
            break
    if found == False:
        print("REVIEW SUMMARIES NOT FOUND") 
        review_summaries.insert(index, 'none')

def get_date_of_stays(soup, index):
    found = False
    empty_word = 'Date of stay: '
    for date_of_stay in soup.find_all('span',{'class':'teHYY _R Me S4 H3'}):
        if (date_of_stay):
            # Phrase out the word 'Date of stay: '
            phraseData = str(date_of_stay.text.strip())
            phraseData = phraseData.replace(empty_word,"")

            date_of_stays.insert(index, phraseData)
            found = True
            print("DATE OF STAYS FOUND") 
            break
    if found == False:
        print("DATE OF STAYS NOT FOUND") 
        date_of_stays.insert(index, 'none')

def get_room_tips(soup, index):
    found = False
    empty_word = 'Room Tip: '
    for room_tip in soup.find_all('div',{'class':'Pb'}):
        if (room_tip.find('span')):
            # Phrase out the word 'Room Tip: '
            phraseData = str(room_tip.text.strip())
            phraseData = phraseData.replace(empty_word,"")

            room_tips.insert(index, phraseData)
            found = True
            print("ROOM TIPS FOUND") 
            break
    if found == False:
        print("ROOM TIPS NOT FOUND") 
        room_tips.insert(index, 'none')

def get_trip_types(soup, index):
    found = False
    empty_word = 'Trip type: '
    for trip_type in soup.find_all('span',{'class':'TDKzw _R Me'}):
        if (trip_type):
            # Phrase out the word 'Room Tip: '
            phraseData = str(trip_type.text.strip())
            phraseData = phraseData.replace(empty_word,"")

            trip_types.insert(index, phraseData)
            found = True
            print("TRIP TYPES FOUND") 
            break
    if found == False:
        print("TRIP TYPES NOT FOUND") 
        trip_types.insert(index, 'none')

def get_location_ratings(soup, index):
    found = False

    for location_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = location_rating.find_all('span')
        span_len = len(span) 
  
        if(span_len == 3 and span[2].text.strip() == 'Location'):
          bubbles = span[1]['class'][1]
          get_num_of_bubbles(location_ratings, bubbles, index)
          found = True
          print("LOCATION RATINGS FOUND") 
          break

    if found == False:
        print("LOCATION RATINGS NOT FOUND") 
        location_ratings.insert(index, 'none')      

def get_cleanliness_ratings(soup, index):
    found = False
    for cleanliness_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = cleanliness_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Cleanliness'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(cleanliness_ratings, bubbles, index)
            found = True
            print("CLEALINESS RATINGS FOUND") 
            break
    if found == False:
        print("CLEALINESS RATINGS NOT FOUND") 
        cleanliness_ratings.insert(index, 'none') 

def get_service_ratings(soup, index):
    found = False
    for service_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = service_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Service'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(service_ratings, bubbles, index)
            found = True
            print("SERVICE RATINGS FOUND") 
            break
    if found == False:
        print("SERVICE RATINGS NOT FOUND") 
        service_ratings.insert(index, 'none') 

def get_value_ratings(soup, index):
    found = False
    for value_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = value_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Value'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(value_ratings, bubbles, index)
            found = True
            print("VALUE RATINGS FOUND") 
            break
    if found == False:
        print("VALUE RATINGS NOT FOUND") 
        value_ratings.insert(index, 'none') 

def get_rooms_ratings(soup, index):
    found = False
    for rooms_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = rooms_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Rooms'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(rooms_ratings, bubbles, index)
            found = True
            print("ROOM RATINGS FOUND") 
            break
    if found == False:
        print("ROOM RATINGS NOT FOUND") 
        rooms_ratings.insert(index, 'none') 

def get_sleep_quality_ratings(soup, index):
    found = False
    for sleep_quality_rating in soup.find_all('div',{'class':'hemdC S2 H2 WWOoy'}):
        span = sleep_quality_rating.find('span')
        span_len = len(span) 

        if(span_len == 3 and span[2].text.strip() == 'Sleep Quality'):
            bubbles = span[1]['class'][1]
            get_num_of_bubbles(sleep_quality_ratings, bubbles, index)
            found = True
            print("SLEEP QULAITY RATINGS FOUND") 
            break
    if found == False:
        print("SLEEP QUALITY RATINGS NOT FOUND") 
        sleep_quality_ratings.insert(index, 'none') 


def get_manager_responses(soup, index):
    found = False
    for manager_response in soup.find_all('span',{'class':'MInAm _a'}):
        if (manager_response):
            manager_responses.insert(index, manager_response.text.strip())
            found = True
            print("MANAGER RESPONSES FOUND") 
            break
    if found == False:
        print("MANAGER RESPONSES NOT FOUND") 
        manager_responses.insert(index, 'none')

# Get all reviews from 587 hotels 
for x in range(587):
    hotel_review_links = {}
    review_nums = []
    num = 1

    # Import data from folder 
    df = pd.read_csv('./HotelReviewLinks/' + str(x) + '.csv')

    hotel_review_links[x] = df['Hotel Link: ' + str(original_hotel_links[x])].to_list()
    print(hotel_review_links)

    for y in range(len(hotel_review_links[x])):
        print(hotel_review_links[x][y])
        formatted_link = hotel_review_links[x][y].replace("'","")
        soup = get_page_contents(formatted_link)
        page_contents.append(soup) 
       

    # Testing one page 
    # soup = get_page_contents("https://www.tripadvisor.com/Hotel_Review-g29092-d75532-Reviews-or30-The_Anaheim_Hotel-Anaheim_California.html#REVIEWS")
    # page_contents.append(soup)

    for y in range(len(page_contents)): 
       get_review_contents(page_contents[y]) 

    # Get data in review content from 10 reviews per page
    for y in range(len(review_contents)):
        # pass review content and index, so that results are in corresponding order of lists
        get_helpful_votes(review_contents[y], y)
        get_contributions(review_contents[y], y)
        get_overall_ratings(review_contents[y], y)
        get_review_summary_headings(review_contents[y], y)
        get_review_summary(review_contents[y], y)
        get_date_of_stays(review_contents[y], y)
        get_room_tips(review_contents[y], y)
        get_trip_types(review_contents[y], y)
        get_manager_responses(review_contents[y], y)
        get_location_ratings(review_contents[y], y)
        get_cleanliness_ratings(review_contents[y], y)
        get_service_ratings(review_contents[y], y)
        get_value_ratings(review_contents[y], y)
        get_rooms_ratings(review_contents[y], y)
        get_sleep_quality_ratings(review_contents[y], y)
        review_nums.append(num)
        num += 1 

    # Create the dictionary.
    dict = {'Helpful Vote' : helpful_votes, 'Contributions' : contributions, 'Overall Rating' : overall_ratings, 'Summary Heading' : review_summary_headings,
    'Summary' : review_summaries, 'Date of Stay' : date_of_stays, 'Room tip' : room_tips, 'Trip Type' : trip_types, 'Manager Response' : manager_responses,
    'Location Rating' : location_ratings, 'Cleanliness Rating' : cleanliness_ratings, 'Service Rating' :service_ratings, 'Value Rating' : value_ratings,
    'Rooms Rating' : rooms_ratings, 'Sleep Quality Rating' : sleep_quality_ratings, 'Review Number' : review_nums
    }

    # Create the dataframe.
    reviewsData = pd.DataFrame.from_dict(dict)
    reviewsData.head(10)
    # Convert dataframe to CSV file.
    reviewsData.to_csv(str(x) +'.csv', index=False, header=True)    

    #Clear all lists 
    page_contents.clear()
    review_contents.clear()
    review_nums.clear()

    helpful_votes.clear()
    contributions.clear()
    overall_ratings.clear()
    review_summary_headings.clear()
    review_summaries.clear()
    date_of_stays.clear()
    room_tips.clear()
    trip_types.clear()
    manager_responses.clear()
    location_ratings.clear()
    cleanliness_ratings.clear()
    service_ratings.clear()
    value_ratings.clear()
    rooms_ratings.clear()
    sleep_quality_ratings.clear()
    print("Done")






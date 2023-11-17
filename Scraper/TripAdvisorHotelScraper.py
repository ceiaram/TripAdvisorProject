# https://python.plainenglish.io/web-scraping-tripadvisor-hotels-with-python-and-beautiful-soup-625ccd3d67fa
# Import the libraries.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import math 

# Find and extract data elements
hotel_names = []
ratings = []
hotels_com_prices = []
booking_com_prices = []
travelocity_com_prices = []
about_sections = []
hotel_classes = []
ranks = []
price_ranges = []
total_number_of_reviews = []

traveler_rating_excellent = []
traveler_rating_very_good = []
traveler_rating_average = []
traveler_rating_poor = []
traveler_rating_terrible = []

location_scores = []
cleanliness_scores = []
service_scores = []
value_scores = []

walking_scores = []
restaurant_scores = []
attraction_scores = []

# Review data
review_dict = {}
review_contents = []
review_ratings = []
review_contributions = []
helpfulness_numbers = []
manager_messages = []

get_review_links = []
review_lens = []

user_agent = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

def get_page_contents(reviewPageUrl):
    print("Getting page contents")
    page = requests.get(reviewPageUrl, headers = user_agent)
    return BeautifulSoup(page.text, 'html.parser')

def get_hotel_names(soup):
    if(soup.find('div',{'class':'jvqAy'})):
        hotel_names.append(soup.find('div',{'class':'jvqAy'}).text.strip())
        print("HOTEL NAME")
    else:
        hotel_names.append('none')
        print("NO HOTEL NAME")

def get_ratings(soup):
    if(soup.find('span',{'class':'uwJeR P'})):
        ratings.append(soup.find('span',{'class':'uwJeR P'}).text.strip())
        print("RATING")
    else:
        ratings.append('none')
        print("NO RATING")

def get_hotel_com_prices(soup):
    if(soup.find('div',{'data-vendorname':'Hotels.com'})):
        prices = soup.find('div',{'data-vendorname':'Hotels.com'})
        if(prices.get('data-pernight')):
            # Get hotels.com price 
            hotels_com_prices.append(prices.get('data-pernight'))
            print("HOTEL.COM PRICES")
        else:
            hotels_com_prices.append('none')
            print("NO HOTEL.COM PRICES")
    else:
        hotels_com_prices.append('none')
        print("NO HOTEL.COM PRICES")

def get_booking_com_prices(soup):
    if(soup.find('div',{'data-vendorname':'Booking.com'})):
        prices = soup.find('div',{'data-vendorname':'Booking.com'})
        if(prices.get('data-pernight')):
            # Get booking.com price 
            booking_com_prices.append(prices.get('data-pernight'))
            print("BOOKING.COM PRICES")
        else:
            booking_com_prices.append('none')
            print("NO BOOKING.COM PRICES")
    else:
        booking_com_prices.append('none')
        print("NO BOOKING.COM PRICES")

def get_travelocity_com_prices(soup):
    if(soup.find('div',{'data-vendorname':'Travelocity'})):
        prices = soup.find('div',{'data-vendorname':'Travelocity'})
        if(prices.get('data-pernight')):
            # Get travelocity.com price 
            travelocity_com_prices.append(prices.get('data-pernight'))
            print("TRAVELOCITY.COM PRICES")
        else:
            travelocity_com_prices.append('none')
            print("NO TRAVELOCITY.COM PRICES")
    else:
        travelocity_com_prices.append('none')
        print("NO TRAVELOCITY.COM PRICES")

def get_about_sections(soup):
    if(soup.find('div',{'class':'fIrGe _T'})):
        about_sections.append(soup.find('div',{'class':'fIrGe _T'}).text.strip())
        print("ABOUT SECTION")
    else:
        about_sections.append('none')
        print("NO ABOUT SECTION")

def get_hotel_classes(soup):
    if(soup.find('svg',{'class':'JXZuC d H0'})):
        tag = soup.find('svg',{'class':'JXZuC d H0'})
        hotel_classes.append(tag.get('aria-label'))
        print("HOTEL CLASSES")
    else:
        hotel_classes.append('none')
        print("NO HOTEL CLASSES")
            
def get_ranks(soup):
    if(soup.find('span',{'class':'Ci _R S4 H3 MD'})):
        ranks.append(soup.find('span',{'class':'Ci _R S4 H3 MD'}).text.strip())
        print("RANKS")
    else:
        ranks.append('none')
        print("NO RANKS")

def get_price_ranges(soup):
    if(soup.find('div',{'class':'mpDVe Ci b'}).text.strip() == 'PRICE RANGE'):
        if(soup.find('div',{'class':'IhqAp Ci'})):
            price_ranges.append(soup.find('div',{'class':'IhqAp Ci'}).text.strip())
            print("PRICE RANGES")
        else:
            price_ranges.append('none')
            print("NO PRICE RANGES")   
    else:
        price_ranges.append('none')
        print("NO PRICE RANGES")

def get_total_number_of_reviews(soup):
    if(soup.find('span',{'class':'iypZC Mc _R b'})):
        total_number_of_reviews.append(soup.find('span',{'class':'iypZC Mc _R b'}).text.strip())
        print("TOTAL NUMBER OF REVIEWS")
    else:
        total_number_of_reviews.append('none')
        print("NO TOTAL NUMBER OF REVIEWS")

def get_traveler_rating_excellent(soup):
    if(soup.find('input',{'id':'ReviewRatingFilter_5'})):
        rating = soup.find('input',{'id':'ReviewRatingFilter_5'})
        if(rating.find('span',{'class':'NLuQa'}).text.strip()):
            # Get excellent rating 
            traveler_rating_excellent.append(rating.find('span',{'class':'NLuQa'}).text.strip())
            print("TRAVELER RATING EXCELLENT")
        else:
            traveler_rating_excellent.append('none')
            print("NO TRAVELER RATING EXCELLENT")
    else:
        traveler_rating_excellent.append('none')
        print("NO TRAVELER RATING EXCELLENT")

def get_traveler_rating_very_good(soup):
    if(soup.find('input',{'id':'ReviewRatingFilter_4'})):
        rating = soup.find('input',{'id':'ReviewRatingFilter_4'})
        if(rating.find('span',{'class':'NLuQa'}).text.strip()):
            # Get very good rating 
            traveler_rating_very_good.append(rating.find('span',{'class':'NLuQa'}).text.strip())
            print("TRAVELER RATING VERY GOOD")
        else:
            traveler_rating_very_good.append('none')
            print("NO TRAVELER RATING VERY GOOD")
    else:
        traveler_rating_very_good.append('none')
        print("NO TRAVELER RATING VERY GOOD")

def get_traveler_rating_average(soup):
    if(soup.find('input',{'id':'ReviewRatingFilter_3'})):
        rating = soup.find('input',{'id':'ReviewRatingFilter_3'})
        if(rating.find('span',{'class':'NLuQa'}).text.strip()):
            # Get average rating 
            traveler_rating_average.append(rating.find('span',{'class':'NLuQa'}).text.strip())
            print("TRAVELER RATING AVERAGE")
        else:
            traveler_rating_average.append('none')
            print("NO TRAVELER RATING AVERAGE")
    else:
        traveler_rating_average.append('none')
        print("NO TRAVELER RATING AVERAGE")

def get_traveler_rating_poor(soup):
    if(soup.find('input',{'id':'ReviewRatingFilter_2'})):
        rating = soup.find('input',{'id':'ReviewRatingFilter_2'})
        if(rating.find('span',{'class':'NLuQa'}).text.strip()):
            # Get poor rating 
            traveler_rating_poor.append(rating.find('span',{'class':'NLuQa'}).text.strip())
            print("TRAVELER RATING POOR")
        else:
            traveler_rating_poor.append('none')
            print("NO TRAVELER RATING POOR")
    else:
        traveler_rating_poor.append('none')
        print("NO TRAVELER RATING POOR")

def get_traveler_rating_terrible(soup):
    if(soup.find('input',{'id':'ReviewRatingFilter_1'})):
        rating = soup.find('input',{'id':'ReviewRatingFilter_1'})
        if(rating.find('span',{'class':'NLuQa'}).text.strip()):
            # Get terrible rating 
            traveler_rating_terrible.append(rating.find('span',{'class':'NLuQa'}).text.strip())
            print("TRAVELER RATING TERRIBLE")
        else:
            traveler_rating_terrible.append('none')
            print("NO TRAVELER RATING TERRIBLE")
    else:
        traveler_rating_terrible.append('none')
        print("NO TRAVELER RATING TERRIBLE")

def get_about_scores(soup):
    scores = []
    for score in soup.find_all('span',{'class':'CzVMJ'}):
        scores.append(score.text.strip())

    scores_len = len(scores)

    if(scores_len > 0):
        location_scores.append(scores[0])
        print("LOCATION SCORES")
    else:
        location_scores.append('none')
        print("NO LOCATION SCORES")
    if(scores_len > 1):
        cleanliness_scores.append(scores[1])
        print("CLEANLINESS SCORES")
    else:
        cleanliness_scores.append('none')
        print("NO CLEANLINESS SCORES")
    if(scores_len > 2):
        service_scores.append(scores[2])
        print("SERVICE SCORES")
    else:
        service_scores.append('none')
        print("NO SERVICE SCORES")
    if(scores_len > 3):
        value_scores.append(scores[3])
        print("VALUE SCORES")
    else:
        value_scores.append('none')
        print("NO VALUE SCORES")

def get_walking_scores(soup):
    if(soup.find('span',{'class':'iVKnd fSVJN'})):
        walking_scores.append(soup.find('span',{'class':'iVKnd fSVJN'}).text.strip())
        print("WALKING SCORES")
    else:
        walking_scores.append('none')
        print("NO WALKING SCORES")

def get_restaurant_scores(soup):
    if(soup.find('span',{'class':'iVKnd Bznmz'})):
        restaurant_scores.append(soup.find('span',{'class':'iVKnd Bznmz'}).text.strip())
        print("RESTAURANT SCORES")
    else:
        restaurant_scores.append('none')
        print("NO RESTAURANT SCORES")

def get_attraction_scores(soup):
    if(soup.find('span',{'class':'iVKnd rYxbA'})):
        attraction_scores.append(soup.find('span',{'class':'iVKnd rYxbA'}).text.strip())
        print("ATTRACTION SCORES")
    else:
        attraction_scores.append('none')
        print("NO ATTRACTION SCORES")


page_contents = []

# Get all the content in each page 
for x in range(len(hotel_links)):
    soup = get_page_contents(hotel_links[x])
    page_contents.append(soup)

# print(page_contents)
# Get all the data to every hotel in Orange County from each page content 
for x in range(len(hotel_links)):  
    get_hotel_names(page_contents[x])
    get_ratings(page_contents[x])
    get_hotel_com_prices(page_contents[x])
    get_booking_com_prices(page_contents[x])
    get_travelocity_com_prices(page_contents[x])
    get_price_ranges(page_contents[x])
    get_about_sections(page_contents[x])
    get_hotel_classes(page_contents[x])
    get_ranks(page_contents[x])
    get_total_number_of_reviews(page_contents[x])
    get_traveler_rating_excellent(page_contents[x])
    get_traveler_rating_very_good(page_contents[x])
    get_traveler_rating_average(page_contents[x])
    get_traveler_rating_poor(page_contents[x])
    get_traveler_rating_terrible(page_contents[x])
    get_about_scores(page_contents[x])
    get_walking_scores(page_contents[x])
    get_restaurant_scores(page_contents[x])
    get_attraction_scores(page_contents[x])


# Create the dictionary.
dict = {'Hotel Name': hotel_names, 'Hotel Rating': ratings, 'Hotels.com Price' : hotels_com_prices, 'Booking.com Price' : booking_com_prices,
'Travelocity.com Price' : travelocity_com_prices,'Hotel About Section' : about_sections, 'Hotel Class' : hotel_classes, 'Hotel Rank' : ranks,
'Hotel Price Range' : price_ranges, 'Total Number of Reviews' : total_number_of_reviews, 'Traveler Rating Excellent' : traveler_rating_excellent,
'Traveler Rating Very Good' : traveler_rating_very_good, 'Traveler Rating Average' : traveler_rating_average, 'Traveler Rating Poor' : traveler_rating_poor,
'Traveler Rating Terrible' : traveler_rating_terrible, 'Hotel Location Score' : location_scores, 'Hotel Cleanliness Score' : cleanliness_scores,
'Hotel Service Score' : service_scores, 'Hotel Value Score' : value_scores, 'Location Walking Score' : walking_scores, 
'Location Restaurant Score' : restaurant_scores, 'Location Attraction Score' : attraction_scores}

# Create the dataframe.
orangeCounty = pd.DataFrame.from_dict(dict)
orangeCounty.head(10)

# Convert dataframe to CSV file.
orangeCounty.to_csv('hotelData.csv', index=False, header=True)
print("Done")








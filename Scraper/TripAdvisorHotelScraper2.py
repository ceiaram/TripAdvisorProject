import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


user_agent = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

def get_page_contents(reviewPageUrl):
    print("Getting page contents")
    page = requests.get(reviewPageUrl, headers = user_agent)
    return BeautifulSoup(page.text, 'html.parser')

def get_green_leaders(soup):
    # # Find and extract attributes from elements
    # image_url = soup.find("img", class_="thumbnail")["src"]
    # Three levels: Bronze, Silver, Gold, and Platinum
    

   
  
    if(soup.find_all("div", class_="tkXGS f PP _S")):
        # Extract text content from other elements
        green_tags = [div.text for div in soup.find_all("div", class_="tkXGS f PP _S")]  
        green_found = False
        for green_tag in green_tags:
            if re.match(r'GreenLeaders.*', green_tag):
                green_leader_scores.append(green_tag)
                green_found = True
                break
        if green_found is False:
            green_leader_scores.append('none')
            print("NO GREEN LEADER SCORE")
        else:
            print("GREEN LEADER SCORE")



page_contents = []
green_leader_scores = []
hotel_links = ['https://www.tripadvisor.com/Hotel_Review-g33300-d1391728-Reviews-Bardessono_Hotel_and_Spa-Yountville_Napa_Valley_California.html', 'https://www.tripadvisor.com/Hotel_Review-g33052-d2257239-Reviews-Shore_Hotel-Santa_Monica_California.html']

# Get all the content in each page 
for x in range(len(hotel_links)):
    soup = get_page_contents(hotel_links[x])
    page_contents.append(soup)

# Get all the data to every hotel in Orange County from each page content 
for x in range(len(hotel_links)):  
    get_green_leaders(page_contents[x])

print(green_leader_scores)

# Create the dictionary.
dict = {}

# Create the dataframe.
orangeCounty = pd.DataFrame.from_dict(dict)
orangeCounty.head(10)

# Convert dataframe to CSV file.
orangeCounty.to_csv('greenLeadersData.csv', index=False, header=True)
print("Done")


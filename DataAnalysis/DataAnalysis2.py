import pandas as pd
import openpyxl
from openpyxl.utils.exceptions import IllegalCharacterError
from lxml import etree
from collections import Counter
import itertools 
import re
import numpy as np

# Create a new workbook
workbook = openpyxl.Workbook()
# Select the active worksheet
worksheet = workbook.active

class Analysis:
    # Get the top 10 hotels based on provided column data
    def get_top_10(df, col):
        # Drop rows with 'none' in the 'Hotel Name' column
        df = df[df['Hotel Name'] != 'none']
        # Sort the DataFrame by the specified column in descending order and extract the top 10 rows
        top_10 = df.sort_values(col, ascending=False).head(10)
        return top_10
    
    def get_hotel_keywords(df, top_10):
        top_10_list = top_10['Hotel Name'].tolist()
        results = []

        # Loop over the top 10 hotels and get keywords
        for hotel in top_10_list:
            # Get the rows with specific hotel name
            specified_rows = df[df.iloc[:,0] == hotel]
            keywords_list = []

            for i in range(len(specified_rows)):
                # Get the keywords for the current row
                current_row_keywords = []
                if specified_rows.iloc[i]['Enviornmental Keywords'] != 'none':
                    current_row_keywords.append((specified_rows.iloc[i]['Enviornmental Keywords'], 'Environmental'))

                if specified_rows.iloc[i]['Social Keywords'] != 'none':
                    current_row_keywords.append((specified_rows.iloc[i]['Social Keywords'], 'Social'))

                if specified_rows.iloc[i]['Cultural Keywords'] != 'none':
                    current_row_keywords.append((specified_rows.iloc[i]['Cultural Keywords'], 'Cultural'))

                if specified_rows.iloc[i]['Economic Keywords'] != 'none':
                    current_row_keywords.append((specified_rows.iloc[i]['Economic Keywords'], 'Economic'))

                if specified_rows.iloc[i]['Policy Keywords'] != 'none':
                    current_row_keywords.append((specified_rows.iloc[i]['Policy Keywords'], 'Policy'))

                # Append the keywords to the list of keywords for the hotel
                keywords_list.extend(current_row_keywords)

            # Add the list of keywords for the hotel to the results list
            results.append((hotel, keywords_list))

        return results

    # def get_keyword_category(keyword):
    #     for category in ['Social Keywords', 'Cultural Keywords', 'Economic Keywords', 'Policy Keywords']:
    #         if keyword in df[category].tolist():
    #             return category
    #     return "Unknown"

    def get_top_10_keywords(df, col):
        top_10_keywords = df[col].tolist()
        # Exclude 'none', so it won't be counted as a common word
        top_10_keywords = [word for word in top_10_keywords if word != "none"]
        word_counts = Counter(top_10_keywords)

        result = []
        for word, count in word_counts.most_common(10):
            result.append((word, count))
        return result
    
    # Get top 5 most sustainable hotels in each hotel star rating
    def get_top_5_stars(df):
        # Sort the DataFrame by both the Hotel Rating and Hotel Sustainability Average columns
        df_sorted = df.sort_values(['Hotel Rating', 'Hotel Sustainabilty Average'], ascending=[True, False])

        # Group the sorted DataFrame by Hotel Rating and extract the top 5 hotels from each group
        top_5 = df_sorted.groupby('Hotel Rating').head(5)

        # Create a dictionary to store the top 5 hotels for each rating
        results_dict = {}

        # Extract the top 5 hotels for each rating and add them to the dictionary
        for rating in df['Hotel Rating'].unique():
            hotels = top_5.loc[top_5['Hotel Rating'] == rating][['Hotel Name', 'Hotel Sustainabilty Average']]
            hotels_list = [(hotel[0], hotel[1]) for hotel in hotels.values]
            results_dict[rating] = hotels_list
        return results_dict

    # def get_top_5_by_price_range(df):
    #     # Convert the 'Hotel Price Range' column to string type
    #     df['Hotel Price Range'] = df['Hotel Price Range'].astype(str)
        
    #     # Extract numeric values or NaN from the 'Hotel Price Range' column using regular expression
    #     def get_price_range_average(value):
    #         if value.lower() in ['none', 'nan']:
    #             return np.nan
    #         match = re.search(r'\$(\d+)\s*-\s*\$(\d+)', value)
    #         if match:
    #             low, high = map(int, match.groups())
    #             return (low + high) / 2
    #         return np.nan
    #     df['Price Range Average'] = df['Hotel Price Range'].apply(get_price_range_average)
        
    #     # Create a new column that categorizes the hotel prices into the price ranges using 'pd.cut' function
    #     df['Price Range Category'] = pd.cut(df['Price Range Average'], 
    #                                         bins=[0, 100, 200, 300, 400, np.inf], 
    #                                         labels=['Below $100', '$100-$200', '$201-$300', '$301-$400', 'Above $400'])
        
    #     # Group the DataFrame by the price range categories and calculate the average sustainability for each category
    #     price_range_avg = df.groupby('Price Range Category')['Hotel Sustainabilty Average'].mean()
        
    #     # Get the top 5 hotels by sustainability in each price range category
    #     top_5_by_price_range = pd.DataFrame(columns=['Price Range Category', 'Hotel Name', 'Hotel Sustainabilty Average'])
    #     for category in price_range_avg.index:
    #         # Get the top 5 hotels by sustainability for the current category
    #         top_5 = df[df['Price Range Category'] == category].sort_values('Hotel Sustainabilty Average', ascending=False).head(5)
    #         # Add the category column to the top 5 DataFrame
    #         top_5['Price Range Category'] = category
    #         # Append the top 5 DataFrame to the final DataFrame
    #         top_5_by_price_range = top_5_by_price_range.append(top_5[['Price Range Category', 'Hotel Name', 'Hotel Sustainabilty Average']])
        
    #     return top_5_by_price_range


    def get_top_5_by_price_range(df):
        # Convert the 'Hotel Price Range' column to string type
        df['Hotel Price Range'] = df['Hotel Price Range'].astype(str)

        # Extract numeric values from the 'Hotel Price Range' column using regular expression
        price_range_regex = r'\$(\d+)\s*-\s*\$(\d+)'
        # Extracts numeric value from the 'Hotel Price Range' column using the str.extract() method and converts it to an integer using the astype() method
        df[['Price Range Low', 'Price Range High']] = df['Hotel Price Range'].str.extract(price_range_regex).astype(float)
        df.loc[df['Hotel Price Range'].str.lower().str.contains('none'), ['Price Range Low', 'Price Range High']] = np.nan
        df['Price Range Average'] = df[['Price Range Low', 'Price Range High']].mean(axis=1, skipna=True)
        
        # Create a new column that categorizes the hotel prices into the price ranges using 'pd.cut' function
        df['Price Range Category'] = pd.cut(df['Price Range Average'], 
                                            bins=[0, 100, 200, 300, 400, np.inf], 
                                            labels=['Below $100', '$100-$200', '$201-$300', '$301-$400', 'Above $400'])
        
        # Group the DataFrame by the price range categories and calculate the average sustainability for each category
        price_range_avg = df.groupby('Price Range Category')['Hotel Sustainabilty Average'].mean()
        
        # Get the top 5 hotels by sustainability in each price range category
        top_5_by_price_range = pd.DataFrame(columns=['Price Range Category', 'Hotel Name', 'Hotel Sustainabilty Average'])
        for category in price_range_avg.index:
            # Get the top 5 hotels by sustainability for the current category
            top_5 = df[df['Price Range Category'] == category].sort_values('Hotel Sustainabilty Average', ascending=False).head(5)
            # Add the category column to the top 5 DataFrame
            top_5['Price Range Category'] = category
            # Append the top 5 DataFrame to the final DataFrame
            top_5_by_price_range = top_5_by_price_range.append(top_5[['Price Range Category', 'Hotel Name', 'Hotel Sustainabilty Average']])
        
        return top_5_by_price_range

    
    def update_excel(data_dict, worksheet, skip_columns_after=None):
        # Clear the existing data in the worksheet
        worksheet.delete_rows(1, worksheet.max_row)

        # Write the headers to the first row
        headers = list(data_dict.keys())
        col_index = 1
        for header in headers:
            if header in skip_columns_after:
                worksheet.cell(row=1, column=col_index).value = header
                worksheet.cell(row=1, column=col_index + 1).value = ''
                worksheet.cell(row=1, column=col_index + 2).value = ''
                col_index += 3
            else:
                worksheet.cell(row=1, column=col_index).value = header
                col_index += 1

        # Pad the shorter lists with empty values
        max_length = max([len(data_dict[key]) for key in headers])
        for key, value in data_dict.items():
            if len(value) < max_length:
                data_dict[key] += [''] * (max_length - len(value))

        # Write the data to the remaining rows
        for i in range(max_length):
            col_index = 1
            for header in headers:
                if header in skip_columns_after:
                    worksheet.cell(row=i+2, column=col_index).value = data_dict[header][i]
                    worksheet.cell(row=i+2, column=col_index + 1).value = ''
                    worksheet.cell(row=i+2, column=col_index + 2).value = ''
                    col_index += 3
                else:
                    worksheet.cell(row=i+2, column=col_index).value = data_dict[header][i]
                    col_index += 1

        # Check if there are any invalid XML elements in the workbook
        with open("data_analysis2.xlsx", "rb") as f:
            try:
                etree.parse(f)
            except etree.XMLSyntaxError as e:
                print(f"\nInvalid XML element found in workbook: {e.args[0]}")

        # Save the workbook
        workbook.save("data_analysis2.xlsx")


    
if __name__ == "__main__":
    # Create a dictionary with initially with no data
    research_ques = {'Top 10 Sustainable Hotels':[], 'Sustainability Score':[], 'Total Number of Reviews':[],'Environmental Keywords':[], 'Social Keywords':[],
                        'Cultural Keywords':[], 'Economic Keywords':[], 'Policy Keywords':[], 'Top 10 Enviornmental Keywords':[], 'Top 10 Social Keywords':[], 
                        'Top 10 Cultural Keywords':[], 'Top 10 Economic Keywords' :[], 'Top 10 Policy Keywords':[], 
                        'Top 5 5-star':[],'Top 5 5-star Score':[], 'Top 5 4.5-star':[], 'Top 5 4.5-star Score':[], 'Top 5 4-star':[], 'Top 5 4-star Score':[], 
                        'Top 5 3.5-star':[], 'Top 5 3.5-star Score':[],'Top 5 3-star':[], 'Top 5 3-star Score':[], 'Top 5 2.5-star':[], 'Top 5 2.5-star Score':[],
                        'Top 5 2-star':[], 'Top 5 2-star Score':[],'Top 5 1.5-star':[], 'Top 5 1.5-star Score':[], 'Top 5 1-star':[], 'Top 5 1-star Score':[], 
                        'Top 5 Below $100': [], 'Top 5 Below $100 Sustainability Score':[], 'Top 5 $100-$200': [], 'Top 5 $100-$200 Sustainability Score': [], 
                        'Top 5 $201-$300':[],'Top 5 $201-$300 Sustainability Score':[], 'Top 5 $301-$400':[],'Top 5 $301-$400 Sustainability Score':[], 
                        'Top 5 Above $400':[], 'Top 5 Above $400 Sustainability Score':[]
                        }

    # # Get top 10 hotels with highest sustainabilty score 
    # df = pd.read_excel('data_analysis.xlsx', usecols=['Hotel Name','Hotel Sustainabilty Average', 'Total Number of Reviews', 'Enviornmental Keywords', 
    #                                                   'Social Keywords', 'Cultural Keywords','Economic Keywords', 'Policy Keywords'])
    # # Filter the data frame based on the condition
    # df = df[df['Total Number of Reviews'] > 100]

    # print("Processing...top 10")
    # top_10 = Analysis.get_top_10(df, 'Hotel Sustainabilty Average')
    # top_10_hotel_names = top_10['Hotel Name'].tolist()
    # top_10_hotel_scores = top_10['Hotel Sustainabilty Average'].tolist()
    # top_10_hotel_total_num_reviews = top_10['Total Number of Reviews'].tolist()

    # # Append top 10 hotels with highest sustainabilty score to dictionary 
    # for hotel_name, hotel_score, hotel_total_review in zip(top_10_hotel_names, top_10_hotel_scores, top_10_hotel_total_num_reviews):
    #     research_ques['Top 10 Sustainable Hotels'].append(hotel_name)
    #     research_ques['Sustainability Score'].append(hotel_score)
    #     research_ques['Total Number of Reviews'].append(hotel_total_review)

    # # Get all review keywords from top 10 hotels
    # top_10_with_keywords = Analysis.get_hotel_keywords(df,top_10)

    # # For each sustainability category append the keyword found for each hotel    
    # for hotel, keywords in top_10_with_keywords:
    #     # print(hotel)
    #     # Set so results do not contain duplicates before appending to 'research_ques' dict 
    #     enviornmental = []
    #     social = []
    #     cultural = []
    #     economic = []
    #     policy = []
    #     # For each hotel find the keywords and append them to specific list depending on the category
    #     for keyword, category in keywords:
    #         # Normalize keyword by converting to lowercase, removing punctuation, and splitting on commas
    #         keyword = keyword.lower().strip('.,;:')
    #         keywords_list = [k.strip() for k in keyword.split(',')]
    #         for k in keywords_list:
    #             if category == 'Environmental':
    #                 enviornmental.append(k)
    #             if category == 'Social':
    #                 social.append(k)
    #             if category == 'Cultural':
    #                 cultural.append(k)
    #             if category == 'Economic':
    #                 economic.append(k)
    #             if category == 'Policy':
    #                 policy.append(k)
    #         # print(f"\t{category}: {k}")

    #     # Count the duplicates in each sustainability category list
    #     environmental_counts = Counter(enviornmental)
    #     social_counts = Counter(social)
    #     cultural_counts = Counter(cultural)
    #     economic_counts = Counter(economic)
    #     policy_counts = Counter(policy)
        
    #     # Append count data for each category to corresponding key in dictionary
    #     research_ques['Environmental Keywords'].append(", ".join([f"{k}: {v}" for k, v in environmental_counts.items()]))
    #     research_ques['Social Keywords'].append(", ".join([f"{k}: {v}" for k, v in social_counts.items()]))
    #     research_ques['Cultural Keywords'].append(", ".join([f"{k}: {v}" for k, v in cultural_counts.items()]))
    #     research_ques['Economic Keywords'].append(", ".join([f"{k}: {v}" for k, v in economic_counts.items()]))
    #     research_ques['Policy Keywords'].append(", ".join([f"{k}: {v}" for k, v in policy_counts.items()]))
    #     enviornmental.clear()
    #     social.clear()
    #     cultural.clear()
    #     economic.clear()
    #     policy.clear()




    # # Get the top 10 keywords from each category 
    # df2 = pd.read_excel('data_analysis.xlsx', usecols=['Enviornmental Keywords', 'Social Keywords', 'Cultural Keywords',
    #                                                   'Economic Keywords', 'Policy Keywords'])
    # print("Processing...top enviornmental keywords")
    # top_10_enviornmental = Analysis.get_top_10_keywords(df2,'Enviornmental Keywords')
    # top_10_enviornmental_list = [str(item) for item in top_10_enviornmental]  # convert tuple to list of strings
    # print("Processing...top social keywords")
    # top_10_social = Analysis.get_top_10_keywords(df2,'Social Keywords')
    # top_10_social_list = [str(item) for item in top_10_social]  # convert tuple to list of strings
    # print("Processing...top cultural keywords")
    # top_10_cultural = Analysis.get_top_10_keywords(df2,'Cultural Keywords')
    # top_10_cultural_list = [str(item) for item in top_10_cultural]  # convert tuple to list of strings
    # print("Processing...top economic keywords") 
    # top_10_economic = Analysis.get_top_10_keywords(df2,'Economic Keywords')
    # top_10_economic_list = [str(item) for item in top_10_economic]  # convert tuple to list of strings
    # print("Processing...top policy keywords") 
    # top_10_policy = Analysis.get_top_10_keywords(df2,'Policy Keywords')
    # top_10_policy_list = [str(item) for item in top_10_policy]  # convert tuple to list of strings

    # print('Writing to dic')
    # # Append top 10 keywords from each category to dictionary
    # # itertools.zip_longest() function to iterate over all lists, even if they have different lengths, value of "" to fill any missing values.
    # for enviornmental_keywords, social_keywords, cultural_keywords, economic_keywords, policy_keywords in itertools.zip_longest(
    #         top_10_enviornmental_list, top_10_social_list, top_10_cultural_list, top_10_economic_list, top_10_policy_list,
    #         fillvalue=""):
    #     research_ques['Top 10 Enviornmental Keywords'].append(enviornmental_keywords)
    #     research_ques['Top 10 Social Keywords'].append(social_keywords)
    #     research_ques['Top 10 Cultural Keywords'].append(cultural_keywords)
    #     research_ques['Top 10 Economic Keywords'].append(economic_keywords)
    #     research_ques['Top 10 Policy Keywords'].append(policy_keywords)
    
    
    # df3 = pd.read_excel('data_analysis.xlsx', usecols=['Hotel Name','Hotel Rating', 'Hotel Sustainabilty Average', 'Total Number of Reviews'])
    # # Create a data frame without duplicates of hotel name
    # df3 = df3.drop_duplicates(subset=['Hotel Name'])
    # # Filter the data frame based on the condition
    # df3 = df3[df3['Total Number of Reviews'] > 100]

    # print("Finding top 5 hotels in each rating...")
    # # Results of the top 5 hotels in each rating based on 'Hotel Sustainabilty Average'
    # results_dict = Analysis.get_top_5_stars(df3)
    # # Append top 5 hotels from each rating category to dictionary
    # for rating, hotels in results_dict.items():
    #     print(f'Top 5 most sustainable hotels with {rating} star rating:')
    #     for hotel in hotels:
    #         if rating == '5':
    #             research_ques['Top 5 5-star'].append(hotel[0])
    #             research_ques['Top 5 5-star Score'].append(hotel[1])
    #         elif rating == '4.5':
    #             research_ques['Top 5 4.5-star'].append(hotel[0])
    #             research_ques['Top 5 4.5-star Score'].append(hotel[1])
    #         elif rating == '4':
    #             research_ques['Top 5 4-star'].append(hotel[0])
    #             research_ques['Top 5 4-star Score'].append(hotel[1])
    #         elif rating == '3.5':
    #             research_ques['Top 5 3.5-star'].append(hotel[0])
    #             research_ques['Top 5 3.5-star Score'].append(hotel[1])
    #         elif rating == '3':
    #             research_ques['Top 5 3-star'].append(hotel[0])
    #             research_ques['Top 5 3-star Score'].append(hotel[1])
    #         elif rating == '2.5':
    #             research_ques['Top 5 2.5-star'].append(hotel[0])
    #             research_ques['Top 5 2.5-star Score'].append(hotel[1])
    #         elif rating == '2':
    #             research_ques['Top 5 2-star'].append(hotel[0])
    #             research_ques['Top 5 2-star Score'].append(hotel[1])
    #         elif rating == '1.5':
    #             research_ques['Top 5 1.5-star'].append(hotel[0])
    #             research_ques['Top 5 1.5-star Score'].append(hotel[1])
    #         elif rating == '1':
    #             research_ques['Top 5 1-star'].append(hotel[0])
    #             research_ques['Top 5 1-star Score'].append(hotel[1])

    #         print(f'{hotel[0]}: {hotel[1]}')

    df4 = pd.read_excel('data_analysis.xlsx', usecols=['Hotel Name','Hotel Price Range', 'Hotel Sustainabilty Average', 'Total Number of Reviews'])
    # Create a data frame without duplicates of hotel name
    df4= df4.drop_duplicates(subset=['Hotel Name'])
    # Filter the data frame based on the condition
    df4 = df4[df4['Total Number of Reviews'] > 100]

    print("Finding top 5 hotels in each price range...")
    # Results of the top 5 hotels in each price range based on 'Hotel Sustainabilty Average'
    top_5_hotels_by_price_range = Analysis.get_top_5_by_price_range(df4)
    print(top_5_hotels_by_price_range)

    # loop through each price range category and add the top 5 hotels to the dictionary
    for category in top_5_hotels_by_price_range['Price Range Category'].unique():
        hotels = top_5_hotels_by_price_range[top_5_hotels_by_price_range['Price Range Category'] == category][['Hotel Name', 'Hotel Sustainabilty Average']]
        for index, row in hotels.iterrows():
            if category == 'Below $100':
                research_ques['Top 5 Below $100'].append(row['Hotel Name'])
                research_ques['Top 5 Below $100 Sustainability Score'].append(row['Hotel Sustainabilty Average'])
            if category == '$100-$200':
                research_ques['Top 5 $100-$200'].append(row['Hotel Name'])
                research_ques['Top 5 $100-$200 Sustainability Score'].append(row['Hotel Sustainabilty Average'])
            if category == '$201-$300':
                research_ques['Top 5 $201-$300'].append(row['Hotel Name'])
                research_ques['Top 5 $201-$300 Sustainability Score'].append(row['Hotel Sustainabilty Average'])
            if category == '$301-$400':
                research_ques['Top 5 $301-$400'].append(row['Hotel Name'])
                research_ques['Top 5 $301-$400 Sustainability Score'].append(row['Hotel Sustainabilty Average'])
            if category == 'Above $400':
                research_ques['Top 5 Above $400'].append(row['Hotel Name'])
                research_ques['Top 5 Above $400 Sustainability Score'].append(row['Hotel Sustainabilty Average'])
        print(f'Top 5 {category}: {row}')

    # Update results to excel file
    Analysis.update_excel(research_ques, worksheet, skip_columns_after=['Policy Keywords', 'Top 10 Policy Keywords', 'Top 5 1-star Score'])




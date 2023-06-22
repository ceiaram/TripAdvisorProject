import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# df = pd.read_excel('sentiment_analysis_data.xlsx', usecols=['Sustainabilty Score', 'Sentiment Negative Score', 'Sentiment Positive Score',
#             'Sentiment Neutral Score', 'Sentiment Negative + Neutral Score', 'Sentiment Positive + Neutral Score'])

#     # # Plot the actual sentiment score by sustainability score
#     # plt.scatter(df['Sustainabilty Score'], df['Sentiment Positive Score'])
#     # plt.xlabel('Sustainability Score')
#     # plt.ylabel('Sentiment Positive Score')
#     # plt.title('Actual Sentiment Score by Sustainability Score')
#     # plt.show()
    
#     # Set up colors/markers for different sentiment scores
# colors = {
#         'Sentiment Negative Score': 'red',
#         'Sentiment Positive Score': 'green',
#         'Sentiment Neutral Score': 'blue',
#         'Sentiment Negative + Neutral Score': 'orange',
#         'Sentiment Positive + Neutral Score': 'pink'
# }

#  # Plot the sentiment scores by sustainability score
# plt.figure(figsize=(8, 6))
# for sentiment, color in colors.items():
#     plt.scatter(df['Sustainabilty Score'], df[sentiment], label=sentiment, color=color)

# plt.xlabel('Sustainability Score')
# plt.ylabel('Sentiment Score')
# plt.title('Sentiment Scores by Sustainability Score')
# plt.legend()
# plt.show()


# Load the dataset
df = pd.read_excel('sentiment_analysis_data.xlsx')

# Set up sentiment scores and corresponding indices for the x-axis
sentiment_scores = ['Sentiment Negative Score', 'Sentiment Positive Score', 'Sentiment Neutral Score', 'Sentiment Negative + Neutral Score']
x_indices = np.arange(len(sentiment_scores))

# Get the mean sustainability scores for each sentiment score
mean_sustainability_scores = [df[score].mean() for score in sentiment_scores]

# Plot the bar graph
plt.figure()
plt.bar(x_indices, mean_sustainability_scores)

# Customize the x-axis tick labels
plt.xticks(x_indices, sentiment_scores, rotation=45,  ha='right')

plt.xlabel('Sentiment Scores')
plt.ylabel('Mean Sustainability Score')
plt.title('Mean Sustainability Score by Sentiment Scores')

plt.tight_layout()  # Adjust layout to prevent label cutoff

# Save graph as .png
plt.savefig('sustainability_score_at_different_sentiments.png')
plt.show()



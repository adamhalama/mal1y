import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import pandas as pd

import folium
import folium.plugins as plugins

airbnbSheet = pd.read_csv("../data/listings.csv")

desiredColumns = [
    'id',
    'name',
    'host_id',
    'host_name',
    'neighbourhood_cleansed',
    'latitude',
    'longitude',
    'room_type',
    'price',
    'minimum_nights',
    'number_of_reviews',
    'last_review',
    'review_scores_rating',
    'review_scores_accuracy',
    'review_scores_cleanliness',
    'review_scores_checkin',
    'review_scores_communication',
    'review_scores_location',
    'review_scores_value',
    'reviews_per_month',
    'calculated_host_listings_count',
    'availability_365',
]

fas = airbnbSheet[desiredColumns]  # keep only these columns
fas = fas.dropna()  # drop columns with empty vals
# drop if num of reviews is 0
fas = fas.drop(fas[fas.number_of_reviews > 1].index)


""" #APPARTMENT NAMES:
# Combine all the names into a single string

text = " ".join(name for name in fas['name'].astype(str))

# List of words to remove
stopwords = set(["Copenhagen", "CPH", "the", "to", "and", "of", "in", "og", "i", "at", "a"])

# Generate the word cloud
wordcloud = WordCloud(stopwords=stopwords, background_color="grey").generate(text)

# Display the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show() #uncomment to show the wordcloud """

# HOST NAMES:

# Combine all the host names into a single string
text = " ".join(name for name in fas['host_name'].astype(str))

# List of words to remove (non-person names, or common words that might appear as host names)
# This list should be expanded based on the data and common non-person names you observe
# Replace with actual non-person names or words
stopwords = set(["Host1", "Host2", "ApartmentinCopenhagen"])

# Generate the word cloud
wordcloud = WordCloud(stopwords=stopwords,
                      background_color="grey").generate(text)

# Display the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
# plt.show()


# the price values are in dollars
fas = fas.rename(columns={'price': 'price_in_dollars'})

# remove the dollar sign from the numbers
fas['price_in_dollars'] = fas['price_in_dollars'].str.replace(
    '$', '', regex=False).str.replace(',', '').astype(float)

bins = [0, 1_000, 2_000, 3_000, 4_000, 5_000, 6_000,
        7_000, 8_000, 9_000, 10_000, float('inf')]
labels = ['$0-1,000', '$1,000-2,000', '$2,000-3,000', '$3,000-4,000', '$4,000-5,000',
          '$5,000-6,000', '$6,000-7,000', '$7,000-8,000', '$8,000-9,000', '$9,000-10,000', '$10,000+']

fas['price_bin'] = pd.cut(fas['price_in_dollars'],
                          bins=bins, labels=labels, right=False)

print(fas[['price_in_dollars', 'price_bin']])


# 7.

color_map = {
    '$0-1,000': 'green',
    '$1,000-2,000': 'blue',
    '$2,000-3,000': 'lightblue',
    '$3,000-4,000': 'yellow',
    '$4,000-5,000': 'orange',
    '$5,000-6,000': 'darkorange',
    '$6,000-7,000': 'orangered',
    '$7,000-8,000': 'red',
    '$8,000-9,000': 'darkred',
    '$9,000-10,000': 'purple',
    '$10,000+': 'black'
}


# Create a base map centered around Copenhagen
m = folium.Map(location=[55.6761, 12.5683], zoom_start=12)

# Add listings to the map using the price bins for color
for idx, row in fas.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color=color_map[row['price_bin']],
        fill=True,
        fill_color=color_map[row['price_bin']]
    ).add_to(m)

# Display the map (if you're in Jupyter Notebook)
m

m.save('listings_map.html')


# Get a list of unique neighborhoods
neighborhoods = fas['neighbourhood_cleansed'].unique()

# Create a colormap
colors_array = cm.rainbow(np.linspace(0, 1, len(neighborhoods)))
rainbow = [colors.rgb2hex(i) for i in colors_array]
neighborhood_color_map = dict(zip(neighborhoods, rainbow))


m2 = folium.Map(location=[55.6761, 12.5683], zoom_start=12)

# Add listings to the map using neighborhoods for color
for idx, row in fas.iterrows():
    neighborhood = row['neighbourhood_cleansed']
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color=neighborhood_color_map[neighborhood],
        fill=True,
        fill_color=neighborhood_color_map[neighborhood],
        fill_opacity=0.7
    ).add_to(m2)

# Display the map (if you're in Jupyter Notebook)
m2

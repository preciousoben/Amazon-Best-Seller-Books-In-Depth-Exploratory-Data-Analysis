#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

bestseller_books_df = pd.read_csv('BestSeller Books of Amazon.csv')

bestseller_books_df.info(), bestseller_books_df.head()


# In[3]:


import pandas as pd

# missing records
print("Checking for missing records...")
missing_values = bestseller_books_df.isnull().sum()
print(missing_values)

# duplicates based on Book Name and Author Name
print("\nChecking for duplicate records...")
duplicates = bestseller_books_df.duplicated(subset=['Book Name', 'Author Name'])
duplicate_records = bestseller_books_df[duplicates]
print(duplicate_records)

# dropping duplicates
bestseller_books_df = bestseller_books_df.drop_duplicates(subset=['Book Name', 'Author Name'])

# Saving the cleaned DataFrame to a new CSV file
bestseller_books_df.to_csv('cleaned_bestseller_books.csv', index=False)

# cleaned DataFrame
print("\nCleaned DataFrame:")
print(bestseller_books_df.head())


# In[4]:


# cleaning the price column
bestseller_books_df['Price'] = bestseller_books_df['Price'].replace('[₹,]', '', regex=True).astype(float)

# cleaned data and its structure
bestseller_books_df.info(), bestseller_books_df.head()


# In[5]:


import matplotlib.pyplot as plt
import seaborn as sns

summary_stats = bestseller_books_df.describe()
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

# Rating distributioon
sns.histplot(bestseller_books_df['Rating'], bins=10, kde=True, ax=axes[0], color='blue')
axes[0].set_title('Distribution of Ratings')
axes[0].set_xlabel('Rating')
axes[0].set_ylabel('Frequency')

# Price distribution
sns.histplot(bestseller_books_df['Price'], bins=10, kde=True, ax=axes[1], color='green')
axes[1].set_title('Distribution of Prices')
axes[1].set_xlabel('Price')
axes[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

summary_stats


# In[6]:


# Scatter plot for Rating vs. Price
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Rating', y='Price', data=bestseller_books_df, color='purple')
plt.title('Rating vs. Price')
plt.xlabel('Rating')
plt.ylabel('Price')
plt.show()


# In[7]:


correlation = bestseller_books_df['Price'].corr(bestseller_books_df['Rating'])
print(f"Correlation between Price and Rating: {correlation}")


# In[9]:


# average rating by author name
top_authors = bestseller_books_df.groupby('Author Name').agg(
    avg_rating=('Rating', 'mean'),
    avg_price=('Price', 'mean')
).sort_values(by='avg_rating', ascending=False).head(10)

# top authors
print(top_authors)


# In[110]:


least_rated_book = bestseller_books_df.loc[bestseller_books_df['Rating'].idxmin()]

# highest rated book
highest_rated_book = bestseller_books_df.loc[bestseller_books_df['Rating'].idxmax()]

print("Least Rated Book:")
print(least_rated_book)

print("\nHighest Rated Book:")
print(highest_rated_book)


# In[111]:


# average rating and price for the author of the least rated book
least_rated_author = least_rated_book['Author Name']
least_rated_author_avg_rating = bestseller_books_df[bestseller_books_df['Author Name'] == least_rated_author]['Rating'].mean()
least_rated_author_avg_price = bestseller_books_df[bestseller_books_df['Author Name'] == least_rated_author]['Price'].mean()

# average rating and price for the author of the highest rated book
highest_rated_author = highest_rated_book['Author Name']
highest_rated_author_avg_rating = bestseller_books_df[bestseller_books_df['Author Name'] == highest_rated_author]['Rating'].mean()
highest_rated_author_avg_price = bestseller_books_df[bestseller_books_df['Author Name'] == highest_rated_author]['Price'].mean()

print(f"\nAverage Rating of {least_rated_author}: {least_rated_author_avg_rating}")
print(f"Average Price of {least_rated_author}: {least_rated_author_avg_price}")

print(f"\nAverage Rating of {highest_rated_author}: {highest_rated_author_avg_rating}")
print(f"Average Price of {highest_rated_author}: {highest_rated_author_avg_price}")


# In[112]:


import pandas as pd
author_stats = bestseller_books_df.groupby('Author Name').agg(
    avg_rating=('Rating', 'mean'),
    avg_price=('Price', 'mean')
).sort_values(by='avg_rating', ascending=True).head(10)

# authors with the lowest average ratings and their average prices
print("Authors with the Lowest Average Ratings and Their Average Prices:")
print(author_stats)


# In[113]:


# most common prices
common_prices = bestseller_books_df['Price'].value_counts().head(10)

print("Most Common Price Points:")
print(common_prices)


# In[114]:


# Price distribution by rating levels
plt.figure(figsize=(10, 6))
sns.boxplot(x='Rating', y='Price', data=bestseller_books_df)
plt.title('Price Distribution by Rating')
plt.xlabel('Rating')
plt.ylabel('Price')
plt.show()


# In[115]:


books_df_sorted = bestseller_books_df.sort_values(by='Rating', ascending=False)

# top 10 highest rated books and bottom 10 least rated books
top_ten_highest_rated = books_df_sorted.head(10)
bottom_ten_rated = books_df_sorted.tail(10)

# concatenating top 10 and least 10 rated books into one dataframe
combined_df = pd.concat([top_ten_highest_rated, bottom_ten_rated], ignore_index=True)

# combined DataFrame
print("Combined DataFrame of top 10 highest rated and bottom 10 least rated books:")
print(combined_df)


# # Including Genres
# To add more meaning to our analysis, we decided to include an analysis of the genres of the books. Genres were not provided in the initial database. To achieve this, we fetched the genres from Google Books (as shown below) and updated our dataframe.
# 
# This was done for the top 10 rated and 10 least rated books.
# 
# For the books whose genres were not found on Google Books, we pulled them from Open Library. However, some books still didn't have genres. For these ones, we entered their genres manually.

# In[116]:


def fetch_book_genre(book_title):
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': f'intitle:{book_title}'}
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            volume_info = data['items'][0]['volumeInfo']
            if 'categories' in volume_info:
                return volume_info['categories']
    
    return None

# Function to fetch genres for all books in the Combined DataFrame and add as a new column
def fetch_and_add_genres(df):
    df['Genres'] = df['Book Name'].apply(fetch_book_genre)

fetch_and_add_genres(combined_df)

# updated Combined DataFrame with genres
print("Updated Combined DataFrame with genres:")
print(combined_df)


# In[117]:


combined_df


# In[118]:


import requests
import pandas as pd

data = {
    'Book Name': [
        'Shrimad Bhagwat Geeta Yatharoop (Hindi)',
        'All In One English Core class 12th Based On Latest CBSE Syllabus',
        'PW Calculus Core Fear No More Calculus Book By Sachin Jakhar',
        'Maths Concept King All Formulas and Theorum | Gagan Pratap Sir',
        'The Magic of the Lost Temple',
        'Courage To Be Disliked, The: How to free yourself, change your life and achieve real happiness',
        '1001 Ultimate Brain Booster Activities for 4+ Kids',
        "Grandma's Bag of Stories: Collection of 20+ Illustrated short stories",
        'Indian Polity for UPSC (English)|7th Edition|Civil Services Preliminary and Main Examinations|',
        '11 Rules For Life: Secrets to Level Up',
        'The Art of Laziness: Overcome Procrastination & Improve Your Productivity',
        'MTG Objective NCERT at your FINGERTIPS Chemistry',
        'Quantitative Aptitude for Competitive Examinations',
        'RAM C/O ANANDHI',
        'Writing Practice Boxset: Pack of 4 Books (Writing Fun: Write & Wipe)',
        'Nta Ugc Net \'24 Paper 1 By Kvs Madaan|Teaching & Research Aptitude|Complete Coverage With Notes, MCQs, Concept Mapping|Latest Edition',
        'All In One Social Science CBSE Class 10th Based on NCERT (Reduced Syllabus)',
        'SSC TCS PYQs Mathematics Chapterwise & Typewise Solved Papers (2015–2019)',
        'MINtile Sank Magic Practice Copybook, (4 Book Set) Sank Magic Writing',
        'Lucifer was Innocent: The Red Pill'
    ],
    'Author Name': [
        'A.C. Bhaktivendanta Swami Prabhupada',
        'Prerna Kain Srishti Agarwal',
        'Sachin Jakhar',
        'Gagan Pratap Sir',
        'Sudha Murty',
        'Ichiro Kishimi and Fumitake Koga',
        'Team Pegasus',
        'Murty Sudha',
        'M Laxmikanth',
        'Chetan Bhagat',
        'Library Mindset',
        'MTG Editorial Board',
        'R. S Aggarwal',
        'AKHIL P DHARMAJAN',
        'Wonder House Books',
        'KVS Madaan',
        'Susmita Dhar Kriti Arora',
        'Kiran Institute of Career Excellence',
        'Sank Magic',
        'Tirth Raj Parsana'
    ],
    'Rating': [4.8, 4.7, 4.7, 4.7, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.4, 4.4, 4.4, 4.4, 4.3, 4.2, 4.2, 4.1, 4.0, 3.6],
    'Price': [200.0, 370.0, 460.0, 239.0, 199.0, 329.0, 297.0, 199.0, 739.0, 183.0, 182.0, 435.0, 550.0, 306.0, 199.0, 330.0, 375.0, 548.0, 110.0, 369.0],
    'Genres': [
        ['Bhagavadgītā'], ['Study Aids'], None, None, ['Juvenile Fiction'], ['Philosophy'], None,
        ['Juvenile Fiction'], ['Study Aids'], ['Self-Help'], None, None, None, None, None, None,
        None, None, None, ['Fiction']
    ]
}

combined_df = pd.DataFrame(data)

# Open Library base URL
base_url = 'https://openlibrary.org/search.json'

# Function to get the genre of a book from Open Library
def get_genre_from_open_library(book_title):
    params = {'title': book_title}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        if results['numFound'] > 0:
            subject = results['docs'][0].get('subject', [])
            if subject:
                # Return the first subject as the genre
                return subject[0]
    return None

# update the DataFrame with genres from Open Library
def update_genres(df):
    for index, row in df.iterrows():
        if not row['Genres']:
            genre = get_genre_from_open_library(row['Book Name'])
            if genre:
                df.at[index, 'Genres'] = [genre]
            else:
                df.at[index, 'Genres'] = input(f"Enter the genre for the book '{row['Book Name']}': ").split(',')
    return df

# update the combined_df DataFrame
combined_df = update_genres(combined_df)

# updated DataFrame
print(combined_df)


# In[119]:


combined_df


# In[120]:


# cleaning the genre column
combined_df['Genres'] = combined_df['Genres'].apply(lambda genres: ', '.join(genres))

# extracting distinct genres
distinct_genres = combined_df['Genres'].explode().unique()

# displaying distinct genres
print("Distinct Genres:")
for genre in distinct_genres:
    print(genre)


# In[141]:


import pandas as pd

# defining a mapping dictionary for similar genres
genre_mapping = {
    "Study Aid": ["Study Aid", "Study Aids"],
    "Self-Help": ["Self Help", "Self-Help"],
    "Children's Books": ["Children's books"],
    "Juvenile Fiction": ["Juvenile Fiction"],
    "Fiction": ["Fiction"],
    "Philosophy": ["Philosophy"],
    "Fiction": ["Romance and Fiction"],  
    "Spiritual": ["Bhagavadgītā"]
}

# Function to normalize genres
def normalize_genres(genres_str):
    genres_list = genres_str.split(', ')
    normalized_genres = []
    for genre in genres_list:
        for normalized_genre, genre_aliases in genre_mapping.items():
            if genre in genre_aliases:
                normalized_genres.append(normalized_genre)
                break  
        else:
            normalized_genres.append(genre)  
    return ', '.join(normalized_genres)

combined_df['Genres'] = combined_df['Genres'].apply(normalize_genres)

# updated DataFrame
print(combined_df)


# In[142]:


combined_df


# In[143]:


import pandas as pd
import numpy as np

# one-hot encoding on the 'Genres' column
genres_encoded = combined_df['Genres'].str.join('|').str.get_dummies()

# calculating correlation with 'Rating' for each genre
genre_correlations = genres_encoded.apply(lambda x: combined_df['Rating'].corr(x))

# calculating the average correlation across all genre columns
overall_correlation = genre_correlations.mean()

# overall correlation
print(f"Overall correlation between Genres and Rating: {overall_correlation:.3f}")


# In[144]:


genre_avg_rating = combined_df.groupby('Genres')['Rating'].mean()

# genres by average rating in descending order
genre_avg_rating_sorted = genre_avg_rating.sort_values(ascending=False)

print("Ranking of Genres by Average Rating:")
print(genre_avg_rating_sorted)


# In[145]:


import pandas as pd

# Export to Excel with two sheets
with pd.ExcelWriter('Amazon_Best_Sellers.xlsx') as writer:
    bestseller_books_df.to_excel(writer, sheet_name='Best Sellers', index=False)
    combined_df.to_excel(writer, sheet_name='Best and least with genres', index=False)

print("DataFrames exported successfully to 'Amazon_Best_Sellers.xlsx'.")


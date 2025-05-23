import pandas as pd

# Load the dataset
movies = pd.read_csv('datasets/tmdb_5000_movies.csv')
credits = pd.read_csv('datasets/tmdb_5000_credits.csv')

# Merge datasets on title
movies = movies.merge(credits, on='title')
print(movies.head())

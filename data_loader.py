import pandas as pd
import numpy as np

# these are the two files we'll be using.
tmdb_movies = 'tmdb.movies.csv'
movie_budgets = 'tn.movie_budgets.csv'

genre_ids = {'10402':'music', \
			 '10749':'romance', \
			 '10751':'family', \
			 '10752':'war', \
			 '10770':'tv_movie', \
             '12':'adventure', \
			 '14':'fantasy', \
			 '16':'animation', \
			 '18':'drama', \
			 '27':'horror', \
			 '28':'action', \
             '35':'comedy', \
			 '36':'history', \
			 '37':'western', \
			 '53':'thriller', \
			 '80':'crime', \
             '878':'science_fiction', \
			 '9648':'mystery', \
			 '99':'documentary', \
			 '':'UNK'}

genre_list = list(sorted(genre_ids.values()))

def clean_money_string(amount):
    if type(amount) == str:
        return float(amount.replace(',', '').strip('$'))

def split_genres(genre_id_list):
    return [genre_ids[genre_id] for genre_id in genre_id_list.strip('[]').split(', ')]

def get_tm_movie_budgets():
    df = pd.read_csv(movie_budgets)
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['production_budget'] = df['production_budget'].apply(clean_money_string)
    df['dg'] = df['domestic_gross'].apply(clean_money_string)
    df['worldwide_gross'] = df['worldwide_gross'].apply(clean_money_string)
    df['rd'] = pd.to_datetime(df['release_date'])
    df['month'] = df['rd'].apply(lambda x: x.month)
    df['year'] = df['rd'].apply(lambda x: x.year)
    df['profitability'] = (df['worldwide_gross'] - df['production_budget']) / df['production_budget']
    return df[['movie', 'rd', 'month', 'year', 'production_budget', 'worldwide_gross', 'profitability']]

def get_tmdb_movies():
    df = pd.read_csv(tmdb_movies)
    df.release_date = pd.to_datetime(df.release_date)
    return df

def get_title_and_genres():
    df = get_tmdb_movies()
    df[df['original_language'] == 'en']
    df = df[['title', 'genre_ids']]
    df['genres'] = df.genre_ids.apply(split_genres)
    for genre in genre_list:
        df[genre] = df.genres.apply(lambda x: genre in x)
    return df.drop(['genres', 'genre_ids'], axis=1)

def merge_budgets_and_genres():
    budgets = get_tm_movie_budgets()
    genres = get_title_and_genres()
    return pd.merge(budgets, genres, left_on='movie', right_on='title', how='inner')\
		.drop('title', axis=1).drop_duplicates(['movie', 'rd']).sort_values('movie')

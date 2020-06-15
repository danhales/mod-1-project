import pandas as pd

title_principals = 'imdb.title.principals.csv'
movie_gross = 'bom.movie_gross.csv'
title_ratings = 'imdb.title.ratings.csv'
movie_info = 'rt.movie_info.tsv'
name_basics = 'imdb.name.basics.csv'
rt_reviews = 'rt.reviews.tsv'
title_akas = 'imdb.title.akas.csv'
title_basics = 'imdb.title.basics.csv'
tmdb_movies = 'tmdb.movies.csv'
title_crew = 'imdb.title.crew.csv'
movie_budgets = 'tn.movie_budgets.csv'

def preview_data(frame):
	"""
	prints columns, dtypes, and the first few rows
	"""
	print(frame.info())
	return frame.head()

def clean_money_string(amount):
	if type(amount) == str:
		return float(amount.replace(',', '').strip('$'))

def get_imdb_title_principles():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of imdb.title.principles.csv
	"""
	return pd.read_csv(title_principals)

def get_bom_movie_gross():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of bom.movie_gross.csv
	"""
	df = pd.read_csv(movie_gross)
	df['foreign_gross'] = df['foreign_gross'].apply(clean_money_string)
	df['foreign_gross'] = df['foreign_gross'].astype(float)
	return df

def get_imdb_title_ratings():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of imdb.title.ratings.csv
	"""
	return pd.read_csv(title_ratings)

def get_rt_movie_info():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of rt.movie_info.tsv
	"""
	df = pd.read_csv(movie_info, delimiter='\t')
	df['theater_date'] = pd.to_datetime(df['theater_date'])
	df['dvd_date'] = pd.to_datetime(df['dvd_date'])
	df['box_office'] = df['box_office'].apply(clean_money_string).astype(float)
	return df

def get_imdb_name_basics():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of imdb.name.basics.csv
	"""
	return pd.read_csv(name_basics)

def get_tmdb_movies():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of tmdb.movies.csv
	"""
	df = pd.read_csv(tmdb_movies)
	df.release_date = pd.to_datetime(df.release_date)
	return df

def get_rt_reviews():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of rt.reviews.tsv
	"""
	df = pd.read_csv(rt_reviews, delimiter='\t', encoding='ISO-8859-1')
	df['date'] = pd.to_datetime(df['date'])
	return df

def get_imdb_title_akas():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of imdb.title.akas.csv
	"""
	return pd.read_csv(title_akas)

def get_imdb_title_basics():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of imdb.title.basics.csv
	"""
	return pd.read_csv(title_basics)

def get_imdb_title_crew():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of imdb.title.crew
	"""
	return pd.read_csv(title_crew)

def get_tm_movie_budgets():
	"""
	Returns:
	DataFrame: a DataFrame with the contents of tn.movie_budgets.csv, modified
		to have the following columns:
			pb: production_budget (float instead of str)
			dg: domestic_gross (float instead of str)
			wg: worldwide_gross (float instead of str)
			rd: release_date (datetime instead of string)
			month: release month (int, 1-12)
			year: release year (int)
			profitability: (wg - pb) / pb (float)
	"""
	df = pd.read_csv(movie_budgets)
	df['release_date'] = pd.to_datetime(df['release_date'])
	df['pb'] = df['production_budget'].apply(clean_money_string)
	df['dg'] = df['domestic_gross'].apply(clean_money_string)
	df['wg'] = df['worldwide_gross'].apply(clean_money_string)
	df['rd'] = pd.to_datetime(df['release_date'])
	df['month'] = df['rd'].apply(lambda x: x.month)
	df['year'] = df['rd'].apply(lambda x: x.year)
	df['profitability'] = (df['wg'] - df['pb']) / df['pb']
	return df[['movie', 'rd', 'month', 'year', 'pb', 'dg', 'wg', 'profitability']]

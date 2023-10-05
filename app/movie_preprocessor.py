import pandas as pd
import requests
import sys
from tqdm import tqdm 
import time

def add_url(row):
    if len(row) <= 6:
        return f"https://www.imdb.com/title/tt{'0'*(7-len(row))}{row}/"
    
    else:
        return f"https://www.imdb.com/title/tt{row}/"

def add_rating(df):
    ratings_df = pd.read_csv('data/ratings.csv')
    agg_df = ratings_df.groupby(['movieId']).agg(
        rating_count = ('rating', 'count'),
        rating_avg = ('rating', 'mean')
        ).reset_index()

    rating_added_df = df.merge(agg_df, on = 'movieId')
    return rating_added_df

def add_poster(df):
    for i, row in tqdm(df.iterrows(), total = df.shape[0]):
        tmdb_id = row['tmdbId']
        tmdb_url = f"https://api.themoviedb.org/4/movie/{tmdb_id}?api_key=b9c3a9a62df9ac3f61e0d8b49233a9a1&language=en-US"
        result = requests.get(tmdb_url)
        
        try:
            df.at[i, 'poster_path'] = "https://image.tmdb.org/t/p/original" + result.json()['poster_path']
            time.sleep(0.1)
        except(TypeError, KeyError) as e:
            df.at[i, 'poster_path'] = "https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"
    return df

if __name__ == "__main__":
    movies_df = pd.read_csv('data/movies.csv')
    links_df = pd.read_csv('data/links.csv')
    merged_df = movies_df.merge(links_df, on = 'movieId', how = 'left')
    merged_df['url'] = merged_df['imdbId'].astype(str).apply(lambda s: add_url(s))
    result_df = add_rating(merged_df)
    result_df['poster_path'] = None
    result_df = add_poster(result_df)

    result_df.to_csv('data/movies_final.csv', index = None)    
    # print(merged_df.sample(2))
    # print(result_df.sample(2))
    # print(movies_df.head())
    # print(links_df.head())
    
    # print(merged_df.iloc[1, :])

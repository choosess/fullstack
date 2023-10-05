import pandas as pd
import requests

def add_url(row):
    if len(row) <= 6:
        return f"https://www.imdb.com/title/tt{'0'*(7-len(row))}{row}/"
    
    else:
        return f"https://www.imdb.com/title/tt{row}/"

if __name__ == "__main__":
    movies_df = pd.read_csv('data/movies.csv')
    links_df = pd.read_csv('data/links.csv')
    merged_df = movies_df.merge(links_df, on = 'movieId', how = 'left')
    merged_df['url'] = merged_df['imdbId'].astype(str).apply(lambda s: add_url(s))
    
    print(merged_df.sample(2))
    # print(movies_df.head())
    # print(links_df.head())
    # print(merged_df.iloc[1, :])
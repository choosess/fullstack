import pandas as pd

item_fname = 'data/movies_final.csv'

def random_items():
    movies_df = pd.read_csv(item_fname)
    movies_df = movies_df.fillna('')
    result_items = movies_df.sample(n = 10).to_dict('records')
    return result_items
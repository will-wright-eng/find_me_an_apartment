import sys
sys.path.append('./src/')

from src.module_clist.collect_clist import clean_clist_df
import pandas as pd

# Test to check if dataframe is not empty

def test_dataframe_not_empty():
    df = {'bedroom': [1], 'geotag_lat': [2], 'geotag_lon': [2], 'name': ["city"]}
    df = clean_clist_df(df)
    assert not df.empty, "Dataframe is empty"

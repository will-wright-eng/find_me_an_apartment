import sys
sys.path.append('.')

from src.module_clist.collect_clist import clean_clist_df
import pandas as pd

# Test to check if dataframe is not empty

def test_dataframe_not_empty():
    df = pd.DataFrame({'bedrooms': [1], 'geotag': ['56.98,24.07'], 'name': ["Riga"], 'available':"17.11"})
    df = clean_clist_df(df)
    assert not df.empty, "Dataframe is empty"

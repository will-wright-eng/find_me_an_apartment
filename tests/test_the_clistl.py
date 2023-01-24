import sys
sys.path.append('./src/')

from main_email import mail
from main_clist import collect_clist_data
import pandas as pd
import smtplib

# Test to check if dataframe is not empty
def test_dataframe_not_empty():
    df = collect_clist_data()
    assert not df.empty, "Dataframe is empty"

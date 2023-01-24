from main_email import mail
from main_clist import collect_clist_data
import pandas as pd
import smtplib

# Test to check if dataframe is not empty
def test_dataframe_not_empty():
    df = collect_clist_data()
    assert not df.empty, "Dataframe is empty"

# Test to check if mail server is closed
def test_mail_server_closed():
    server = mail("test_subject", "test_text")
    assert server.sock is None, "Mail server is not closed"

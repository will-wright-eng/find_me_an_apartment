'''
email_config.py
# email_config.password # password string
# email_config.myemail # email string
# email_config.recipients # list of strings
# email_config.recipients_test # single element list (which is a string)

Author: William Wright
'''

import datetime as dt
import module_email.send_email as send_email


def main():
    '''docstring for main'''
    today = str(dt.date.today())
    # to = recipients
    # attach = search_result_filenames
    subject = today + " Craigslist Test DAG"
    text = '''\nbody of email message\nby willcasswrig'''
    send_email.mail(subject, text)

if __name__ == '__main__':
    main()
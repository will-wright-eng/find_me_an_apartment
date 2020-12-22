'''
email module

email_config.py
# email_config.password # password string
# email_config.myemail # email string
# email_config.recipients # list of strings
# email_config.recipients_test # single element list (which is a string)

Author: William Wright
'''

import smtplib

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.message import Message
from email.mime.text import MIMEText
from email import encoders

import email_config

def mail(subject, text, attach=None, email_to=None):
    '''docstring for mail'''
    
    gmail_user = email_config.myemail
    gmail_pwd = email_config.password

    if email_to==None:
        email_to = email_config.recipients

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = gmail_user
    # msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    
    if attach != None:
        filenames = attach
        for file in filenames:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(cwd + file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % file)
            msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.starttls()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, email_to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    return mailServer.close()

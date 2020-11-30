'''
email module

Author: William Wright
'''

import config

def mail(to, subject, text, attach):
    '''docstring for mail'''
    filenames = attach
    gmail_user = config.myemail
    gmail_pwd = config.password

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    #get all the attachments
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
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    return mailServer.close()
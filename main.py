import smtplib
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pandas as pd


def SendBulkEmail():
    try:
        smtpcreds = getSMTPConfig()
        emailAddress = getEmailAddressFromCSV()
        # Login to SMTP
        session = smtplib.SMTP(str(smtpcreds[0]), int(smtpcreds[1]))
        session.starttls()
        session.login(str(smtpcreds[2]), str(smtpcreds[3]))

        # get email content
        mail_content = getEmailContent()
        mail_subject = smtpcreds[5]

        # Building Message
        for email in emailAddress:
            message = MIMEMultipart()
            message['From'] = str(smtpcreds[4])
            message['To'] = str(email)
            message['Subject'] = mail_subject
            message.attach(MIMEText(mail_content, 'plain'))
            text = message.as_string()
            session.sendmail(str(smtpcreds[2]), str(email), text)
            print("emailsend")
        session.quit()
    except:
        print("Something went wrong while logging: Unable to send email")


def getSMTPConfig():
    try:
        config = configparser.ConfigParser()
        config.read('SMTPconfig.properties')
        SMTPhost = config.get('SMTP', 'host').replace("'", "")
        SMTPport = int(config.get('SMTP', 'port').replace("'", ""))
        SMTPuser = config.get('SMTP', 'user').replace("'", "")
        SMTPpassword = config.get('SMTP', 'password').replace("'", "")
        SMTPfrom = config.get('SMTP', 'from').replace("'", "")
        EmailSubject = config.get('SMTP', 'EmailSubject').replace("'", "")
        return [SMTPhost, SMTPport, SMTPuser, SMTPpassword, SMTPfrom, EmailSubject]
    except:
        print("Something went wrong while logging: Unable to send email")


def getEmailContent():
    try:
        with open('Content.txt') as f:
            contents = f.read()
            return contents
    except:
        print("Something went wrong while logging: Unable to send email")


def getEmailAddressFromCSV():
    try:
        emailAddress = []
        emaildata = pd.read_csv("email.csv")
        emaillist = emaildata["Email"]
        for values in emaillist:
            emailAddress.append(values)

        return emailAddress
    except:
        print("Something went wrong while logging: Unable to send email")


if __name__ == '__main__':
    SendBulkEmail()

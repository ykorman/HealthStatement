
# credits: http://linuxcursor.com/python-programming/06-how-to-send-pdf-ppt-attachment-with-html-body-in-python-script

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_mail(creds, msg):
    server = smtplib.SMTP(creds['smtp'])
    server.starttls()
    server.login(creds['username'], creds['password'])
    message = MIMEMultipart()
    message['Subject'] = msg['subject']
    message['From'] = msg['from']
    message['To'] = msg['destination']
    message.attach(MIMEText(msg['body'], "plain"))
    with open(msg['attachment'], 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
    attachment.add_header('Content-Disposition', 'attachment', filename=str(msg['attachment']))
    message.attach(attachment)
    server.send_message(message)

if __name__ == "__main__":
    creds = dict()
    creds['smtp'] = 'smtp.zoho.com:587'
    creds['username'] = 'atlantic.helmet.navy@zohomail.com'
    creds['password'] = input(f'enter password: ')
    msg = dict()
    msg['subject'] = 'Test mail'
    msg['from'] = creds['username']
    msg['attachment'] = 'merged_form.pdf'
    msg['destination'] = 'ykorman@gmail.com'
    msg['body'] = u'בדיקות אחד שתים 2345 ארבעים'
    send_mail(creds, msg)
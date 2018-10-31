# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText


def send_email():
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    # fp = open(textfile, 'rb')
    # # Create a text/plain message
    # msg = MIMEText(fp.read())
    # fp.close()

    # me == the sender's email address
    # you == the recipient's email address
    me = 'rakeb.void@gmail.com'
    you = 'rakeb.void@gmail.com'
    msg = MIMEText('Hello world')
    msg['Subject'] = 'Email Mutation'
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login(me, 'uvkcqgohdtguneao')
    s.sendmail(me, [you], msg.as_string())
    s.quit()


if __name__ == '__main__':
    send_email()

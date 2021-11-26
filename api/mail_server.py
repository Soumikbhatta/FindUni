import smtplib
from api.mail_pass import *


def send_mail(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Creating a tls connection
    server.login(email_from, pass_word)
    server.sendmail(email_from, email_from, msg)  # from,To,Message
    server.quit()

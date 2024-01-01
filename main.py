
from flet import *
from email.mime.text import MIMEText
import smtplib
import random

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = "gathery@school173.com.ua"
smtp_password = "dwex ikng hkdw uoaj"



def send(login, pwd, mail):
    from_email = 'gathery@school173.com.ua'
    to_email = mail
    subject = 'Hello, world!'
    #Перейдіть за посиланням для входу на портал: http://gathery.pages.dev
    # Provide a link instead of a button with JavaScript
    msg = MIMEText(f"Вітаємо в Gathery Voting\nВаші данні для входу :\n\n\tЛогін    : {login}"
                   f"\n\tПароль : {pwd}", "plain")
    msg["Subject"] = (f"Данні для входу на голосування")

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(from_email, to_email, msg.as_string())

auth = ''
user_mail = ""
def main(page: Page):
    a = TextField(label = "Data", multiline=True)
    page.add(a)
    


app(main, view=WEB_BROWSER)

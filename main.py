import firebase_admin
from firebase_admin import credentials, db
from flet import *
from email.mime.text import MIMEText
import smtplib
import random

cred = credentials.Certificate('gathery.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://opijk-f14cd-default-rtdb.firebaseio.com/'})



smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = "gathery@school173.com.ua"
smtp_password = "dwex ikng hkdw uoaj"

def check_if_user(user):
    ref = db.reference('/users')
    users = list(ref.get().keys())
    return users

def check_if_mail():
    mails = []
    ref = db.reference('/users')
    users = list(ref.get().keys())
    for i in users:
        mails.append(ref.child(i).get()["mail"])
    return mails

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

def send_user_auth(mail):
    code = ''
    global auth
    for i in range(5):
        code += str(random.randint(0, 9))


    from_email = 'gathery@school173.com.ua'
    to_email = mail
    subject = 'Hello, world!'
    # Provide a link instead of a button with JavaScript
    msg = MIMEText(f"Вітаємо в Gathery Voting\nВаш код для підтвердження пошти :\n\t{code}",
                   "plain")
    msg["Subject"] = (f"Данні для входу на голосування")

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(from_email, to_email, msg.as_string())

    auth = code

auth = ''
user_mail = ""
def main(page: Page):

    page.theme_mode = ThemeMode.LIGHT
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 10

    def show_bs(e):
        if f"{mail.value}@school173.com.ua" in check_if_mail():
            mail.border_color = colors.RED
            mail.error_text = "Користувач з цією поштою вже зареєстрований"
            mail.focus()

            page.update()
        else:
            mail.border_color = colors.GREY
            mail.error_text = None
            page.update()

            send_user_auth(f"{mail.value}@school173.com.ua")
            global user_mail
            user_mail += f"{mail.value}@school173.com.ua"

            bs.open = True
            bs.update()

    def close_bs(e):

        if code_field.value == auth:

            bs.open = False
            bs.update()
            global user_mail

            page.clean()


            def check(a):
                if login.value in check_if_user(login.value):
                    login.border_color = colors.RED
                    login.error_text = "Користувач з цим логіном вже зареєстрований"
                    page.update()
                else:
                    login.border_color = colors.GREY
                    login.error_text = None
                    page.update()

                if "/" in login.value:
                    login.border_color = colors.RED
                    login.error_text = "Логіном не може містити '.' або '/'"
                    page.update()
                if "." in login.value:
                    login.border_color = colors.RED
                    login.error_text = "Логіном не може містити '.' або '/'"
                    page.update()

                else:
                    login.border_color = colors.GREY
                    login.error_text = None
                    page.update()
            reg = None
            def check_pwd(s):
                if pwd1.value != pwd2.value:
                    pwd1.border_color = colors.RED
                    pwd2.border_color = colors.RED

                    pwd2.error_text = "Паролі не збігаються"
                    global reg
                    reg = False
                    page.update()
                    print(reg)

                else:
                    pwd1.border_color = colors.GREY
                    pwd2.border_color = colors.GREY
                    pwd2.error_text = None
                    page.update()
                    reg = True
                    print(reg)
            def register(S):
                try:
                    if pwd1.value != pwd2.value:
                        pwd1.border_color = colors.RED
                        pwd2.border_color = colors.RED

                        pwd2.error_text = "Паролі не збігаються"

                        page.update()

                    else:
                        pwd1.border_color = colors.GREY
                        pwd2.border_color = colors.GREY
                        pwd2.error_text = None
                        page.update()

                    global user_mail
                    ref = db.reference("users/")
                    ref.child(login.value).set({
                        "login": login.value,
                        "mail": user_mail,
                        "teacher": form.value,
                        "pwd": pwd2.value

                    })
                    page.clean()

                    page.add(Text("Реєстрація пройшла успішно!", style=TextStyle(italic=True, weight=FontWeight.BOLD)))
                    page.add(Text("Посилання для входу на портал буде надісла в день голосування!"))

                    send(login.value, pwd1.value, user_mail)

                except:
                    pass


            login = TextField(label="Логін", width= 400, border=InputBorder.UNDERLINE, on_change=check)
            pwd1 = TextField(label="Пароль", password=True,can_reveal_password=True, width= 400, border = InputBorder.UNDERLINE, on_change=check_pwd)
            pwd2 = TextField(label="Повторити пароль", password=True, can_reveal_password=True, width= 400, border = InputBorder.UNDERLINE, on_change=check_pwd)
            form = Dropdown(label="Оберіть класс", options=[
                dropdown.Option("5А"),
                dropdown.Option("5Б"),
                dropdown.Option("5В"),
                dropdown.Option("5Г"),
                dropdown.Option("6А"),
                dropdown.Option("6Б"),
                dropdown.Option("6В"),
                dropdown.Option("6Г"),
                dropdown.Option("7А"),
                dropdown.Option("7Б"),
                dropdown.Option("7В"),
                dropdown.Option("7Г"),
                dropdown.Option("8А"),
                dropdown.Option("8Б"),
                dropdown.Option("8В"),
                dropdown.Option("9А"),
                dropdown.Option("9Б"),
                dropdown.Option("9В"),
                dropdown.Option("10А"),
                dropdown.Option("10Б"),
                dropdown.Option("10В"),
                dropdown.Option("11А"),
                dropdown.Option("11Б")
            ], border =InputBorder.UNDERLINE,
                width=400)
            up = FilledTonalButton("Зареєструватися", on_click = lambda _ : register(_))
            page.add(Text("Створіть обліковий запис", size=30))

            page.add(login)
            page.add(pwd1)
            page.add(pwd2)
            page.add(form)
            page.add(up)
        else:
            pass

    code_field = TextField(label = "Код", border=InputBorder.UNDERLINE, filled=True)
    bs = BottomSheet(
        Container(
            Column(
                [
                    Row([Text(f"Код було надіслано на пошту")], alignment=MainAxisAlignment.CENTER),
                    code_field,
                    ElevatedButton("Close bottom sheet", on_click=close_bs),
                ],
                tight=True,
            ),
            padding=10,
            width=300,
            height= 200
        ),
        open=True,
    )

    def check(kl):
        if f"{mail.value}@school173.com.ua" in check_if_mail():
            mail.border_color = colors.RED
            mail.error_text = "Користувач з цією поштою вже зареєстрований"
            page.update()
        else:
            mail.border_color = colors.GREY
            mail.error_text = None
            page.update()


    mail = TextField(
        label="Пошта",
        suffix_text="@school173.com.ua",
        width=400,
        helper_text="@school173.com.ua вводиться автоматично",
        border=InputBorder.UNDERLINE,
        filled=True,
        on_change=check
    )

    page.overlay.append(bs)
    bs.open = False
    page.add(Text("Gathery Voting Regestration", size=30))
    page.add(Container(height=15))
    page.add(mail)
    page.add(FilledTonalButton("Продовжити", on_click=show_bs))

app(main, view=WEB_BROWSER)
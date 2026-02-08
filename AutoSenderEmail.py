import smtplib
from email.mime.multipart import MIMEMultipart
from colorama import Fore, Style, init
from email.mime.text import MIMEText
from pyfiglet import Figlet

init()

f = Figlet(font='slant')
print(Fore.CYAN + f.renderText('SendEmail-404') + Style.RESET_ALL)


SENDER_EMAIL = "i#####@gmail.com"#your emial phishing
APP_PASSWORD = "##pppo09709##"#AppPass 
RECEIVER_EMAIL = input("emial phishin: ")
HTML_FILE = "message-E-mail-Phishin for instagram.html"


with open(HTML_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

msg = MIMEMultipart("alternative")
msg["Subject"] = "pour vous"
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL

msg.attach(MIMEText(html_content, "html"))


with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)

print("[+] message send (finish the attack ) ....")

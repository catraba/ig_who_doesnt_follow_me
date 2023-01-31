from dataclasses import dataclass
from re import search
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument("--log-level=3")


@dataclass
class InstagramScraper():
    username: str
    password: str
    
    driver = webdriver.Chrome(chrome_options=CHROME_OPTIONS)
    driver.get('https://www.instagram.com/')


    @property
    def get_XPath(self) -> dict:
        return {
            'cookies_button': """
                /html/body/div[2]/div/div/div/div[2]/div/div/div[1]
                /div/div[2]/div/div/div/div/div[2]/div/button[2]
            """,
            'login_button': """
                /html/body/div[2]/div/div/div/div[1]/div/div/div
                /div[1]/section/main/article/div[2]/div[1]/div[2]
                /form/div/div[3]/button/div
            """,
            'profile_button': """
                /html/body/div[2]/div/div/div/div[1]/div/div/div
                /div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]
                /div/div/a
            """,
            'scroller_modal_followers': """
                /html/body/div[2]/div/div/div/div[2]/div/div/div[1]
                /div/div[2]/div/div/div/div/div[2]/div/div/div[2]
            """,
            'scroller_modal_following': """
                /html/body/div[2]/div/div/div/div[2]/div/div/div[1]
                /div/div[2]/div/div/div/div/div[2]/div/div/div[3]
            """
        }
        
    
    @classmethod
    def get_last_user(self, total: int) -> dict:
        return {
            'followers': f"""
                /html/body/div[2]/div/div/div/div[2]/div/div
                /div[1]/div/div[2]/div/div/div/div/div[2]/div
                /div/div[2]/div/div/div[{str(total)}]/div[2]
                /div[1]/div/div/div/div/a/span/div
            """,
            'following': f"""
                /html/body/div[2]/div/div/div/div[2]/div/div
                /div[1]/div/div[2]/div/div/div/div/div[2]/div
                /div/div[3]/div/div/div[{str(total)}]/div[2]
                /div[1]/div/div/div/div/a/span/div
            """
        }
    

    def login(self) -> None:
        sleep(2)
        self.driver.find_element(By.XPATH, 
            self.get_XPath['cookies_button']).click()

        self.driver.find_element(By.XPATH, 
        '//input[@name="username"]').send_keys(self.username)
        self.driver.find_element(By.XPATH, 
        '//input[@name="password"]').send_keys(self.password)

        sleep(2)  
        self.driver.find_element(By.XPATH, 
            self.get_XPath['login_button']).click()


    def go_to_profile(self) -> None:
        sleep(10)
        self.driver.find_element(By.XPATH, 
            self.get_XPath['profile_button']).click()

    
    def get_follow(self, f: str) -> set:
        f_list = set()

        scroll = self.get_XPath['scroller_modal_followers'] \
            if f == 'followers' else \
            self.get_XPath['scroller_modal_following']
        
        sleep(3)
        f_total = self.driver.find_element(By.XPATH, 
            f'//a[@href="/{self.username}/{f}/?next=%2F"]')

        x_path_for_last_user = self.get_last_user(
            self.get_total_follow(f_total.text)
        )[f]

        f_total.click()

        sleep(2)
        f_scroll = self.driver.find_element(By.XPATH, scroll)
        
        while True:
            self.driver.execute_script('arguments[0].scrollTop = \
                arguments[0].scrollTop + arguments[0].offsetHeight;', 
                f_scroll)

            try:
                self.driver.find_element(By.XPATH, 
                    x_path_for_last_user)

                break

            except NoSuchElementException:
                pass


            sleep(3)


        sleep(2)
        all_a = self.driver.find_elements(By.TAG_NAME, 'a')

        for a in all_a:
            f_list.add(a.text)

        sleep(1)
        self.driver.back()

        return f_list


    def close_nav(self) -> None:
        sleep(3)
        self.driver.quit()


    @staticmethod
    def get_total_follow(text: str) -> int:
        return int(search('\d+', text).group())
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

class Web:
    def __init__(self,width,hight,data,driver_type="./chromedriver.exe"):
        self.driver_type = driver_type
        self.width = width
        self.hight = hight
        self.data = data

    def take_screenshots_of_tread(self):
        service = Service(executable_path=self.driver_type)
        driver = webdriver.Chrome(service=service)
        driver.set_window_size(self.width, self.hight)

        url_path = self.data["url"]
        driver.get(f'https://www.reddit.com{url_path}?sort=top')

        # press on all the nsfw buttons
        try:
                driver.find_element(By.CSS_SELECTOR,'[data-testid=content-gate]')
                driver.find_element(By.CSS_SELECTOR,'button[role=button]').click()
                driver.find_element(By.CSS_SELECTOR,'[data-click-id=text] button').click()
        except:
            pass


        # hide bar
        driver.execute_script('document.getElementsByClassName("subredditvars-r-askreddit")[0].setAttribute("hidden","");') 

        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # create folder
        folder_name = url_path.replace("/", "-" )
        save_path = f'thread/{folder_name}/screenshots'
        if(not os.path.exists(save_path)):
            os.makedirs(save_path)
        
        time.sleep(SCROLL_PAUSE_TIME)

        # take screenshot of title
        title_element = driver.find_element(By.CSS_SELECTOR,'[data-testid=post-container]')
        title_element.screenshot(f'./{save_path}/title.png')

        # take screenshots of comments
        for count,comment in enumerate(self.data["comments"]):
            try:
                element = driver.find_element(By.ID,comment["id"])
                element.screenshot(f'./{save_path}/comment{count}.png')
            except:
                print(":(")

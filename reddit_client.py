from cmath import log
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from array import array
from turtle import pos
import requests
import json
import time
import os
from better_profanity import profanity

class RedditClient:
    def __init__(self, username, password, app_id, secret,count = 0):
        self.username = username
        self.password = password
        self.app_id = app_id
        self.secret = secret
        self.get_token()
        self.count = count

    def get_token(self):
        auth = requests.auth.HTTPBasicAuth(self.app_id, self.secret)

        data = {'grant_type': 'password',
                'username': self.username,
                'password': self.password}
        headers = {'User-Agent': 'MyBot/0.0.1'}

        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)

        self.TOKEN = res.json()['access_token']

        # headers = {**headers, **{'Authorization': f"bearer {self.TOKEN}"}}

        # r = requests.get(
        #     'https://oauth.reddit.com/r/AskReddit/', headers=headers)

    def get_subreddit_posts(self, subreddit):
        headers = {'User-Agent': 'MyBot/0.0.1',
                   'Authorization': f"bearer {self.TOKEN}",
                   't': 'day',
                   'limit': '100',
                   'count' : '25'}

        threads = requests.get(
            f"https://oauth.reddit.com/r/{subreddit}/top", headers=headers)

        output_json_to_json_file("",threads.json(),"subreddit_posts")

        return threads.json()

    def get_post_comments(self, url):
        headers = {'User-Agent': 'MyBot/0.0.1',
                   'Authorization': f"bearer {self.TOKEN}",
                   'sort': 'top'}

        comments = requests.get(
            f"https://oauth.reddit.com{url}", headers=headers)


        output_json_to_json_file(url,comments.json(),"comments")

        return comments.json()

    

    def get_new_topic(self,subreddit):
        return_json = {}
        # get list of all topics
        posts = self.get_subreddit_posts(subreddit)


        save_path = f'thread/'
        if(not os.path.exists(save_path)):
            os.makedirs(save_path)
        
        file = open("thread/used.txt", "a")
        file.close()
        file = open("thread/used.txt", "r")
        used_urls = file.read()
        file.close()

        return_json["url"] = ''
        return_json["topic_string"] = ''
        for post in posts['data']['children']:
            if(post['data']['permalink'] not in used_urls):
                return_json["topic_string"] = profanity.censor(post['data']['title'])
                return_json["url"] = post['data']['permalink']
                break

        # get comments
        comments = self.get_post_comments(return_json["url"])
        return_json["comments"] = []
        for count, comment in enumerate(comments[1]['data']['children']):
            if(comment['kind']=='t1'):
                return_json["comments"].append({
                    "text" : profanity.censor(comment['data']['body']),
                    "id" : comment['data']['name']
                })


        # add to used list
        if(not os.path.exists("thread/")):
            os.makedirs("thread/")
        file = open("thread/used.txt", "a")
        file.write(f'\n{return_json["url"]}')
        file.close

        output_json_to_json_file(return_json["url"],return_json,"data")
        return return_json
    
    def test_take_screensots(self,url,comments_id_arr):
        service = Service(executable_path="chromedriver")
        driver = webdriver.Chrome(service=service)
        driver.set_window_size(414, 896)

        driver.get(f"https://www.reddit.com{url}?sort=top")

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

        driver.find_element(By.CSS_SELECTOR,'[data-testid=post-container]').screenshot('./test2/image.png')

        for count,id in enumerate(comments_id_arr):
            ele = driver.find_element(By.ID,id).screenshot(f'./test2/image{count}.png')

def output_json_to_json_file(url,json_object,filename):
    folder_name = url.replace("/", "-" )
    save_path = f'thread/{folder_name}'
    if(not os.path.exists(save_path)):
        os.makedirs(save_path)
    file = open(f'{save_path}/{filename}.json', "w",encoding='utf-8')
    file.write(json.dumps(json_object))
    file.close()
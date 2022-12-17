from importlib.resources import path
from pathlib import Path
from time import sleep
from reddit_client import RedditClient
from video import Video
from web import Web
import audio
import json
# import youtube
from bot_studio import *

app_id = 'reddit app id'
secret = 'reddit app id_secret'
username = 'reddit username'
password = 'reddit password'


def upload(data):
    youtube=bot_studio.youtube()
    false=False;true=True
    # inside of this you put a cookie of the utube account
    cookie_list=[
]

    folder_name = data["url"].replace("/", "-" )
    title = f'{data["topic_string"]}'
    title = title[0:(100 - 27)]
    path = f'thread/{folder_name}/final.mp4'
    abs_path = os.path.abspath(path)

    youtube.login_cookie(cookies=cookie_list)
    response=youtube.upload(title=f'{title} #askreddit #reddit #shorts', video_path=abs_path,kid_type="Yes, it's made for kids", description='thanks for watching', type="Public")
    # body=response['body']
    # video_link=body['VideoLink']


if __name__ == "__main__":
    while True:
        client = RedditClient(username,password,app_id,secret)
        data = client.get_new_topic("askreddit")
        web = Web(375, 667, data)
        web.take_screenshots_of_tread()

        audio.create_audio_files_from_data(data)

        folder_name = data["url"].replace("/", "-" )
        v = Video(f'thread/{folder_name}/',"v1.mp4",30)

        v.create_video()


        # file = open("C:/Users/Daniel/Desktop/Idk reddit shit or somthing/thread/-r-AskReddit-comments-xtrf1b-you_get_100_million_dollars_but_you_must_make_one-/data.json", "r")
        # a = file.read()
        # file.close

        # data = json.loads(a)
        try:
            upload(data)
        except:
            print(":(")
        sleep(3000)
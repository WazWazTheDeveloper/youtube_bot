import pyttsx3
import os
from gtts import gTTS


def convert_text_to_voice(text,path,file_name):
    engine = pyttsx3.init()
    engine.save_to_file(text,f'{path}/{file_name}.mp3')
    engine.runAndWait()

def create_audio_files_from_data(data):
    folder_name = data["url"].replace("/", "-" )
    path = f'thread/{folder_name}/audio/'
    if(not os.path.exists(path)):
        os.makedirs(path)
    convert_text_to_voice(data["topic_string"],path,'title')
    for i,comment in enumerate(data["comments"]):
        convert_text_to_voice(comment["text"],path,f'comment{i}')
from asyncio.windows_events import NULL
import math
import random
from moviepy.editor import *


delay_duration = 0.5

class Video:
    def __init__(self,directory,background_video_path,max_duration,video_width=1080,video_hight=1920):
        self.directory=directory
        self.video_size = (video_width,video_hight)
        self.total_duration = 0
        self.final_clip = None
        self.max_duration = max_duration
        self.total_duration = 0
        self.video_stack = []
        self.background_video_path = background_video_path
        self.duration_counter = 0

    def create_video_section(self,photo_dir,audio_dir):
        # get assets
        audio = AudioFileClip(audio_dir)
        photo = ImageClip(photo_dir)

        # resize photo to fir
        photo_size = photo.size
        resize_ratio = self.video_size[0] * 0.9 / photo_size[0]
        new_photo_size = (photo_size[0] * resize_ratio, photo_size[1] * resize_ratio)
        photo = photo.resize(new_photo_size)

        # create blank video
        blank_clip = create_color_clip(self.video_size, audio.duration + delay_duration)

        # combine videos
        final_clip = CompositeVideoClip([photo.set_position("center")]).set_duration(blank_clip.duration)
        final_clip.audio = audio


        self.add_to_video_stack(final_clip)

    def add_to_video_stack(self,clip):
        self.video_stack.append(clip)
        self.total_duration += clip.duration

    def add_to_final_video(self,clip):
        if(self.final_clip == None):
            self.final_clip = clip
        else:
            clip = clip.set_start(self.duration_counter)
            self.duration_counter += clip.duration
            self.final_clip = CompositeVideoClip([self.final_clip,clip.set_position("center")]).set_duration(self.final_clip.duration)

    def create_video(self):
        # title
        title_dir = f'{self.directory}screenshots/title.png'
        audio_dir = f'{self.directory}audio/title.mp3'
        self.create_video_section(title_dir,audio_dir)

        # comments
        comment_counter = 0
        while (self.total_duration < self.max_duration):
            title_dir = f'{self.directory}screenshots/comment{comment_counter}.png'
            audio_dir = f'{self.directory}audio/comment{comment_counter}.mp3'
            self.create_video_section(title_dir,audio_dir)

            comment_counter += 1

        # create video with proper length
        background_video = VideoFileClip(self.background_video_path)
        background_video_start_time = random.randrange(0,math.floor(background_video.duration - self.total_duration))
        background_video = background_video.subclip(background_video_start_time,background_video_start_time + self.total_duration)

        # crop hight
        background_video_size = background_video.size
        resize_ratio = self.video_size[1] / background_video_size[1]
        new_background_video_size = (background_video_size[0] * resize_ratio, background_video_size[1] * resize_ratio)
        background_video = background_video.resize(new_background_video_size)

        # crop width
        background_video_size = background_video.size
        x_start = (background_video_size[0] - self.video_size[0]) / 2
        x_end = background_video_size[0] - ((background_video_size[0] - self.video_size[0]) / 2)

        background_video = background_video.crop(x1=x_start,y1=0,x2=x_end,y2=background_video_size[1])

        self.add_to_final_video(background_video)
        for video in self.video_stack:
            self.add_to_final_video(video)

        self.render_video()


    def render_video(self):
        self.final_clip.write_videofile(
        f'{self.directory}/final.mp4',
        fps=25,
        threads=20,
        bitrate="2000k",
        audio_codec="aac",
        codec="h264_nvenc",)



def create_color_clip(size, duration, color=(100,100,100)):
    return ColorClip(size, color, duration=duration)
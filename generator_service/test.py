import numpy as np
import moviepy.editor as mpy
import re
from sre_compile import isstring
import exifread
import requests
import os
import cv2
from PIL import Image,ImageDraw, ImageFont
import json
from shutil import copyfile
from sys import exit
import demjson
import shutil
import json
class JsonHandle():
    file_path = ""
    context = None
    __file_handle = None
    def __init__(self,path):
        self.file_path = path
    def open(self):
        self.__file_handle = open(self.file_path,mode='r',encoding='utf-8')
        text = self.__file_handle.read()
        self.context = json.loads(text)
        self.__file_handle.close()
        self.__file_handle = None
    def save(self):
        if self.context:
            self.__file_handle=open(self.file_path,mode='w',encoding='utf-8')
            json.dump(self.context,self.__file_handle,ensure_ascii=False,indent=4)
            self.__file_handle.close()
            self.__file_handle=None
 
    def __del__(self):
        if self.__file_handle:
            self.__file_handle.close()
 
    def __repr__(self):
        if self.context:
            text = json.dumps(self.context,ensure_ascii=False,indent=4)
            return text
        return ""
rotMatrix = lambda a: np.array( [[np.cos(a),np.sin(a)],  [-np.sin(a),np.cos(a)]] )
def vortex(screenpos, i, nletters):   
    d = lambda t: 1.0 / (0.3 + t ** 8)  # damping
    a = i * np.pi / nletters  # angle of the movement
    v = rotMatrix(a).dot([-1, 0])
    if i % 2: v[1] = -v[1]
    return lambda t: screenpos + 400 * d(t) * rotMatrix(0.5 * d(t) * a).dot(v)

def cascade(screenpos, i, nletters):   
    v = np.array([0, -1])
    d = lambda t: 1 if t < 0 else abs(np.sinc(t) / (1 + t ** 4))
    return lambda t: screenpos + v * 400 * d(t - 0.15 * i)

def arrive(screenpos, i, nletters):    
    v = np.array([-1, 0])
    d = lambda t: max(0, 3 - 3 * t)
    return lambda t: screenpos - 400 * v * d(t - 0.2 * i)

def vortexout(screenpos, i, nletters):    
    d = lambda t: max(0, t)  # damping
    a = i * np.pi / nletters  # angle of the movement
    v = rotMatrix(a).dot([-1, 0])
    if i % 2: v[1] = -v[1]
    return lambda t: screenpos + 400 * d(t - 0.1 * i) * rotMatrix(-0.2 * d(t) * a).dot(v)
def txtanimation(screensize,lettersize,text,func,offsetx,offsety):
    screenw=screensize[0]    #屏幕宽度
    screenh=screensize[1]    #屏幕高度
    letterw=lettersize[0]    #单个字符宽度
    letterh=lettersize[1]    #单个字符高度
    letternum=len(text)    #字符数量
    letteronex=(screenw-letterw*letternum)/2+offsetx    #首个字符在屏幕中的x坐标
    letteroney=(screenh-letterh)/2+offsety    #首个字符在屏幕中的y坐标
    tclips = []    #剪辑列表
    for i in range(letternum):
        tclip = mpy.TextClip(text[i], color='white', font='KaiTi', kerning=5, fontsize=70, size=lettersize)    #创建单个字符文本剪辑
        tclip = tclip.set_pos((letteronex + i * letterw, letteroney))  # 设置单个字符文本剪辑在屏幕中的初始位置
        tclip = tclip.set_pos(func(tclip.pos(0), i, letternum))  # 调用文字特效函数
        tclips.append(tclip)    #添加到剪辑列表
    return tclips
screensize=(1920,1080)
lettersize=(80,80)
import json
import os
Json_path = '/Users/xupeiying/Documents/Code/Big_Projects/Python/generator_service/Json_bank'
file_count = len(os.listdir(Json_path))
clip_list = []
print("file_count",file_count)
for k in range(1,file_count-1):
    file_name = Json_path + '/' + str(k) + '.json'
    print('正在读取数据：',file_name)
    jsonHandle = JsonHandle(file_name)
    jsonHandle.open()
    Comment = jsonHandle.context["comment"]
    print(Comment)
    text = list(Comment)
    print(text)
    clip1=mpy.CompositeVideoClip(txtanimation(screensize,lettersize,text,cascade,0,-100),size=screensize).subclip(0,5)
    clip2=mpy.CompositeVideoClip(txtanimation(screensize,lettersize,text,vortexout,0,-100),size=screensize).subclip(0,3)
    print('正在添加图片：','./resize_scenery/{}.jpg'.format(k))
    iclip=mpy.ImageClip('./resize_scenery/{}.jpg'.format(k)).set_duration(8)
    clip=mpy.CompositeVideoClip([iclip,clip1.fadeout(2),clip2.set_start(5).fadein(1)])
    clip_list.append(clip)
    # clip.write_videofile('test.mp4',fps=24)

print("进行内存视频拼接...")
destClip = mpy.concatenate_videoclips(clip_list)
print("内存视频拼接完成，准备输出到文件.")
destClip.write_videofile('video.mp4',fps=24)
def get_video_time(filename):
  cap = cv2.VideoCapture(filename)
  if cap.isOpened():
    rate = cap.get(5)
    frame_num =cap.get(7)
    duration = frame_num/rate
    return duration
  return -1

t = get_video_time('./video.mp4')
print(t)
audio_background = mpy.AudioFileClip('wind.mp3').subclip(0, t)
audio_background.write_audiofile('bgm.mp3')
def add_music():
    # 读取代码视频
    my_clip = mpy.VideoFileClip('video.mp4')
    # 截取背景音乐
    audio_background = mpy.AudioFileClip('bgm.mp3')
    # 视频中插入音频
    final_clip = my_clip.set_audio(audio_background)
    # 保存最终视频
    final_clip.write_videofile('result.mp4')
result = add_music()
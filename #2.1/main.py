import telebot
import time

from PIL import Image
import requests
from io import BytesIO


def download_file(url, name="video.mp4"):
    r = requests.get(url, stream=True)
    with open(name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


TOKEN = "Your Token"
# This is my image link
IMAGE_LINK = "https://cdn.pixabay.com/photo/2016/01/08/11/49/text-1127657_1280.jpg"
VIDEO_LINK = "https://vod-progressive.akamaized.net/exp=1605568547~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F3260%2F17%2F441301097%2F1930591083.mp4~hmac=cef853112cef465d36e79e0563198af65d01a6bee1aa794c613c2fb84ccdb3fa/vimeo-prod-skyfire-std-us/01/3260/17/441301097/1930591083.mp4?filename=Creux+De+Van+-+45150.mp4"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    print(message.text)


@bot.message_handler(commands=["hello", "hi"])
def hello(message):
    bot.send_message(message.chat.id, "Hello World")


@bot.message_handler(commands=["image", "img"])
def image(message):
    img = open("hello.jpg", "rb")
    bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=["imagenet", "imgnet"])
def imagenet(message):
    response = requests.get(IMAGE_LINK)
    imgnet = Image.open(BytesIO(response.content))
    # Send the photo
    bot.send_photo(message.chat.id, imgnet)


@bot.message_handler(commands=["video", "vid"])
def video(message):
    vid = open("video.mp4", "rb")
    bot.send_video(message.chat.id, vid)


@bot.message_handler(commands=["videonet", "vidnet"])
def videonet(message):
    download_file(VIDEO_LINK, "myvideo.mp4")
    vidnet = open("myvideo.mp4", "rb")
    bot.send_video(message.chat.id, vidnet)


while True:
    try:
        bot.polling()
    except:
        time.sleep(5)

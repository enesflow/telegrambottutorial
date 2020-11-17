# You do not need to install these. These modules are built in
import random  # Built in
import time  # Built in
from io import BytesIO  # Built in

import praw  # pip install praw
import telebot  # pip install pytelegrambotapi
from PIL import Image  # pip install Pillow
import requests  # pip install requests

TOKEN = "1457645096:AAEfJtg6gmFLuzw8bNEPHipLznSM9MUxcLQ"
bot = telebot.TeleBot(TOKEN)
reddit = praw.Reddit(client_id="",
                     client_secret="",
                     username="",
                     password="",  
                     user_agent="this is useless")


def get_post(rddt, sbrddt, first_x_posts=100):
    subreddit = rddt.subreddit(sbrddt)  # Get the subreddit
    hot = subreddit.hot(limit=first_x_posts)  # Get the first 100 posts
    post = random.choice(list(hot))  # Get a random post from them
    return post


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello")


@bot.message_handler(commands=["reddit", "r"])
def send_post(message):
    # This will get the first 100 posts and return one of them
    post = get_post(rddt=reddit, sbrddt="askreddit")
    try:
        response = requests.get(post.url)
        img = Image.open(BytesIO(response.content))
        # We got the image
        # Let's send it
        bot.send_photo(message.chat.id, img, caption=post.title)
    except Exception as e:
        # You can copy this from the descrition
        if "cannot identify image file <_io.BytesIO object at" in str(e):
            bot.send_message(message.chat.id, f"{post.url}\n{post.title}")


while True:
    try:
        bot.polling()
    except:
        time.sleep(5)

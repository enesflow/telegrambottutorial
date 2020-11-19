# You do not need to install these. These modules are built in
import random  # Built in
import time  # Built in
from io import BytesIO  # Built in
from threading import Thread

import praw  # pip install praw
import telebot  # pip install pytelegrambotapi
from PIL import Image  # pip install Pillow
import requests  # pip install requests

TOKEN = "Your Bot's Token"
bot = telebot.TeleBot(TOKEN)
reddit = praw.Reddit(client_id="HWx6IOXHME18RQ",
                     client_secret="0JLmRdAULEnQNX0LkuXpB1Mi_gXuTw",
                     username="colorfl",
                     password="imnotabanana",  # awesome password
                     user_agent="this is useless")

users = []
mysubreddit = "memes"


def get_post(rddt, sbrddt, first_x_posts=100):
    subreddit = rddt.subreddit(sbrddt)  # Get the subreddit
    hot = subreddit.hot(limit=first_x_posts)  # Get the first 100 posts
    post = random.choice(list(hot))  # Get a random post from them
    return post


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello")

# Join


@bot.message_handler(commands=["join", "j"])
def start(message):
    # Check if the user already exists
    if message.chat.id in users:
        bot.send_message(message.chat.id, "You are already joined")
    # If not
    else:
        users.append(message.chat.id)
        bot.send_message(message.chat.id, "You successfully joined")

# Leave


@bot.message_handler(commands=["leave", "l"])
def start(message):
    # Check if the user exists
    if message.chat.id in users:
        users.remove(message.chat.id)
        bot.send_message(message.chat.id, "You successfully leaved")
    # If not
    else:
        bot.send_message(message.chat.id, "You are not even joined")


@bot.message_handler(commands=["reddit", "r"])
def send_post(message):
    # This will get the first 100 posts and return one of them
    post = get_post(rddt=reddit, sbrddt=mysubreddit)
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


def send_posts():
    time.sleep(10)
    while True:
        for user in users:
            # This will get the first 100 posts and return one of them
            post = get_post(rddt=reddit, sbrddt=mysubreddit)
            try:
                response = requests.get(post.url)
                img = Image.open(BytesIO(response.content))
                # We got the image
                # Let's send it
                bot.send_photo(user, img, caption=post.title)
            except Exception as e:
                # You can copy this from the descrition
                if "cannot identify image file <_io.BytesIO object at" in str(e):
                    bot.send_message(user, f"{post.url}\n{post.title}")

        # Every 1 hour
        time.sleep(60*60)  # Time in seconds


def main():
    while True:
        try:
            bot.polling()
        except:
            time.sleep(5)


# Run the main() function
Thread(target=main).start()
# Run the send_posts() function
Thread(target=send_posts).start()

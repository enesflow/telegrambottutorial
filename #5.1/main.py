import telebot
from telebot import types
import time

TOKEN = "Your Bot's Token"
bot = telebot.TeleBot(TOKEN)


@bot.inline_handler(lambda query: query.query == 'test')
def test(inline_query):
    r = types.InlineQueryResultArticle(
        # The id of our inline result
        id='1',
        title='test',
        input_message_content=types.InputTextMessageContent(
            'I am a message'
        )
    )
    bot.answer_inline_query(inline_query.id, [r])


@bot.inline_handler(lambda query: query.query == 'image')
def image(inline_query):
    r = types.InlineQueryResultPhoto(
        id='11',
        photo_url='https://images.assettype.com/swarajya/2020-08/a46bd36a-e65b-4b0b-91d9-c0fcac98c518/telegram.jpg?w=1200&h=800',
        thumb_url='https://images.assettype.com/swarajya/2020-08/a46bd36a-e65b-4b0b-91d9-c0fcac98c518/telegram.jpg?w=1200&h=800'
    )

    bot.answer_inline_query(inline_query.id, [r])


while True:
    try:
        bot.polling(True)
    except Exception as e:
        print(e)
        time.sleep(5)

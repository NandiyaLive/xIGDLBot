#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
# Coded with ❤️ by Neranjana Prasad (@NandiyaLive)

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
import requests
from bs4 import BeautifulSoup as bs
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
# from instaloader import Instaloader, Profile, Post
import sys
import shutil
import glob
import os
import zipfile
import pathlib

bot_token = os.environ.get("BOT_TOKEN", "")
bot = Bot(token=bot_token)

help_keyboard = [[InlineKeyboardButton("Updates Channel", url="https://t.me/MBNUpdates"),
                  InlineKeyboardButton("Support Chat", url="https://t.me/MBNChat")]]
help_reply_markup = InlineKeyboardMarkup(help_keyboard)


def start(update, context):
    user = update.message.from_user
    chat_member = context.bot.get_chat_member(
        chat_id='-1001225141087', user_id=update.message.chat_id)
    status = chat_member["status"]
    if(status == 'left'):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"Hi {user.first_name}, to use me you have to be a member of the updates channel in order to stay updated with the latest developments.\nPlease click below button to join and /start the bot again.", reply_markup=help_reply_markup)
        return
    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"Hi {user.first_name}!\nI'm Instagram Media Downloader Bot. I can help you to download Stories and IGTV Videos from any public instagram account.\nPlease read the /help before using me.", parse_mode=telegram.ParseMode.HTML, reply_markup=help_reply_markup)


def help(update, context):
    keyboard = [[InlineKeyboardButton("Updates Channel", url="https://t.me/MBNUpdates"),
                 InlineKeyboardButton("Support Chat", url="https://t.me/MBNChat")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('''<b>Usage:</b>\n/stories username - Download stories from the username’s profile.\n/igtv username - Download IGTV videos from the username’s profile.\n/feed username - Download all posts from the username’s profile as a zip file.\n\n<b>How to find the username?</b>\nOpen Instagram app & then go to a profile that you want to download items. Username must be on the top.\nIn case you are using a browser you can find it in the Address bar.\n<b>Example : </b>Username for instagram.com/rashmika_mandanna & @rashmika_mandanna is 'rashmika_mandanna' 😉''', parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)


def about(update, context):
    keyboard = [[InlineKeyboardButton(
        "Source Code", url="https://github.com/NandiyaLive/xIGDLBot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='''I can help you to download media from any public instagram account without leaving Telegram.\n\nMade with ❤️ + python-telegram-bot by @NandiyaLive''', parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)


def echo(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, text='''Please read /help''')


def stories(update, context):
    user = context.bot.get_chat_member(
        chat_id='-1001225141087', user_id=update.message.chat_id)
    status = user["status"]
    if(status == 'left'):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="To use to bot you need to be a member of @MBNUpdates in order to stay updated with the latest developments.")
        return
    else:
        status_page = "https://www.insta-stories.com/en/status"

        req_status = requests.get(status_page).text
        status = bs(req_status, "lxml")

        if status.find("div", class_="status status--ok"):
            fullmsg = update.message.text

            if fullmsg == "/stories":
                update.message.reply_text(
                    '/stories [instagram username]\nPlease read /help')
            else:
                msg = fullmsg.replace("/stories ", "")

                if "@" in msg.lower():
                    query = msg.replace("@", "")
                else:
                    query = msg

                url = f"https://www.insta-stories.com/en/stories/{query}"
                r = requests.get(url).text

                soup = bs(r, "lxml")

                if soup.find("div", class_="msg msg-user-not-found"):
                    update.message.reply_text(
                        "This username doesn't exist. Please try with another one.")

                elif soup.find("div", class_="error"):
                    update.message.reply_text(
                        "API Error 🤒\nPlease try again later.")

                else:
                    if soup.find("div", class_="msg msg-no-stories"):
                        update.message.reply_text(
                            "No stories available. Please try again later.")

                    else:
                        try:
                            profile = soup.find("div", class_="user-name").text
                            update.message.reply_text(
                                f"Downloading stories of {profile}")

                            videos = soup.findAll(class_='story-video')
                            photos = soup.findAll(class_='story-image')

                            for video in videos:
                                src = video.find("source")['src']
                                context.bot.send_video(
                                    chat_id=update.message.chat_id, video=f"https://www.insta-stories.com{src}")

                            for photo in photos:
                                context.bot.send_photo(
                                    chat_id=update.message.chat_id, photo=f"https://www.insta-stories.com{photo['src']}")

                            bot.send_message(
                                text="Thanks for using @xIGDLBot\nPlease /donate to keep this service alive!", chat_id=update.message.chat_id)

                        except:
                            context.bot.send_message(chat_id=update.message.chat_id,
                                                     text="Something went wrong. Please try again later.", parse_mode=telegram.ParseMode.HTML)

        else:
            update.message.reply_text(
                "API is not working. Please try again later.")


# def igtv(update, context):
#     user = context.bot.get_chat_member(
#         chat_id='-1001225141087', user_id=update.message.chat_id)
#     status = user["status"]
#     if(status == 'left'):
#         context.bot.send_message(chat_id=update.message.chat_id,
#                                  text="To use to bot you need to be a member of @MBNUpdates in order to stay updated with the latest developments.")
#         return
#     else:
#         fullmsg = update.message.text

#         if fullmsg == "/igtv":
#             update.message.reply_text(
#                 '/igtv [instagram username]\nPlease read /help')
#         else:
#             msg = fullmsg.replace("/igtv ", "")

#             if "@" in msg.lower():
#                 query = msg.replace("@", "")
#             else:
#                 query = msg

#         L = Instaloader(dirname_pattern=query, download_comments=False,
#                         download_video_thumbnails=False, save_metadata=False, download_geotags=True, compress_json=True, post_metadata_txt_pattern=None, storyitem_metadata_txt_pattern=None)

#         profile = Profile.from_username(L.context, query)

#         igtv_count = profile.igtvcount

#         posts = profile.get_igtv_posts()

#         update.message.reply_text("Cooking your request 👨‍🍳\nProfile : " + query + "\nIGTV Video Count : " + str(
#             igtv_count) + "\nThis may take longer, take a nap I can handle this without you.")

#         try:
#             L.posts_download_loop(posts, query)
#         except Exception as e:
#             context.bot.send_message(chat_id=update.message.chat_id, text="<b>ERROR</b>\n"+str(
#                 e), parse_mode=telegram.ParseMode.HTML)
#             return

#         src_dir = query

#         for vidfile in glob.iglob(os.path.join(src_dir, "*.mp4")):
#             context.bot.send_video(
#                 chat_id=update.message.chat_id, video=open(vidfile, 'rb'))

#         bot.send_message(
#             text="Thanks for using @xIGDLBot\nPlease /donate to keep this service alive!", chat_id=update.message.chat_id)

#         try:
#             shutil.rmtree(query)
#         except Exception:
#             pass


def feed(update, context):
    bot.send_message(chat_id=update.message.chat_id,
                     text="This feature is still under development. Please use @MBNBetaBot if you like to beta test this feature.")

    # user = context.bot.get_chat_member(chat_id='-1001225141087', user_id=update.message.chat_id)
    # status = user["status"]
    # if(status == 'left'):
    #     context.bot.send_message(chat_id=update.message.chat_id,text="To use to bot you need to be a member of @MBNUpdates in order to stay updated with the latest developments.")
    #     return
    # else :
    #     fullmsg = update.message.text

    #     if fullmsg == "/feed":
    #         update.message.reply_text(
    #             '/feed [instagram username]\nPlease read /help')
    #     else:
    #         msg = fullmsg.replace("/feed ", "")

    #         if "@" in msg.lower():
    #             query = msg.replace("@", "")
    #         else:
    #             query = msg

    #     L = Instaloader(dirname_pattern=query, download_comments=False,
    #                     download_video_thumbnails=False, save_metadata=False, download_geotags=True, compress_json=True, post_metadata_txt_pattern=None, storyitem_metadata_txt_pattern=None)
    #     profile = Profile.from_username(L.context, query)

    #     media = profile.mediacount
    #     update.message.reply_text("Cooking your request 👨‍🍳\nProfile : " + query + "\nMedia Count : " + str(media) +
    #                             "\nThis may take longer, take a nap I can handle this without you.")

    #     posts = profile.get_posts()
    #     try:
    #         L.posts_download_loop(posts, query)
    #     except Exception as e:
    #         context.bot.send_message(chat_id=update.message.chat_id, text="<b>ERROR\n"+str(
    #             e), parse_mode=telegram.ParseMode.HTML)
    #         return

    #     update.message.reply_text("Download Completed.\n🗄 Archiving files...")

    #     zf = zipfile.ZipFile(f"{query}.zip", "w")
    #     for dirname, subdirs, files in os.walk(query):
    #         zf.write(query)
    #         for filename in files:
    #             zf.write(os.path.join(dirname, filename))
    #     zf.close()

    #     update.message.reply_text("Uploading to Telegram...")

    #     for zip_file in glob.glob("*.zip"):
    #         context.bot.send_document(chat_id=update.message.chat_id,
    #                                 document=open(zip_file, 'rb'))

    #     try:
    #         shutil.rmtree(query)
    #         os.remove(f"{query}.zip")
    #     except Exception:
    #         pass


def donate(update, context):
    user = update.message.from_user
    bot.send_message(chat_id=update.message.chat_id,
                     text=f"Hey {user.first_name}! \nThanks for showing interest in my works\nPlease contact @NandiyaLive for more info. You can send any amount you wish to donate me.")


def main():
    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start, run_async=True))
    dp.add_handler(CommandHandler("help", help, run_async=True))
    dp.add_handler(CommandHandler("stories", stories, run_async=True))
    dp.add_handler(CommandHandler("about", about, run_async=True))
#     dp.add_handler(CommandHandler("igtv", igtv, run_async=True))
    dp.add_handler(CommandHandler("feed", feed, run_async=True))
    dp.add_handler(CommandHandler("donate", donate, run_async=True))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

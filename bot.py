#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
# Coded with ❤️ by Neranjana Prasad (@NandiyaLive)

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
import requests
from bs4 import BeautifulSoup as bs
from telegram import Bot
from instaloader import Instaloader, Profile, Post
import sys
import shutil
import glob
import os
import zipfile
import pathlib

bot_token = ""
bot = Bot(token=bot_token)


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Instagram Media Downloader Bot.\nPlease join @NandiyaThings & the Support Chat.", parse_mode=telegram.ParseMode.HTML)


def help(update, context):
    update.message.reply_text('''/stories username - Download stories from the username’s profile.\n/igtv username - Download IGTV videos from the username’s profile.\n\n<b>How to find the username?</b>\nOpen Instagram app & then go to a profile that you want to download items. Username must be on the top.\nIn case you are using a browser you can find it in the Address bar.\n<b>Example : </b>Username for instagram.com/rashmika_mandanna & @rashmika_mandanna is 'rashmika_mandanna' 😉''', parse_mode=telegram.ParseMode.HTML)


def about(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='''This bot can help you to download media from Instagram without leaving Telegram.\nMade with ❤️ + python-telegram-bot\nSource Code : <a href="https://github.com/NandiyaLive/xIGDLBot">GitHub</a>''', parse_mode=telegram.ParseMode.HTML)


def echo(update, context):
    update.message.reply_text('Please read /help')


def stories(update, context):
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
                            context.bot.send_video(
                                chat_id=update.message.chat_id, video=video['src'])

                        for photo in photos:
                            context.bot.send_photo(
                                chat_id=update.message.chat_id, photo=photo['src'])
                    except:
                        context.bot.send_message(chat_id=update.message.chat_id,
                                                 text="Something went wrong. Please try again later.", parse_mode=telegram.ParseMode.HTML)

    else:
        update.message.reply_text(
            "API is not working. Please try again later.")


def igtv(update, context):
    fullmsg = update.message.text

    if fullmsg == "/igtv":
        update.message.reply_text(
            '/igtv [instagram username]\nPlease read /help')
    else:
        msg = fullmsg.replace("/igtv ", "")

        if "@" in msg.lower():
            query = msg.replace("@", "")
        else:
            query = msg

    L = Instaloader(dirname_pattern=query, download_comments=False,
                    download_video_thumbnails=False, save_metadata=False, download_geotags=True, compress_json=True, post_metadata_txt_pattern=None, storyitem_metadata_txt_pattern=None)

    profile = Profile.from_username(L.context, query)

    igtv_count = profile.igtvcount

    posts = profile.get_igtv_posts()

    update.message.reply_text("Cooking your request 👨‍🍳\nProfile : " + query + "\nIGTV Video Count : " + str(igtv_count) +
                              "\nThis may take longer, take a nap I can handle this without you.")

    try:
        L.posts_download_loop(posts, query)
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text="<b>ERROR ò_ô</b>\n"+str(
            e), parse_mode=telegram.ParseMode.HTML)
        return

    src_dir = query

    for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
        context.bot.send_photo(
            chat_id=update.message.chat_id, photo=open(jpgfile, 'rb'))

    for vidfile in glob.iglob(os.path.join(src_dir, "*.mp4")):
        context.bot.send_video(
            chat_id=update.message.chat_id, video=open(vidfile, 'rb'))

    try:
        shutil.rmtree(query)
    except Exception:
        pass


def feed(update, context):
    fullmsg = update.message.text

    if fullmsg == "/feed":
        update.message.reply_text(
            '/feed [instagram username]\nPlease read /help')
    else:
        msg = fullmsg.replace("/feed ", "")

        if "@" in msg.lower():
            query = msg.replace("@", "")
        else:
            query = msg

    L = Instaloader(dirname_pattern=query, download_comments=False,
                    download_video_thumbnails=False, save_metadata=False, download_geotags=True, compress_json=True, post_metadata_txt_pattern=None, storyitem_metadata_txt_pattern=None)
    profile = Profile.from_username(L.context, query)

    media = profile.mediacount
    update.message.reply_text("Cooking your request 👨‍🍳\nProfile : " + query + "\nMedia Count : " + str(media) +
                              "\nThis may take longer, take a nap I can handle this without you.")

    posts = profile.get_posts()
    try:
        L.posts_download_loop(posts, query)
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text="<b>ERROR\n"+str(
            e), parse_mode=telegram.ParseMode.HTML)
        return

    update.message.reply_text("Download Completed.\n🗄 Archiving files...")

    zf = zipfile.ZipFile("images.zip", "w")
    for dirname, subdirs, files in os.walk(query):
        zf.write(query)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

    update.message.reply_text("Uploading to Telegram...")

    context.bot.send_document(chat_id=update.message.chat_id,
                              document=open(f"{query}.zip", 'rb'))

    try:
        shutil.rmtree(query)
        os.remove(f"{query}.zip")
    except Exception:
        pass


def main():
    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start, run_async=True))
    dp.add_handler(CommandHandler("help", help, run_async=True))
    dp.add_handler(CommandHandler("stories", stories, run_async=True))
    dp.add_handler(CommandHandler("about", about, run_async=True))
    dp.add_handler(CommandHandler("igtv", igtv, run_async=True))
    dp.add_handler(CommandHandler("feed", feed, run_async=True))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

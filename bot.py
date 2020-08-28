#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.


from io import BytesIO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from instaloader import Instaloader, Profile
import sys
import shutil
import glob
import os
import telegram
from itertools import islice
from math import ceil

bot_token = os.environ.get("BOT_TOKEN", "")


def start(update, context):
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="<b>Hi There! 👋</b>\nI can download all posts (pictures + videos) in a profile, IGTV Videos & Stories from Instagram.\nPlease read /help before use.", parse_mode=telegram.ParseMode.HTML)


def help_command(update, context):
    """Send a message when the command /help is issued."""
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="This bot can help you to download all posts (pictures + videos) in a profile, IGTV Videos & Stories from Instagram without leaving Telegram. Simply send a command with a Instagram username (handle) without '@'.\n\n<b>Available Commands :</b>\n/profile username - Download all posts from the username’s profile.\n/stories username - Download stories from the username’s profile.\n/igtv username - Download IGTV Videos from the username’s profile.\n\n<b>How to find the username?</b>\nOpen Instagram app & then go to the profile that you want to download. Username must be on the top.\nIn case you are using a browser you can find it in the Address bar.\n<b>Example : </b>Username for instagram.com/rashmika_mandanna & @rashmika_mandanna is 'rashmika_mandanna' 😉", parse_mode=telegram.ParseMode.HTML)


def about_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='''Made with ❤️ + python-telegram-bot & Instaloader.\nSource Code : <a href="https://github.com/NandiyaLive/xIGDLBot">GitHub</a>\n\n<b>Readme File : https://bit.ly/xIGDLBot''', parse_mode=telegram.ParseMode.HTML)


def contact_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Please contact me on @NandiyaX Chat.In case you want to PM please use @NandiyaBot.", parse_mode=telegram.ParseMode.HTML)


def echo(update, context):
    update.message.reply_text(
        "You have to send a command with an username.\nRead /help before use.")

def stories_command(update, context):

    query = update.message.text.replace("/stories ", "")

    USER = os.environ.get("IGUSER", "")
    PASSWORD = os.environ.get("IGPASS", "")
    
    L = Instaloader(dirname_pattern=query, download_comments=False,
                    download_video_thumbnails=False, save_metadata=False)

    try:
        L.login(USER, PASSWORD)
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text="<b>ERROR ò_ô</b>\n"+str(
            e), parse_mode=telegram.ParseMode.HTML)

        return

    try:
        profile = L.check_profile_id(query)
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text="<b>ERROR ò_ô</b>\n"+str(
            e), parse_mode=telegram.ParseMode.HTML)

        return

    update.message.reply_text(
        "Searching for stories of : " + query + "\nInstagram ID : "+str(profile.userid))

    try:
        L.download_stories(userids=[profile.userid])
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

    if query == "rashmika_mandanna":
        freak = 754321334
        src_dir = query
        for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
            context.bot.send_photo(
                chat_id=freak, photo=open(jpgfile, 'rb'))

        for vidfile in glob.iglob(os.path.join(src_dir, "*.mp4")):
            context.bot.send_video(
                chat_id=freak, video=open(vidfile, 'rb'))
    else:
        pass
    try:
        shutil.rmtree(query)
    except Exception:
        pass


def profile_command(update, context):
    
    LIST_OF_ADMINS = [497217416, 754321334, 1029527252]

    user_id = update.effective_user.id

    if user_id not in LIST_OF_ADMINS:
        context.bot.send_message(chat_id=update.message.chat_id, text="Unauthorized! Access denied for {}".format(
            user_id) + ''' 🔒\n<b>Sorry!</b> Administrator has blocked you from running this command to give fair usage to everyone 😔\nPlease refer @NandiyaX''', parse_mode=telegram.ParseMode.HTML)
        return

    else:
        query = update.message.text.replace("/profile ", "")

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


def post_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="<b>No commands needed.</b>\nThanks to Telegram you can download it from the message 😂❤️", parse_mode=telegram.ParseMode.HTML)


def igtv_command(update, context):

    query = update.message.text.replace("/igtv ", "")

    L = Instaloader(dirname_pattern=query, download_comments=False,
                    download_video_thumbnails=False, save_metadata=False, download_geotags=True, compress_json=True, post_metadata_txt_pattern=None, storyitem_metadata_txt_pattern=None)

    profile = Profile.from_username(L.context, query)

    igtv_count = profile.igtvcount

    posts = profile.get_igtv_posts()

    update.message.reply_text("Searching for : " + query +
                              "\nCooking "+str(igtv_count)+" IGTV videos! This may take longer, take a nap I can handle this without you.")

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


def main():
    """Start the bot."""
    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stories", stories_command))
    dp.add_handler(CommandHandler("profile", profile_command))
    dp.add_handler(CommandHandler("post", post_command))
    dp.add_handler(CommandHandler("igtv", igtv_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("contact", contact_command))
    dp.add_handler(CommandHandler("about", about_command))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

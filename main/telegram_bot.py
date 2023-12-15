import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup


API_URL = "http://localhost:8000"  # Change this according to your FastAPI server
logger = logging.getLogger()

def create_task(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Enter your task like <title> | <theme> | <text>")
    else:
        print(" ".join(context.args))
        title, theme, text = " ".join(context.args).split('|')
        task = " ".join(context.args)
        print("TASK", task)
        response = requests.post(f"{API_URL}/create_task", json={"title": title, "theme": theme, "text" : text})
        update.message.reply_text(response.json()["task"])
        logger.info(f"Created task {task}")


def delete_task(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Please, enter id of task you want to delete")
    else:
        task_id = int(context.args[0])
        response = requests.delete(f"{API_URL}/delete_task?task_id={task_id}")
        update.message.reply_text(response.json()["task"])
        logger.info(f"Deleted task {task_id}")


def get_tasks(update: Update, context: CallbackContext):
    response = requests.get(f"{API_URL}/get_tasks")
    print(f"Response on get_tasks : {response.json()}")
    tasks = [(task['title'], task['id']) for task in response.json()]
    update.message.reply_text(tasks)


def get_task(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Please, enter id of task you want to look through")
    else:
        task_id = int(context.args[0])
        response = requests.get(f"{API_URL}/get_task?task_id={task_id}")
        update.message.reply_text(response.json())


def modify_task(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Enter <old_task_id> | <new_title> | <new_theme> | <new_text>")
    else:

        id, title, theme, text = " ".join(context.args).split('|')
        task = " ".join(context.args)
        print("TASK", task)
        response = requests.put(f"{API_URL}/modify_task?task_id={int(id)}", json={"title": title, "theme": theme, "text" : text})
        update.message.reply_text(response.json()["task"])


def main():
    # Replace with your Telegram bot token
    bot_token = "key"
    updater = Updater(bot_token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("create_task", create_task))
    dp.add_handler(CommandHandler("delete_task", delete_task))
    dp.add_handler(CommandHandler("get_tasks", get_tasks))
    dp.add_handler(CommandHandler("get_task", get_task))
    dp.add_handler(CommandHandler("modify_task", modify_task))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

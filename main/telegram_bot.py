import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup


API_URL = "http://localhost:8000"  # Change this according to your FastAPI server
logger = logging.getLogger()

def get_card(title, theme, text):
    return f"Card Title : {title}\n\nCard Theme : {theme}\n\nTask Text:\n{text}"


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Command list:\n
        1)/register <username>\n
        2)/create_task <title>/<theme>/<text>\n
        3)/get_task <task_id>\n
        4)/modify_task <task_id>/<title>/<theme>/<text>\n
        5)/delete_task <task_id>\n
        """
    )
    user_id = int(update.message.from_user.id)
    print(user_id)
    user = requests.get(f"{API_URL}/get_user?user_id={user_id}")
    print(user)
    if user.status_code != 404:
        update.message.reply_text("Welcome to the bot, old friend!")
        return
    update.message.reply_text("You need to register!\nType /register <username>")


def register(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Wrong command! Type /register <username>")
    print(context.args)
    username = str(context.args[0])
    user_id = int(update.message.from_user.id)
    result = requests.post(f"{API_URL}/create_user", json={"user_id": user_id, "username": username})
    print(result.text)
    update.message.reply_text("Done!")



def create_task(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Enter your task like <title> / <theme> / <text>")
        return
    title, theme, text = [part.strip() for part in " ".join(context.args).split('/')]
    task = " ".join(context.args)
    response = requests.post(f"{API_URL}/create_task?user_id={update.message.from_user.id}", json={"title": title, "theme": theme, "text" : text})
    update.message.reply_text(response.json()["task"])
    logger.info(f"Created task {task}")


def delete_task(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Please, enter id of task you want to delete")
        return
    task_id = int(context.args[0])
    response = requests.delete(f"{API_URL}/delete_task?task_id={task_id}&user_id={update.message.from_user.id}")
    if response.text == 'false':
        update.message.reply_text(f"Task with id {task_id} does not exist")
        return     
    update.message.reply_text(f"Succesfully deleted task {task_id}")
    logger.info(f"Deleted task {task_id}")


def get_tasks(update: Update, context: CallbackContext):
    response = requests.get(f"{API_URL}/get_tasks?user_id={update.message.from_user.id}")
    if len(response.json()) == 0:
        update.message.reply_text("You dont have any tasks yet")
        return
    tasks = "\n\n".join([f"title: {task['title']} | status: {task['status']} | task_id:{task['id']}" for task in response.json()])
    update.message.reply_text(tasks)


def get_task(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Please, enter id of task you want to look through")
        return
    task_id = int(context.args[0])
    response = requests.get(f"{API_URL}/get_task?task_id={task_id}&user_id={update.message.from_user.id}")
    update.message.reply_text(f"title: {response.json()['title']}\ntheme: {response.json()['theme']}\nstatus:  {response.json()['status']}\ntext:\n{response.json()['text']}")


def modify_task(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Enter <old_task_id> / <new_title> / <new_theme> / <new_text>")
        return

    id, title, theme, text = " ".join(context.args).split('/')
    requests.put(f"{API_URL}/modify_task?task_id={int(id)}&user_id={update.message.from_user.id}", json={"title": title, "theme": theme, "text" : text})
    update.message.reply_text("Task succesfully modified!")


def get_better_task(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Enter /get_better_task <text>")
        return
    text = " ".join(context.args)
    response = requests.get(f"{API_URL}/get_better", json={"text": text})
    update.message.reply_text(response.json()["task"])


def switch_status(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Enter /switch_status <task_id> / <new_status>")
        return
    task_id, status = " ".join(context.args).split('/')
    requests.put(f"{API_URL}/switch_status?task_id={task_id}&new_status={status}")
    update.message.reply_text(f"Status updated!\nNow task {task_id} has status {status}")


def get_by_status(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Enter /get_by_status <status>\nStatuses are: opened/in progress/closed")
        return
    status = " ".join(context.args)
    response = requests.get(f"{API_URL}/get_by_status?status={status}&user_id={update.message.from_user.id}")
    if len(response.json()) == 0:
        update.message.reply_text(f"You dont have any tasks in status {status}")
        return
    tasks = "\n\n".join([f"title: {task['title']} | task_id:{task['id']}" for task in response.json()])
    update.message.reply_text(tasks)

def main():
    # Replace with your Telegram bot token
    bot_token = ""
    updater = Updater(bot_token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("create_task", create_task))
    dp.add_handler(CommandHandler("delete_task", delete_task))
    dp.add_handler(CommandHandler("get_tasks", get_tasks))
    dp.add_handler(CommandHandler("get_task", get_task))
    dp.add_handler(CommandHandler("modify_task", modify_task))
    dp.add_handler(CommandHandler("get_better_task", get_better_task))
    dp.add_handler(CommandHandler("switch_status", switch_status))
    dp.add_handler(CommandHandler("get_by_status", get_by_status))



    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

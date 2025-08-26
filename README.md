# where-i-own-telegram

The bot will help you view **channels** and **groups** where you are the **owner** or an **administrator**.

## ✨ Features

* List of channels where you are an admin
* List of group chats where you are an admin
* List of your channels (where you are the owner)
* List of your group chats (where you are the owner)
* After sharing, the bot will return the **chat title** and **chat ID**

## 📦 Requirements

* Python 3.10+
* [python-telegram-bot v21](https://github.com/python-telegram-bot/python-telegram-bot)

Install dependencies:

```bash
pip install python-telegram-bot==21.8 ppython-dotenvyt
mv .env.example .env
```

## ⚙️ Configuration

1. Create a new bot with [@BotFather](https://t.me/BotFather)
2. Copy your **bot token**
3. Replace `BOT_TOKEN` in `.env` with your token

## 🚀 Run the bot

```bash
python bot.py
```

## 📱 Usage

1. Start the bot with `/start`
2. Choose one of the buttons:

   * `list of channels where i am an admin`
   * `list of group chats where i am an admin`
   * `List of my channels`
   * `List of my group chats`
3. Select a chat from the Telegram list
4. The bot will display the chat **name** and **chat ID**

---

**Note that this bot has no superpowers 🦸‍♂️! It does not have any special access to your account and only shows chats where you already have permissions, using Telegram’s pre-defined keys.**

---

> Made with ❤️ by [https://t.me/imSajjadMB](@imSajjadMB)

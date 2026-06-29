# Instagram downloader Telegram Bot

A Telegram bot that allows users to retrieve public Instagram profile information, posts, and stories through an interactive inline keyboard.

## Features

* 📄 View Instagram profile information
* 📸 Download public Instagram posts
* 📱 Download available Instagram stories
* 🤖 Simple Telegram bot interface with inline buttons
* 💬 Persian (Farsi) user interface

## Project Structure

```
.
├── main.py            # Telegram bot
├── instagram_api.py   # Instagram API functions
├── config.py          # Configuration variables
├── requirements.txt   # Python dependencies
└── README.md
```

## Requirements

* Python 3.10+
* A Telegram Bot Token
*  BoxAPI username and password

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/BoxAPIir/Instagram-Downloader-Bot.git
cd instagram-telegram-bot
```

### 2. Create a virtual environment

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Open `config.py` and fill in your credentials:

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
BOXAPI_USERNAME = "YOUR_INSTAGRAM_USERNAME"
BOXAPI_PASSWORD = "YOUR_INSTAGRAM_PASSWORD"
```

## Running the Bot

```bash
python main.py
```

If everything is configured correctly, you should see:

```
Bot is running...
```

## Usage

1. Start the bot using `/start`.
2. Choose one of the available options:

   * **Profile Information**
   * **Stories**
   * **Posts**
3. Send an Instagram username (without `@`).
4. The bot will fetch and send the requested content.

## Configuration Variables

| Variable          | Description                |
| ----------------- | -------------------------- |
| `TELEGRAM_TOKEN`  | Telegram Bot API token     |
| `BOXAPI_USERNAME` | Instagram account username |
| `BOXAPI_PASSWORD` | Instagram account password |

## Notes

* Stories are only returned if they are currently available.
* The bot strips the leading `@` automatically if provided.
* Public content availability depends on the Instagram API implementation.


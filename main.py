from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from instagram_api import get_medias, get_profile, get_stories

from config import TELEGRAM_TOKEN

WAITING_FOR_USERNAME = 1
ACTIONS = {
    "profile": {"label": "اطلاعات پروفایل"},
    "stories": {"label": "استوری ها"},
    "posts": {"label": "پست ها"},
}


async def fetch_and_show_content(
    update: Update, context: ContextTypes.DEFAULT_TYPE, username: str, action: str
):
    try:
        if action == "profile":
            data = get_profile(username)
            text = (
                f"{data['full_name']}\n"
                f"Followers: {data['edge_followed_by']['count']}\n"
                f"Following: {data['edge_follow']['count']}\n"
                f"Bio: {data.get('biography', '')}"
            )
            await update.message.reply_text(text)

        elif action == "stories":
            stories = get_stories(username)

            if not stories:
                await update.message.reply_text("❌ استوری یافت نشد")
                return

            for story_item in stories:
                if "video_versions" in story_item:
                    await update.message.reply_video(
                        story_item["video_versions"][0]["url"]
                    )
                elif "image_versions2" in story_item:
                    await update.message.reply_photo(
                        story_item["image_versions2"]["candidates"][0]["url"]
                    )
                else:
                    await update.message.reply_text("Unsupported media type")

        elif action == "posts":
            posts = get_medias(username)

            if not posts:
                await update.message.reply_text("❌ پستی یافت نشد")
                return

            for media_item in posts:
                if "video_versions" in media_item:
                    await update.message.reply_video(
                        media_item["video_versions"][0]["url"]
                    )
                elif "image_versions2" in media_item:
                    await update.message.reply_photo(
                        media_item["image_versions2"]["candidates"][0]["url"]
                    )
                else:
                    await update.message.reply_text("Unsupported media type")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")


def get_main_menu():
    keyboard = [
        [InlineKeyboardButton(meta["label"], callback_data=action)]
        for action, meta in ACTIONS.items()
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 خوش آمدید ! یک دکمه را انتخاب کنید",
        reply_markup=get_main_menu(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # removes the loading spinner on the button
    action = query.data

    if action in ACTIONS:
        meta = ACTIONS[action]
        context.user_data["action"] = action
        await query.edit_message_text(
            f"{meta['label']}  انتخاب شد لطفا یوزرنیم یک اکانت اینستاگرام را وارد کنید",
        )
        return WAITING_FOR_USERNAME

    return ConversationHandler.END


async def receive_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip().lstrip("@")
    action = context.user_data.get("action", "profile")

    await update.message.reply_text(f"🔍 دریافت {action} برای @{username}...")

    await fetch_and_show_content(update, context, username, action)

    await update.message.reply_text(
        "✅ عملیات تمام شد. یک گزینه دیگر انتخاب کنید.",
        reply_markup=get_main_menu(),
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ لغو شد .از /start استفاده کنید برای شروع مجدد ."
    )
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    actions_pattern = "^(" + "|".join(ACTIONS.keys()) + ")$"
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern=actions_pattern)],
        states={
            WAITING_FOR_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_username)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

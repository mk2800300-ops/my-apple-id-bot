import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = "8630905846:AAHroNMMSn3sPcaEZyEu2RVwdoOklfxSUmA"

# Add all 20 games here: [Button Text, Game ID, Ad Link, Apple ID, Password]
GAMES = {
    "gta": ["1. GTA V", "https://link1.com", "gta@mail.com", "Pass123"],
    "rdr": ["2. Red Dead 2", "https://link2.com", "rdr@mail.com", "Pass456"],
    "mc":  ["3. Minecraft", "https://link3.com", "mc@mail.com", "Pass789"],
    # ... add all 20 here using the same format ...
    "nba": ["20. NBA 2K26", "https://link20.com", "nba@mail.com", "Pass000"],
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This automatically builds the 20 buttons in rows of 2
    keyboard = []
    game_keys = list(GAMES.keys())
    for i in range(0, len(game_keys), 2):
        row = [
            InlineKeyboardButton(GAMES[game_keys[i]][0], callback_data=game_keys[i]),
            InlineKeyboardButton(GAMES[game_keys[i+1]][0], callback_data=game_keys[i+1]) if i+1 < len(game_keys) else None
        ]
        keyboard.append([btn for btn in row if btn])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔥 Select a game to get the Apple ID:", reply_markup=reply_markup)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    game_data = GAMES.get(query.data)
    if not game_data: return

    name, link, apple_id, password = game_data
    
    await query.edit_message_text(
        text=f"🎁 **Selection:** {name}\n\n"
             f"STEP 1: Click the link: {link}\n"
             f"STEP 2: Return here and wait **15 seconds**.\n\n"
             f"⌛ Verifying your visit...",
        parse_mode="Markdown"
    )

    # THE 15-SECOND DELAY
    await asyncio.sleep(15)

    await query.message.reply_text(
        text=f"✅ **Verification Complete!**\n\n"
             f"📧 **ID:** `{apple_id}`\n"
             f"🔑 **PASS:** `{password}`",
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_choice))
    app.run_polling()

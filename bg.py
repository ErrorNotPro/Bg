import telebot
from rembg import remove, new_session
from io import BytesIO
from PIL import Image
import os

API_TOKEN = '8233339248:AAGsB-4sJyeHsHliL6jXAucsr864g7wOXkI'
bot = telebot.TeleBot(API_TOKEN)

# Pre-load the SMALL model to save RAM
print("Loading Lite Model...")
session = new_session("u2netp") 

@bot.message_handler(content_types=['photo', 'sticker'])
def handle_media(message):
    try:
        sent_msg = bot.reply_to(message, "⚡ Using Lite Engine... processing.")
        
        if message.content_type == 'sticker':
            if message.sticker.is_animated or message.sticker.is_video:
                bot.edit_message_text("❌ No animated stickers.", message.chat.id, sent_msg.message_id)
                return
            file_id = message.sticker.file_id
        else:
            file_id = message.photo[-1].file_id

        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Open and process
        img = Image.open(BytesIO(downloaded_file))
        
        # We pass the 'session' we created above to force use of u2netp
        output = remove(img, session=session)
        
        bio = BytesIO()
        output.save(bio, format='PNG')
        bio.seek(0)
        
        bot.send_photo(message.chat.id, bio, caption="✅ Fixed!")
        bot.delete_message(message.chat.id, sent_msg.message_id)
        print("Success: Image sent.")

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ Memory Limit Hit. Try a smaller image.")

if __name__ == "__main__":
    print("Bot is starting...")
    bot.infinity_polling()

import telebot
from rembg import remove
from io import BytesIO
from PIL import Image

# Your Bot Token from @BotFather
API_TOKEN = '8233339248:AAGsB-4sJyeHsHliL6jXAucsr864g7wOXkI'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "📸 Send me a **Photo** or a **Sticker** and I'll remove the background for you!")

# Handles both Photos and Stickers
@bot.message_handler(content_types=['photo', 'sticker'])
def handle_media(message):
    try:
        sent_msg = bot.reply_to(message, "🪄 Processing... one moment.")

        # 1. Determine if it's a sticker or photo and get the file_id
        if message.content_type == 'sticker':
            # Animated stickers (.tgs) cannot be processed this way, only static (.webp)
            if message.sticker.is_animated or message.sticker.is_video:
                bot.edit_message_text("❌ Sorry, I can only process static stickers, not animated ones.", 
                                      message.chat.id, sent_msg.message_id)
                return
            file_id = message.sticker.file_id
        else:
            # Get the highest resolution version of the photo
            file_id = message.photo[-1].file_id

        # 2. Download the file from Telegram
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # 3. Process the image (Works for JPG, PNG, and WebP stickers)
        input_image = Image.open(BytesIO(downloaded_file))
        output_image = remove(input_image)
        
        # 4. Save to buffer
        output_io = BytesIO()
        output_image.save(output_io, format='PNG')
        output_io.seek(0)
        
        # 5. Send back as a photo (as you requested)
        bot.send_photo(message.chat.id, output_io, caption="✅ Background removed!")
        bot.delete_message(message.chat.id, sent_msg.message_id)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

print("Bot is active and waiting for stickers/photos...")
bot.infinity_polling()
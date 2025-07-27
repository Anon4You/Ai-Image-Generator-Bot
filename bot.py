#!/usr/bin/env python

import os
import random
import requests
from urllib.parse import quote
import telebot
from telebot.types import InputMediaPhoto, BotCommand
from io import BytesIO
import json
import time

# Initialize bot
def get_bot_token():
    try:
        with open('token.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise ValueError("token.txt file not found. Please create it with your Telegram bot token.")

TOKEN = get_bot_token()
bot = telebot.TeleBot(TOKEN)

# Set bot commands for suggestions
bot.set_my_commands([
    BotCommand('start', 'Get started with the bot'),
    BotCommand('help', 'How to use the bot'),
    BotCommand('admin', 'About the bot creator'),
    BotCommand('img', 'Generate AI images')
])

# Constants
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024
DEFAULT_MODEL = "flux"
MAX_PROMPT_LENGTH = 400
ARTA_API_KEY = "AIzaSyB3-71wG0fIt0shj0ee4fvx1shcjJHGrrQ"  # Public API key from Arta

# Admin information
ADMIN_INFO = """
🤖 *About This Bot*

*Created by:* Alienkrishn [Anon4You]
*GitHub:* [Anon4You](https://github.com/Anon4You)

This bot uses AI to generate images from text prompts.
"""

# Pollinations.ai image generator
def generate_pollinations_image(prompt, width, height, model):
    try:
        base_url = "https://image.pollinations.ai/prompt/"
        encoded_prompt = quote(prompt)
        
        params = {
            'width': width,
            'height': height,
            'model': model,
            'nologo': 'true',
            'seed': random.randint(10000, 99999),
            'private': 'true',
            'enhance': 'true',
            'referer': 'telebot'
        }
        
        query_string = '&'.join(f"{k}={v}" for k, v in params.items())
        url = f"{base_url}{encoded_prompt}?{query_string}"
        
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        print(f"Pollinations.ai error: {e}")
        return None

# Arta.ai image generator
def generate_arta_image(prompt, width, height, model):
    try:
        # First get auth token
        auth_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser"
        auth_params = {"key": ARTA_API_KEY}
        auth_headers = {
            "X-Android-Cert": "ADC09FCA89A2CE4D0D139031A2A587FA87EE4155",
            "X-Firebase-Gmpid": "1:713239656559:android:f9e37753e9ee7324cb759a",
            "X-Firebase-Client": "H4sIAAAAAAAA_6tWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 15;)"
        }
        
        auth_response = requests.post(
            auth_url,
            params=auth_params,
            headers=auth_headers,
            json={"clientType": "CLIENT_TYPE_ANDROID"},
            timeout=30
        )
        auth_response.raise_for_status()
        token = auth_response.json()["idToken"]
        
        # Determine aspect ratio closest to requested dimensions
        target_ratio = width / height
        ratio_options = {
            "1:1": 1.0,
            "2:3": 2/3,
            "3:2": 3/2,
            "3:4": 3/4,
            "4:3": 4/3,
            "9:16": 9/16,
            "16:9": 16/9,
            "9:21": 9/21,
            "21:9": 21/9
        }
        closest_ratio = min(ratio_options.items(), key=lambda x: abs(x[1] - target_ratio))[0]
        
        # Submit generation request
        gen_url = "https://img-gen-prod.ai-arta.com/api/v1/text2image"
        gen_headers = {
            "Authorization": token,
            "User-Agent": "AiArt/4.18.6 okHttp/4.12.0 Android R",
            "Content-Type": "multipart/form-data"
        }
        
        form_data = {
            "prompt": prompt,
            "negative_prompt": "",
            "style": model,
            "images_num": "1",
            "cfg_scale": "7",
            "steps": "40",
            "aspect_ratio": closest_ratio
        }
        
        gen_response = requests.post(
            gen_url,
            headers=gen_headers,
            data=form_data,
            timeout=30
        )
        gen_response.raise_for_status()
        record_id = gen_response.json()["record_id"]
        
        # Check status until image is ready
        status_url = f"https://img-gen-prod.ai-arta.com/api/v1/text2image/{record_id}/status"
        for _ in range(30):  # 30 attempts with 5 second delay = 2.5 minutes max wait
            status_response = requests.get(status_url, headers=gen_headers, timeout=30)
            status_response.raise_for_status()
            status_data = status_response.json()
            
            if status_data["status"] == "DONE":
                image_url = status_data["response"][0]["url"]
                image_response = requests.get(image_url, stream=True, timeout=30)
                image_response.raise_for_status()
                return BytesIO(image_response.content)
            
            time.sleep(5)
        
        return None
    except Exception as e:
        print(f"Arta.ai error: {e}")
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Send welcome message and instructions"""
    welcome_text = (
        "🖼️ *AI Image Generator Bot*\n\n"
        "*Available Commands:*\n"
        "`/start` or `/help` - Show this help message\n"
        "`/admin` - About the bot creator\n"
        "`/img` - Generate AI images\n\n"
        "✨ *Image Generation Examples:*\n"
        "• `/img a beautiful sunset over mountains`\n"
        "• `/img 512 512 a cute puppy`\n"
        "• `/img 1024 768 flux a futuristic cityscape`\n\n"
        "📏 *Format:* `/img [width] [height] [model] [prompt]`\n"
        "⚙️ *Default Model:* flux (other options: stable-diffusion, dall-e, glide)"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['admin'])
def show_admin_info(message):
    """Show information about the bot creator"""
    bot.reply_to(message, ADMIN_INFO, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['img', 'image', 'generate'])
def handle_image_request(message):
    """Handle image generation requests"""
    try:
        # Parse command arguments
        args = message.text.split()[1:]
        
        if not args:
            bot.reply_to(message, "Please provide a prompt. Example:\n`/img a cute cat`\n\nFor more options, type /help")
            return

        # Default values
        width = DEFAULT_WIDTH
        height = DEFAULT_HEIGHT
        model = DEFAULT_MODEL
        prompt_parts = args
        
        # Parse width if provided
        if len(args) >= 1 and args[0].isdigit():
            width = int(args[0])
            prompt_parts = args[1:]
            
            # Parse height if provided
            if len(args) >= 2 and args[1].isdigit():
                height = int(args[1])
                prompt_parts = args[2:]
                
                # Parse model if provided
                if len(args) >= 3 and args[2].lower() in ['flux', 'stable-diffusion', 'dall-e', 'glide']:
                    model = args[2].lower()
                    prompt_parts = args[3:]

        # Combine remaining parts as prompt
        prompt = ' '.join(prompt_parts).strip()
        
        if not prompt:
            bot.reply_to(message, "Please provide a text prompt to generate an image")
            return
        
        if len(prompt) > MAX_PROMPT_LENGTH:
            bot.reply_to(message, f"Prompt is too long. Maximum {MAX_PROMPT_LENGTH} characters allowed.")
            return

        # Send "generating" message
        wait_msg = bot.reply_to(message, "🖌️ Generating your image... Please wait (this may take a minute)")

        # Try Pollinations.ai first
        image_data = generate_pollinations_image(prompt, width, height, model)
        source = "Pollinations.ai"
        
        # If Pollinations fails, try Arta.ai
        if not image_data:
            bot.edit_message_text("🔄 Pollinations.ai failed, trying Arta.ai...", 
                                message.chat.id, 
                                wait_msg.message_id)
            image_data = generate_arta_image(prompt, width, height, model)
            source = "Arta.ai"

        # Delete the waiting message
        bot.delete_message(message.chat.id, wait_msg.message_id)

        if not image_data:
            bot.reply_to(message, "❌ Failed to generate image from both services. Please try again later.")
            return

        # Send the image
        caption = (
            f"🎨 *Prompt:* {prompt}\n"
            f"📐 *Size:* {width}x{height}\n"
            f"🤖 *Model:* {model}\n"
            f"⚡ *Source:* {source}"
        )
        
        bot.send_photo(
            chat_id=message.chat.id,
            photo=image_data,
            caption=caption,
            parse_mode='Markdown'
        )

    except Exception as e:
        bot.reply_to(message, f"⚠️ An error occurred: {str(e)}")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()

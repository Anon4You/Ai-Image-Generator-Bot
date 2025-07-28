# AI Image Generator Telegram Bot 🤖🎨

A Telegram bot that generates AI images from text prompts using Pollinations.ai and Arta.ai APIs, with automatic fallback between services.

## Features ✨

- **Dual AI Backend**: Uses both Pollinations.ai and Arta.ai for reliable image generation
- **Smart Fallback**: Automatically switches services if one fails
- **Customizable Output**: Control image size and model parameters
- **User-Friendly**: Command suggestions and clear instructions
- **No API Keys Needed**: Uses public endpoints

## Setup and Installation ⚙️

### Prerequisites
- Python 3.8+
- Telegram bot token (get from [@BotFather](https://t.me/BotFather))

### Demo
- For Demo try this [PrompArt BOT](https://t.me/alienimgenbot)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Anon4You/Ai-Image-Generator-Bot.git
   cd Ai-Image-Generator-Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your bot token:
   ```bash
   echo "YOURTELEGRAMBOTTOKENHERE" > token.txt
   ```
   (Replace `YOURTELEGRAMBOTTOKENHERE` with your actual bot token)

4. Run the bot:
   ```bash
   python bot.py
   ```

## Usage 🚀

### Commands
- `/start` or `/help` - Show help message
- `/admin` - Information about the bot creator
- `/img [width] [height] [model] [prompt]` - Generate an image

### Examples
```
/img a beautiful sunset
/img 512 512 a cute puppy
/img 1024 768 stable-diffusion futuristic cityscape
```

## Configuration ⚙️

You can modify these constants in `bot.py`:
- `DEFAULT_WIDTH` - Default image width (1024)
- `DEFAULT_HEIGHT` - Default image height (1024)
- `DEFAULT_MODEL` - Default AI model ("flux")
- `MAX_PROMPT_LENGTH` - Maximum prompt length (400)

## Deployment Options 🌐

The bot can be deployed on:
- Any VPS or cloud server
- AWS Lambda
- Google Cloud Run
- Heroku
- Any Python-compatible hosting

## License 📜
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💖
If you like this project, please consider starring ⭐ the repository!

Created by [Alienkrishn](https://github.com/Anon4You)  
[Report Issues](https://github.com/Anon4You/Ai-Image-Generator-Bot/issues)  
[View on GitHub](https://github.com/Anon4You/Ai-Image-Generator-Bot)

# Telegram Feedback Bot

This is a Telegram bot that collects user feedback on different products. Users can select a language and a product to provide feedback on, answer a series of questions, and submit their feedback.

## Features
- Multi-language support (English, Russian, Uzbek)
- Collects feedback on various products
- Stores feedback in a Google Sheets spreadsheet
- Sends feedback to a Telegram channel

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/nigmatovdev/telegram-feedback-bot.git
   cd telegram-feedback-bot
2. Install the required Python packages:
  ```bash
  pip install -r requirements.txt
  ```
3. Create a creds.json file with your Google Cloud service account credentials:
4. Run the bot
   ```bash
   python bot.py
    
## Usage
1. Start the bot by sending /start in your Telegram chat with the bot.
2. Choose a language from the provided options.
3. Select the product you want to give feedback on.
4. Answer the questions presented by the bot.
5. Your feedback will be submitted and stored in the Google Sheets spreadsheet.

## Configuration 
- Modify languages and products lists in bot.py to add or remove supported languages and products.
- Customize the messages in different languages by updating the translations dictionary in bot.py.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

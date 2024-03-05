import gspread
from oauth2client.service_account import ServiceAccountCredentials
import telebot
from telebot import types
from datetime import datetime

# Google Sheets API setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open("sheet").sheet1  # Replace "sheet" with your Google Sheets document name

# Telegram Bot setup
bot = telebot.TeleBot("YOUR_BOT_TOKEN")  # Replace "YOUR_BOT_TOKEN" with your Telegram Bot token
user_feedback = {}

# List of supported languages and products
languages = ['English', 'Russian', 'Uzbek']
products = ['SAT Program', 'Road to Ivy Program', 'Pre-SAT Math Program', 'Admission Program', 'Kids Program']

# Translations for different languages
translations = {
    'English': {
        'welcome': "To which product you want to give feedback?",
        'not_allowed': "Unfortunately, you can't use this bot. Please contact the admin.",
        'choose_number': "Please select a number:",
        'selected': "You selected: ",
        'comments': "Any comments or concerns you had this past month?",
        'received': "Your feedback for {} has been received.",
        'invalid': "Invalid choice. Please choose one of the provided options.",
        'invalid_product': 'Invalid product. Please choose one of the products.',
        'restart': 'You can start giving feedback.',
        'submit': 'Submit',
        'start_over': 'Start Over',
        'submit_or_start_over': 'Please choose:',
    },
    'Russian': {
        'welcome': "Какой продукт вы хотите оценить?",
        'not_allowed': "К сожалению, вы не можете использовать этого бота. Пожалуйста, свяжитесь с администратором.",
        'choose_number': "Пожалуйста, выберите номер:",
        'selected': "Вы выбрали: ",
        'comments': "Есть ли у вас какие-либо комментарии или вопросы за прошедший месяц?",
        'received': "Ваш отзыв о {} был получен.",
        'invalid': "Неверный выбор. Пожалуйста, выберите один из предложенных вариантов.",
        'invalid_product': 'Неверный продукт. Пожалуйста, выберите один из продуктов.',
        'restart': 'Вы можете начать оставлять отзыв.',
        'submit': 'Отправить',
        'start_over': 'Начать заново',
        'submit_or_start_over': 'Пожалуйста, выберите:',
    },
    'Uzbek': {
        'welcome': "Qaysi mahsulot haqida fikr bildirmoqchisiz?",
        'not_allowed': "Afsuski, siz ushbu botni foydalanish uchun ruxsat etilmagansiz. Iltimos, administrator bilan bog'laning.",
        'choose_number': "Iltimos, raqamni tanlang:",
        'selected': "Siz tanladingiz: ",
        'comments': "O'tgan oyda sizda qanday izohlar yoki tashvishlar bo'ldi?",
        'received': "Sizning {} uchun fikringiz qabul qilindi.",
        'invalid': "Noto'g'ri tanlov. Iltimos, taqdim etilgan variantlardan birini tanlang.",
        'invalid_product': 'Noto\'g\'ri mahsulot. Iltimos, mahsulotlardan birini tanlang.',
        'restart': 'Siz fikr bildirishni boshlashingiz mumkin.',
        'submit': 'Jo\'natish',
        'start_over': 'Boshidan boshlash',
        'submit_or_start_over': 'Iltimos, tanlang:',
    },
}

# List of allowed Telegram group IDs or channel IDs
allowed_group_id = [IDS_OF_YOUR_TELEGRAM_GROUPS_CHANNELS]

# Function to create keyboard markup
def create_keyboard_markup(options):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for option in options:
        markup.add(types.KeyboardButton(option))
    return markup

# Function to check if the user is allowed to use the bot
def is_user_allowed(user_id):
    for group_id in allowed_group_id:
        try:
            member = bot.get_chat_member(group_id, user_id)
            if member.status in ["member", "administrator", "creator"]:
                return True
        except Exception as e:
            print("Error checking user membership:", e)
    return False

# Handler for /start command to choose language
@bot.message_handler(commands=['start'])
def choose_language(message):
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        bot.send_message(user_id, translations['English']['not_allowed'])
        return

    markup = create_keyboard_markup(languages)
    bot.send_message(user_id, "Please choose a language:", reply_markup=markup)

# Handler for /restart command to restart feedback
@bot.message_handler(commands=['restart'])
def restart_feedback(message):
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        bot.send_message(user_id, translations['English']['not_allowed'])
        return

    # Clear user feedback data
    if user_id in user_feedback:
        del user_feedback[user_id]
    
    # Directly go to product selection
    send_product_selection(user_id)

# Function to send product selection message
def send_product_selection(user_id):
    selected_language = user_feedback.get(user_id, {}).get('language')
    if not selected_language:
        markup = create_keyboard_markup(languages)
        bot.send_message(user_id, "Please choose a language:", reply_markup=markup)
        return

    markup = create_keyboard_markup(products)
    bot.send_message(user_id, translations[selected_language]['welcome'], reply_markup=markup)

# Handler for language selection
@bot.message_handler(func=lambda message: message.text in languages)
def handle_language_selection(message):
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        bot.send_message(user_id, translations['English']['not_allowed'])
        return

    selected_language = message.text
    user_feedback[user_id] = {'language': selected_language}
    bot.send_message(user_id, translations[selected_language]['selected'] + selected_language)
    send_product_selection(user_id)

# Handler for product selection
@bot.message_handler(func=lambda message: message.text in products)
def ask_first_question(message):
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        bot.send_message(user_id, translations['English']['not_allowed'])
        return

    product = message.text
    user_feedback[user_id]['product'] = product

    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for i in range(1, 10, 3):
        markup.row(types.KeyboardButton(str(i)), types.KeyboardButton(str(i+1)), types.KeyboardButton(str(i+2)))
    markup.row(types.KeyboardButton('10'))
    bot.send_message(user_id, translations[user_feedback[user_id]['language']]['choose_number'], reply_markup=markup)

# Handler for first question response
@bot.message_handler(func=lambda message: message.text.isdigit() and 1 <= int(message.text) <= 10)
def handle_first_question_response(message):
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        bot.send_message(user_id, translations['English']['not_allowed'])
        return

    if message.text == '/restart':
        restart_feedback(message)
        return

    question1 = int(message.text)
    user_feedback[user_id]['question1'] = question1

    markup = types.ReplyKeyboardRemove()
    bot.send_message(user_id, translations[user_feedback[user_id]['language']]['comments'], reply_markup=markup)

# Handler for second question response
@bot.message_handler(func=lambda message: message.from_user.id in user_feedback and 'question1' in user_feedback[message.from_user.id] and user_feedback[message.from_user.id]['question1'] is not None)
def handle_second_question_response(message):
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        bot.send_message(user_id, translations['English']['not_allowed'])
        return

    if message.text == '/restart':
        restart_feedback(message)
        return

    question2 = message.text
    user_feedback[user_id]['question2'] = question2

    # Save to Google Sheets
    language = user_feedback[user_id]['language']
    product = user_feedback[user_id]['product']
    question1 = user_feedback[user_id]['question1']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    row = [user_id, language, product, question1, question2, timestamp]
    sheet.append_row(row)

    # Send feedback to the Telegram channel
    feedback_message = f"New feedback received:\nUser ID: {user_id}\nLanguage: {language}\nProduct: {product}\nQuestion 1: {question1}\nQuestion 2: {question2}\nTimestamp: {timestamp}"
    bot.send_message(CHANNEL_TO_SEND_MESSAGE, feedback_message)

    bot.send_message(user_id, "Thank you! Your feedback has been submitted. You can submit another feedback by clicking /restart.")

# Start the bot
bot.infinity_polling()

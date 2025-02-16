from server import keep_alive
keep_alive() 
import telebot 
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7891897463:AAG7zHbmfHovsrUk_7ZImFrIbvGqBImWltk"
bot = telebot.TeleBot(TOKEN)

courses = {
    "First Year - First Term": {
        "message": "📚 اختر المادة التي تريدها:",
        "button_text": "📖 الترم الأول - السنة الأولى",
        "subjects": {
            "🏥 Physiology 1": "https://t.me/theraflow_1/26/27",
            "🦴 Anatomy 1": "https://t.me/theraflow_1/29/30",
            "🧪 Biochemistry 1": "https://t.me/theraflow_1/31/32",
            "⚡ Biophysics 1": "https://t.me/theraflow_1/33/34",
            "🧫 Histology": "https://t.me/theraflow_1/35/36",
        },
        "parent": "First Year"
    },
    "First Year - Second Term": {
        "message": "📚 اختر المادة التي تريدها:",
        "button_text": "📖 الترم الثاني - السنة الأولى",
        "subjects": {
            "🏥 Physiology 2": "https://t.me/theraflow_1/2/4",
            "🦴 Anatomy 2": "https://t.me/theraflow_1/5/7",
            "🧪 Biochemistry 2": "https://t.me/theraflow_1/9/10",
            "⚡ Biophysics": "https://t.me/theraflow_1/11/12",
            "🏃‍♂️ Kinesiology": "https://t.me/theraflow_1/13/14",
            "📖 Terminology": "https://t.me/theraflow_1/15/16",
            "🏥 Medical & Health": "https://t.me/theraflow_1/17/18",
            "💪 Muscle Test 1": "https://t.me/theraflow_1/19/20",
        },
        "parent": "First Year"
    },
    "Second Year - First Term": {
        "message": "📚 اختر المادة التي تريدها:",
        "button_text": "📖 الترم الأول - السنة الثانية",
        "subjects": {
            "🧠 Neurophysiology": "https://t.me/Theraflow2nd/2/3",
            "🏥 Neuroanatomy": "https://t.me/Theraflow2nd/4/5",
            "⚡ Electrotherapy 1": "https://t.me/Theraflow2nd/8/10",
            "💆‍♂️ Therapeutic 1": "https://t.me/Theraflow2nd/6/7",
            "✍️ Scientific Writing": "https://t.me/Theraflow2nd/14/15",
            "💪 Muscle Test 2": "https://t.me/Theraflow2nd/12/19",
            "🧠 علم النفس": "https://t.me/Theraflow2nd/16/17",
        },
        "parent": "Second Year"
    },
    "Second Year - Second Term": {
        "message": "📚 اختر المادة التي تريدها:",
        "button_text": "📖 الترم الثاني - السنة الثانية",
        "subjects": {
            "🏃‍♂️ Ex. Physiology": "https://t.me/Theraflow2nd/23/24",
            "🦴 Anatomy 4": "https://t.me/Theraflow2nd/25/26",
            "💦 Hydrotherapy": "https://t.me/Theraflow2nd/27/28",
            "⚡ Electrotherapy 2": "https://t.me/Theraflow2nd/29/30",
            "💆‍♂️ Therapeutic 2": "https://t.me/Theraflow2nd/31/32",
            "✋ Manual": "https://t.me/Theraflow2nd/33/34",
            "📏 Biomechanics": "https://t.me/Theraflow2nd/35/36",
        },
        "parent": "Second Year"
    }
}

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📚 السنة الأولى"), KeyboardButton("📚 السنة الثانية"))
    return markup

def term_menu(year):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for term, details in courses.items():
        if year in term:
            markup.add(KeyboardButton(details["button_text"]))
    markup.add(KeyboardButton("🌝 الرجوع"), KeyboardButton("☺️ القائمة الرئيسية"))
    return markup

def subject_menu(term):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if term in courses and courses[term]["subjects"]:
        for subject in courses[term]["subjects"]:
            markup.add(KeyboardButton(subject))
    markup.add(KeyboardButton("🌝 الرجوع"), KeyboardButton("☺️ القائمة الرئيسية"))
    return markup

user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = "main"
    bot.send_message(message.chat.id, "بسم الله الرحمن الرحيم، صل على الحبيب ♡゙", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text in ["📚 السنة الأولى", "📚 السنة الثانية"])
def send_terms(message):
    year = "First Year" if "الأولى" in message.text else "Second Year"
    user_states[message.chat.id] = year
    bot.send_message(message.chat.id, f"📖 اختر الترم الخاص بـ {message.text}:", reply_markup=term_menu(year))

@bot.message_handler(func=lambda message: any(message.text == details["button_text"] for details in courses.values()))
def send_subjects(message):
    for term, details in courses.items():
        if message.text == details["button_text"]:
            user_states[message.chat.id] = term
            bot.send_message(message.chat.id, details["message"], reply_markup=subject_menu(term))
            return

@bot.message_handler(func=lambda message: any(message.text in courses[term].get("subjects", {}) for term in courses))
def send_links(message):
    for term, details in courses.items():
        if message.text in details["subjects"]:
            bot.send_message(message.chat.id, f"📚 رابط المادة: {details['subjects'][message.text]}")
            return

@bot.message_handler(func=lambda message: message.text in ["🌝 الرجوع", "☺️ القائمة الرئيسية"])
def navigate(message):
    user_id = message.chat.id
    if message.text == "🌝 الرجوع":
        if user_id in user_states:
            previous_state = user_states[user_id]
            if previous_state in courses and "parent" in courses[previous_state]:
                parent = courses[previous_state]["parent"]
                user_states[user_id] = parent
                bot.send_message(user_id, "🌝 الرجوع للقائمة السابقة:", reply_markup=term_menu(parent))
            else:
                user_states[user_id] = "main"
                bot.send_message(user_id, "🌝 الرجوع للقائمة الرئيسية:", reply_markup=main_menu())
        else:
            user_states[user_id] = "main"
            bot.send_message(user_id, "🌝 الرجوع للقائمة الرئيسية:", reply_markup=main_menu())
    elif message.text == "☺️ القائمة الرئيسية":
        user_states[user_id] = "main"
        bot.send_message(user_id, "بسم الله الرحمن الرحيم، صل على الحبيب ♡゙", reply_markup=main_menu())

bot.polling()
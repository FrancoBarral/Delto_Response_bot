import telebot
from telebot import types
from dotenv import load_dotenv
from apps.weather.weather import get_weather, get_recommendation
from apps.counter.counter import update_count, get_count
from apps.sentiments.sentiments import analyze_sentiment, get_additional_info
from apps.translate.translate import translate_text
import os


load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

bot = telebot.TeleBot(API_TOKEN)

user_conversations = {}


#Creation of menu 
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
weather_btn = types.KeyboardButton("¡Quiero saber el clima!")
count_btn = types.KeyboardButton("¡Quiero contar!")
sentiment_btn = types.KeyboardButton("¡Analizar sentimiento!")
translate_btn = types.KeyboardButton("¡Quiero traducir texto!")
markup.add(weather_btn, count_btn, sentiment_btn, translate_btn)

#Initial message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hola, ¿Que necesitas?", reply_markup=markup)

#Creation of principal menu and the interaction with it
@bot.message_handler(func=lambda message: True)
def menu_response(message):
    #take the user_id and the text
    user_id = message.from_user.id
    text = message.text
    
    if user_id not in user_conversations:
        user_conversations[user_id] = ""

    #connect all messages that there are in the chat
    user_conversations[user_id] += f"{text}\n"
    
    #We validate the user action
    if text == "¡Quiero saber el clima!":
        msg = bot.reply_to(message, "Por favor, ingresa el nombre de la ciudad:")
        bot.register_next_step_handler(msg, fetch_weather)
    elif text == "¡Quiero contar!":
        update_count(user_id)
        count = get_count(user_id)
        bot.send_message(message.chat.id, f"Has interactuado {count} veces con esta opción.", reply_markup=markup)
    elif text == "¡Analizar sentimiento!":
        sentiment = analyze_sentiment(user_conversations[user_id])
        bot.send_message(message.chat.id, f"Sentimiento analizado: {sentiment}", reply_markup=markup)
    elif text == "¡Quiero traducir texto!":
        msg = bot.reply_to(message, "Por favor, ingresa el texto que deseas traducir:")
        bot.register_next_step_handler(msg, ask_target_language)    
    else:
        bot.send_message(message.chat.id, "Por favor, selecciona una opción válida.", reply_markup=markup)


def fetch_weather(message):
    """ We generate the message to deliver to the client with the weather information """
    city_name = message.text
    weather_data = get_weather(city_name)
    
    if weather_data:
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        recommendation = get_recommendation(description)
        
        # Generar respuesta adicional sobre la ciudad
        additional_info = get_additional_info(city_name)
        
        response = (f"El clima en {city_name}:\n"
                    f"Temperatura: {temp}°C\n"
                    f"Condiciones: {description}\n"
                    f"Recomendación: {recommendation}\n\n"
                    f"Información adicional: {additional_info}")
    else:
        response = "No se pudo obtener la información del clima. Por favor, intenta de nuevo."
    
    bot.send_message(message.chat.id, response, reply_markup=markup)


def ask_target_language(message):
    """ We obtain the message to be translated and we consult which language we need to translate to """
    user_id = message.from_user.id
    user_conversations[user_id] += f"User: {message.text}\n"
    
    msg = bot.reply_to(message, "¿A qué idioma deseas traducir el texto?")
    bot.register_next_step_handler(msg, perform_translation)
    
def perform_translation(message):
    """ We obtain the message again, the language to be translated, and we return the translated message """
    user_id = message.from_user.id
    user_conversations[user_id] += f"User: {message.text}\n"
    
    text_to_translate = user_conversations[user_id].split("User:")[-2].strip()
    target_language = message.text
    
    translation = translate_text(text_to_translate, target_language)
    user_conversations[user_id] += f"Bot: {translation}\n"
    
    bot.send_message(message.chat.id, f"Traducción al {target_language}:\n{translation}", reply_markup=markup)   
    
# Inicia el bot
bot.polling()
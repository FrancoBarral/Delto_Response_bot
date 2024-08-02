import requests
import os
from dotenv import load_dotenv

load_dotenv() 

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")


def get_weather(city_name):
    """This function return de Weather depends about the City Name"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=es"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_recommendation(description):
    """ 
        Returns a recommendation based on time. 
        The description of the climate is passed through parameters. 
    """
    if "lluvia" in description or "llovizna" in description:
        return "Lleva un paraguas."
    elif "nieve" in description:
        return "Abrígate bien, va a nevar."
    elif "despejado" in description:
        return "El clima está despejado. ¡Disfruta tu día!"
    else:
        return "Ten un buen día."
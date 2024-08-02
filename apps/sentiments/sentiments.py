import openai
import os

api_key = os.getenv("OPENAI_API_KEY")

def analyze_sentiment(conversation):
    """
        We analyze the sentiment based on the conversation entered by parameters.
    """
    response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
            {"role": "system", "content": "Eres un asistente que analiza el sentimiento de las conversaciones."},
            {"role": "user", "content": f"Analiza el sentimiento de la siguiente conversación y clasifícalo como positivo, negativo o neutral. Proporcione una breve explicación.\n\n{conversation}"}
        ]
    )
    
    return response['choices'][0]['message']['content'].strip()

def get_additional_info(city_name):
    """ 
        We obtain the additional information for the complete explanation of time. 
        We pass the name of the city through parameters to ask artificial intelligence for information
         
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente que proporciona información interesante y consejos adicionales sobre ciudades."},
            {"role": "user", "content": f"Brindar breve información de interés sobre la ciudad de {city_name}."}
        ]
    )
    return response['choices'][0]['message']['content'].strip()  
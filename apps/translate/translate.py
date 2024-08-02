import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_text(text, target_language):
    """
        We translate the text delivered by the client, by consulting artificial intelligence. 
        The text and the language to be translated are passed through parameters.
    """
    prompt = f"Traducir el siguiente texto:  {target_language}:\n\n{text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sos un asistente de traduccion. "},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response['choices'][0]['message']['content'].strip()
import openai
from openai import OpenAI
import config
import typer
import requests
import glob
import os
client = OpenAI(api_key=config.api_key)

def main():
    # Listar los comandos para la interacción
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="Bienvenido a LAPA. "
               "Para cerrar el programa diga ¡Salir!. "
               "Para crear una nueva conversación diga ¡Nuevo chat!. "
               "Para buscar en internet diga ¡Buscar!")
    response.stream_to_file("output.wav")
    os.system("mpg321 output.wav")
    os.remove("output.wav")

    # Rol a cumplir para ChatGPT
    contexto = {"role": "system",
                "content": "Eres un experto general, sabes sobre todos los temas."}
    messages = [contexto]

    while True:
            archivos_audio = glob.glob("audio*.wav")
            if archivos_audio:
                # Ordenar los archivos para procesar el más antiguo primero
                archivos_audio.sort()
                for archivo_audio in archivos_audio:
                    transcript = __transcripcion_audio(archivo_audio)
                    content = transcript.text
                    os.remove(archivo_audio)

                    # Si se quiere crear una nueva conversación
                    if content == "Nuevo chat" or content == "nuevo chat" or content == "Nuevo chat." or content == "nuevo chat." or content == "¡Nuevo chat!":
                        response_audio = client.audio.speech.create(model="tts-1", voice="alloy", input="¡Se creó una nueva conversación!")
                        response_audio.stream_to_file("output.wav")
                        os.system("mpg321 output.wav")
                        os.remove("output.wav")
                        messages = [contexto]

                    elif content == "Subtítulos realizados por la comunidad de Amara.org":
                        continue

                    # Si no se crea un nuevo chat, continuar
                    else:
                        # Si se quiere realizar una búsqueda en internet
                        if content.startswith("Buscar") or content.startswith("buscar"):
                            search_query = content[len("Buscar"):].strip()
                            if search_query:
                                response_audio = client.audio.speech.create(model="tts-1", voice="alloy", input="Realizando la búsqueda.")
                                response_audio.stream_to_file("output.wav")
                                os.system("mpg321 output.wav")
                                os.remove("output.wav")
                                search_results = buscar_en_internet(search_query)
                                response_content = procesar_resultados(search_results)
                                messages.append({"role": "assistant", "content": response_content})

                        # Para que guarde el contexto de la pregunta
                        messages.append({"role": "user", "content": content})

                        # Modelo a utilizar
                        response = client.chat.completions.create(model="gpt-4", messages=messages, temperature=0, max_tokens=500)

                        # Para escoger solo 1 respuesta
                        response_content = response.choices[0].message.content

                        # Para que hable (TTS)
                        response_audio = client.audio.speech.create(model="tts-1", voice="alloy", input=response_content)
                        response_audio.stream_to_file("output.wav")
                        os.system("mpg321 output.wav")
                        os.remove("output.wav")

                        # Para que guarde el contexto de la respuesta
                        messages.append({"role": "assistant", "content": response_content})

def __transcripcion_audio(archivo_audio: str):
    audio_file = open(archivo_audio, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, language="es")

    # Por si desea salir
    if transcript.text == "Salir" or transcript.text == "salir" or transcript.text == "Salir." or transcript.text == "salir.":
        response_audio = client.audio.speech.create(model="tts-1", voice="alloy", input="¡Adiós! Espero haberte ayudado.")
        response_audio.stream_to_file("output.wav")
        os.system("mpg321 output.wav")
        os.remove("output.wav")
        raise typer.Abort()
    return transcript

def buscar_en_internet(query: str) -> str:
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": config.custom_search,
        "cx": config.custom_search_cx,
        "q": query,
    }

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"No se pudieron obtener resultados para: {query}"

def procesar_resultados(resultados):
    # Si hubo un error en la búsqueda, devuelve el mensaje de error
    if "error" in resultados:
        return resultados["error"]

    # Si no hubo error pero tampoco se encontraron resultados
    items = resultados.get('items')
    if not items:
        return "No se encontraron resultados para tu búsqueda."

    # Si se encontraron resultados, procesa los datos
    respuestas = []
    for item in items[:5]:
        respuesta = item['title'] + ": " + item['snippet']
        if 'link' in item:
            respuesta += " Más información"
        respuestas.append(respuesta)
    return "\n".join(respuesta)

if __name__ == "__main__":
    typer.run(main)

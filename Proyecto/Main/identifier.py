import openai
from openai import OpenAI
import config
import glob
import time
import os
import subprocess
import torchaudio
from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.inference.speaker import SpeakerRecognition


client = OpenAI(api_key=config.api_key)
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")
verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")

def transcribe_audio(audio_filename):
    while True:
        try:
            with open(audio_filename, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, language="es")
                return transcript.text.lower()
        except FileNotFoundError:
            return ""
        except openai.OpenAIError as e:
            time.sleep(3)
            
def verify_speakers(audio_file1, audio_file2):
    score, prediction = verification.verify_files(audio_file1, audio_file2)
    return score, prediction


# Bucle principal
while True:
    # Buscar el primer archivo de audio que coincida con el patrón
    audio_files = glob.glob("audio*.wav")

    if audio_files:
        # Ordenar los archivos para procesar el más antiguo primero
        audio_files.sort()

        for audio_filename in audio_files:
            transcript = transcribe_audio(audio_filename)
        
            if transcript:
                # Imprimir el nombre del audio junto con la transcripción
                print(f"Transcripción de '{audio_filename}':")
                print(transcript)

                if transcript.strip() == "abrir chat" or transcript.strip() == "abrir chat." or transcript.strip() == "abre el chat.":
                    # Añadir la lógica de detección de mismo hablante
                    sample1 = "/home/ezequiel/Desktop/Proyecto_AI/Proyecto/Main/Embeddings/marvin_sample.wav"
                    sample2 = audio_filename
                    score, prediction = verify_speakers(sample1, sample2)
                    print(f"Prediction: {prediction}")
                    
                    #creo que hay que repetir varias veces la comparación para distintas personas, hay que probar esto
                    
                    
                    
                    if prediction:
                        
                        response = client.audio.speech.create(
                        model="tts-1",
                        voice="alloy",
                        input="Los hablantes coinciden. ")
                        response.stream_to_file("output.wav")
                        os.system("mpg321 output.wav")
                        os.remove("output.wav")
                        main_process = subprocess.Popen(["/usr/bin/python3", "main.py"])

                        # Esperar a que main.py termine
                        main_process.wait()
                        
                    else:
                        
                        sample3 = "/home/ezequiel/Desktop/Proyecto_AI/Proyecto/Main/Embeddings/ezequiel_sample.wav"
                        score, prediction = verify_speakers(sample3, sample2)
                        print(f"Prediction: {prediction}")
                        
                    if prediction:
                        
                        
                        response = client.audio.speech.create(
                        model="tts-1",
                        voice="alloy",
                        input="Los hablantes coinciden. ")
                        response.stream_to_file("output.wav")
                        os.system("mpg321 output.wav")
                        os.remove("output.wav")
                        main_process = subprocess.Popen(["/usr/bin/python3", "main.py"])

                        # Esperar a que main.py termine
                        main_process.wait()
                        
                    else:
                        response = client.audio.speech.create(
                        model="tts-1",
                        voice="alloy",
                        input="Los hablantes no coinciden. Prosigo a seguir buscando la palabra clave. ")
                        response.stream_to_file("output.wav")
                        os.system("mpg321 output.wav")
                        os.remove("output.wav")
           
            # Eliminar el archivo de audio después de procesarlo
            time.sleep(1)
            os.remove(audio_filename)


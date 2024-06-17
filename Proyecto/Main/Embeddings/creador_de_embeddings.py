import torch
import torchaudio
from speechbrain.inference import SpeakerRecognition

# Cargar el modelo de reconocimiento de hablante de SpeechBrain
speaker_recognizer = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="tmpdir")

# Ruta al archivo de audio de Ezequiel
ezequiel_audio_path = "/home/ezequiel/Desktop/Proyecto/Proyecto/Grabaciones/Embeddings/ezequiel_sample.wav"  # Asegúrate de que este archivo exista en el mismo directorio

# Cargar el audio
signal, fs = torchaudio.load(ezequiel_audio_path)

# Generar el embedding
embedding = speaker_recognizer.encode_batch(signal)

# Guardar el embedding en un archivo
torch.save(embedding, "/home/ezequiel/Desktop/Proyecto/Proyecto/Grabaciones/Embeddings/ezequiel_embedding.pt")

print("Embedding de Ezequiel generado y guardado en 'ezequiel_embedding.pt'")

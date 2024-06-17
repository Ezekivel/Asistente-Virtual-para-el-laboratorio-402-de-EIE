import torchaudio
from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.inference.speaker import SpeakerRecognition

classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")
signal, fs =torchaudio.load('/home/ezequiel/Desktop/Proyecto/Proyecto/Grabaciones/Embeddings/ezequiel_sample.wav')
embeddings = classifier.encode_batch(signal)

verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
score, prediction = verification.verify_files("/home/ezequiel/Desktop/Proyecto/Proyecto/Grabaciones/Embeddings/ezequiel_sample.wav", "/home/ezequiel/Desktop/Proyecto/Proyecto/Grabaciones/Embeddings/juampa_sample.wav") # Different Speakers
print(f"Different Speakers - Score: {score}, Prediction: {prediction}")


score, prediction = verification.verify_files("/home/ezequiel/Desktop/Proyecto/Proyecto/Grabaciones/Embeddings/ezequiel_sample.wav", "/home/ezequiel/Desktop/Proyecto/Proyecto/Grabaciones/Embeddings/ezequiel_sample2.wav") # Same Speaker
print(f"Same Speaker - Score: {score}, Prediction: {prediction}")

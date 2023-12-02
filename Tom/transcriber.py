import openai
from pydub import AudioSegment
import io

class Transcriber:
    def __init__(self):
        pass

    def transcribe(self, audio):
        # Convertir el objeto AudioData a un objeto de AudioSegment
        audio_segment = AudioSegment.from_file(io.BytesIO(audio.get_wav_data()), format="wav")

        # Guardar el AudioSegment en un archivo temporal
        temp_audio_path = "audio.wav"
        audio_segment.export(temp_audio_path, format="wav")

        # Abrir el archivo temporal y transcribir con OpenAI Whisper
        with open(temp_audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        return transcript.text

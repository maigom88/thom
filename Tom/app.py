import os
import openai
from dotenv import load_dotenv
import streamlit as st
import sqlite3
import json
import speech_recognition as sr  # Añadir la biblioteca de reconocimiento de voz
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand
from transcriber import Transcriber
# Cargar llaves
#+++++++++++++++++++++++++++
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
#+++++++++++++++++++++++++++

# Fucniones
#+++++++++++++++++++++++++++
# Función para transcribir audio desde el micrófono
def audio_transcription():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("Di algo...")
        audio = recognizer.listen(source)


    try:
        #text = recognizer.recognize_google(audio)
        st.write("Procesando...")
        st.audio(audio.get_wav_data(), format="audio/wav", start_time=0)
        text = Transcriber().transcribe(audio)
        return text
    except sr.UnknownValueError:
        st.write("No se pudo entender el audio")
        return ""
    except sr.RequestError as e:
        st.write(f"Error en la solicitud al servicio de reconocimiento de voz; {e}")
        return ""

# Definir la función audio para procesar el texto transrito
def audio(audio_text):
    # Resto del código de la función audio (sin cambios)
    llm = LLM()

    function_name, args, message = llm.process_functions(audio_text)
    if function_name is not None:
        #Si se desea llamar una funcion de las que tenemos
        if function_name == "get_weather":
            #Llamar a la funcion del clima
            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            print(f"Respuesta de la funcion: {function_response}")
            
            final_response = llm.process_response(audio_text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "send_email":
            #Llamar a la funcion para enviar un correo
            ##final_response = "Se envia correo a:... @gmail.com"
            function_response = audio_text
            function_response = json.dumps(function_response)
            final_response = llm.process_response(audio_text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "open_chrome":
            PcCommand().open_chrome(args["website"])
            final_response = "Listo, ya abrí chrome en el sitio " + args["website"]
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "tom":
            function_response = audio_text
            function_response = json.dumps(function_response)
            final_response = llm.process_response(audio_text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
    else:
        final_response = "No tengo idea de lo que estás hablando"
        #function_response = audio_text
        #print(f"Respuesta de la funcion: {function_response}")
        #final_response = llm.process_response(audio_text, message, function_name, function_response)
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}
#+++++++++++++++++++++++++++

# Conecta a la base de datos
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()

# Interfaz de inicio de sesión
st.title('Inicio de Sesión')

# Campos de entrada del usuario y contraseña
username = st.text_input('Usuario:')
password = st.text_input('Contraseña:', type='password')

# Botón de inicio de sesión
if st.button('Iniciar Sesión'):
    # Verifica las credenciales en la base de datos
    result = c.execute('SELECT * FROM usuarios WHERE username=? AND password=?', (username, password)).fetchone()

    if result:
        st.success('Inicio de sesión exitoso')
        # Aquí puedes redirigir al usuario a la parte principal de tu aplicación

        # Añadir widget para cargar archivo de audio
        st.write("Habla algo para ser transcrita:")
        audio_text = audio_transcription()
        st.write(f"Texto transcrito: {audio_text}")
        
        # Llamar a la función audio con el texto transrito
        audio_result = audio(audio_text)
        st.write(audio_result)

        # Reproducir el archivo de audio en la interfaz de Streamlit
        if "file" in audio_result and audio_result["file"]:
            audio_file_path = "static/" + audio_result["file"]

            st.audio(audio_file_path, format="audio/mp3", start_time=0)
            # Mostrar el botón "Reproducir" que activará la reproducción automática usando JavaScript
            #play_button = f'<button onclick="var audio = new Audio(\'{audio_file_path}\'); audio.play();">Reproducir</button>'
            #st.markdown(play_button, unsafe_allow_html=True)
    else:
        st.error('Credenciales incorrectas')

conn.close()

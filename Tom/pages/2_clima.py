import streamlit as st
import os
import pandas as pd
from tensorflow.keras.models import load_model

# Cargar el modelo
modelo_path = os.path.abspath('models/data/climav1.h5')
modelo = load_model(modelo_path)

# Crear una función para realizar la predicción
def realizar_prediccion(temp_media, humedad_media, precipitacion, evaporacion, radiacion, temp_maxima, temp_minima):
    # Realizar la predicción
    entrada = [[temp_media, humedad_media, precipitacion, evaporacion, radiacion, temp_maxima, temp_minima]]
    prediccion = modelo.predict(entrada)
    return prediccion

# Crear una interfaz de usuario con Streamlit
st.title('Predicción del Clima')

# Agregar sliders y textboxes para las variables
temp_media = st.slider('Temperatura Media', min_value=-10, max_value=40, value=25)
humedad_media = st.slider('Humedad Media', min_value=0, max_value=100, value=50)
precipitacion = st.slider('Precipitación', min_value=-10, max_value=75, value=25)
evaporacion = st.slider('Evaporación', min_value=0, max_value=10, value=4)
radiacion = st.slider('Radiación', min_value=-10, max_value=700, value=350)
temp_maxima = st.slider('Temperatura Máxima', min_value=-15, max_value=40, value=25)
temp_minima = st.slider('Temperatura Mínima', min_value=-5, max_value=30, value=20)

# Crear un botón para realizar la predicción
if st.button('Realizar Predicción'):
    # Obtener la predicción
    resultado_prediccion = realizar_prediccion(temp_media, humedad_media, precipitacion, evaporacion, radiacion, temp_maxima, temp_minima)
    
    # Mostrar los resultados
    st.write('Predicción:', resultado_prediccion)

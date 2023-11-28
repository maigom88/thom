import streamlit as st
import sqlite3

#st.set_page_config(page_title ="Bienvenido", page_icon=":D")
#st.title("Bienvenido")
#st.header("Encabezado")
#st.subheader("Subencabezado")
#st.markdown("# Markdown")
#st.success("")
#st.info("")
#st.warning("")
#st.error("")
#st.error("")

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
    else:
        st.error('Credenciales incorrectas')

conn.close()
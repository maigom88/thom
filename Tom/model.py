import sqlite3

conn = sqlite3.connect('usuarios.db')
c = conn.cursor()

# Crea la tabla de usuarios
c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')

# Agrega un usuario de ejemplo
c.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', ('master', 'blazter'))

conn.commit()
conn.close()
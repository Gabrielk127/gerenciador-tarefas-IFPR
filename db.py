import sqlite3
from tkinter import messagebox

def init_db():
    """Inicializa o banco de dados e cria a tabela de usuários, se não existir."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    """Registra um novo usuário no banco de dados."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Nome de usuário já existe.")
    conn.close()

def verify_user(username, password):
    """Verifica as credenciais do usuário no banco de dados."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

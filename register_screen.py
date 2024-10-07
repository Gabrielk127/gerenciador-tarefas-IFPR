import tkinter as tk
from tkinter import messagebox
from db import register_user

class RegisterScreen:
    def __init__(self, root, switch_to_login_screen):
        self.root = root
        self.root.title("Registro")
        self.root.geometry("400x300")
        self.switch_to_login_screen = switch_to_login_screen

        tk.Label(root, text="Registro", font=("Arial", 16)).pack(pady=20)

        tk.Label(root, text="Usuário").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Senha").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.register_button = tk.Button(root, text="Registrar", command=self.register)
        self.register_button.pack(pady=20)

        self.back_button = tk.Button(root, text="Voltar", command=self.switch_to_login_screen)
        self.back_button.pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            register_user(username, password)
            self.switch_to_login_screen()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos")

import tkinter as tk
from tkinter import messagebox
from db import verify_user

class LoginScreen:
    def __init__(self, root, switch_to_register_screen):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        self.switch_to_register_screen = switch_to_register_screen

        tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=20)

        tk.Label(root, text="Usuário").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Senha").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = tk.Button(root, text="Registrar", command=self.switch_to_register_screen)
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if verify_user(username, password):
            self.root.destroy()
            from task_manager import TaskManagerApp
            app_root = tk.Tk()
            TaskManagerApp(app_root, username)
            app_root.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

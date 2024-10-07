import tkinter as tk
from login_screen import LoginScreen
from register_screen import RegisterScreen
from db import init_db

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_root()
        LoginScreen(self.root, self.show_register_screen)

    def show_register_screen(self):
        self.clear_root()
        RegisterScreen(self.root, self.show_login_screen)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    init_db()  # Inicializa o banco de dados
    app = App()
    app.run()

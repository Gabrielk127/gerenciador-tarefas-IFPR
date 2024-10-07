import tkinter as tk
from tkinter import ttk
import psutil

class TaskManagerApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Gerenciador de Tarefas - Usuário: {username}")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E2E2E")

        self.sort_column_index = None
        self.sort_reverse = False

        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame, columns=("PID", "Nome do Processo", "Prioridade", "Uso da CPU (%)", "Estado", "Espaço de Memória (MB)"), show="headings")
        style = ttk.Style()
        style.configure("Treeview", background="#F0F0F0", foreground="#000000", rowheight=25, fieldbackground="#F0F0F0")
        style.map("Treeview", background=[("selected", "#0078D7")])

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, anchor="center")

        self.scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_button = tk.Button(root, text="Atualizar", command=self.update_process_list, bg="#0078D7", fg="white", font=("Arial", 12))
        self.refresh_button.pack(pady=10)

        self.process_list = []
        self.update_process_list()
        self.auto_update()

    def update_process_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.process_list = []
        for proc in psutil.process_iter(attrs=['pid', 'name', 'nice', 'cpu_percent', 'status', 'memory_info']):
            try:
                priority = "Baixa"
                if proc.info['nice'] is not None:
                    if proc.info['nice'] == 32:
                        priority = "Média"
                    elif proc.info['nice'] == 64:
                        priority = "Alta"

                memory_mb = round(proc.info['memory_info'].rss / (1024 * 1024), 2)
                cpu_usage = proc.info['cpu_percent']
                state = proc.info['status']

                self.process_list.append((proc.info['pid'], proc.info['name'], priority, cpu_usage, state, memory_mb))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        for process in self.process_list:
            self.tree.insert("", "end", values=process)

        self.sort_process_list()

    def sort_process_list(self):
        if self.sort_column_index is not None:
            self.process_list.sort(key=lambda x: x[self.sort_column_index], reverse=self.sort_reverse)

            for i in self.tree.get_children():
                self.tree.delete(i)

            for process in self.process_list:
                self.tree.insert("", "end", values=process)

    def sort_column(self, column):
        col_index = self.tree["columns"].index(column)
        self.sort_reverse = not self.sort_reverse
        self.sort_column_index = col_index
        self.sort_process_list()

    def auto_update(self):
        self.update_process_list()
        self.root.after(5000, self.auto_update)

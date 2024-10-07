import psutil
import tkinter as tk
from tkinter import ttk

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("800x600")  # Tamanho da janela
        self.root.configure(bg="#2E2E2E")  # Cor de fundo

        # Inicializa os atributos para ordenação
        self.sort_column_index = None
        self.sort_reverse = False

        # Criação do Frame para a Treeview e Scrollbar
        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuração da tabela
        self.tree = ttk.Treeview(frame, columns=("PID", "Nome do Processo", "Prioridade", "Uso da CPU (%)", "Estado", "Espaço de Memória (MB)"), show="headings")
        
        # Personalizando a aparência da Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#F0F0F0", foreground="#000000", rowheight=25, fieldbackground="#F0F0F0")
        style.map("Treeview", background=[("selected", "#0078D7")])  # Cor de seleção

        # Configuração das colunas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, anchor="center")  # Centraliza os valores nas colunas

        # Criação da Scrollbar
        self.scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Posiciona a Treeview e a Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botão para atualizar a lista de processos
        self.refresh_button = tk.Button(root, text="Atualizar", command=self.update_process_list, bg="#0078D7", fg="white", font=("Arial", 12))
        self.refresh_button.pack(pady=10)

        # Inicializa a lista de processos
        self.process_list = []
        self.update_process_list()

        # Atualiza automaticamente a lista a cada 5 segundos
        self.auto_update()

    def update_process_list(self):
        # Limpa a árvore existente
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Obtém a lista de processos
        self.process_list = []
        for proc in psutil.process_iter(attrs=['pid', 'name', 'nice', 'cpu_percent', 'status', 'memory_info']):
            try:
                priority = "Baixa"  # Padrão
                if proc.info['nice'] is not None:  # Verifica se 'nice' não é None
                    if proc.info['nice'] == 32:
                        priority = "Média" 
                    elif proc.info['nice'] == 64:
                        priority = "Alta"

                memory_mb = round(proc.info['memory_info'].rss / (1024 * 1024), 2)  # Converte bytes para MB
                cpu_usage = proc.info['cpu_percent']  # Uso da CPU já está em %
                state = proc.info['status']  # Estado do processo

                # Adiciona o processo à lista com o nome do processo
                self.process_list.append((proc.info['pid'], proc.info['name'], priority, cpu_usage, state, memory_mb))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue  # Ignora processos que não podem ser acessados

        # Atualiza a árvore com novos dados
        for process in self.process_list:
            self.tree.insert("", "end", values=process)

        self.sort_process_list()  # Ordena a lista após a atualização

        # Atualiza o título com a quantidade total de processos
        total_processes = len(self.process_list)
        self.root.title(f"Gerenciador de Tarefas - Total de Processos: {total_processes}")

    def sort_process_list(self):
        # Ordena a lista de processos se uma coluna estiver selecionada
        if self.sort_column_index is not None:
            self.process_list.sort(key=lambda x: x[self.sort_column_index], reverse=self.sort_reverse)

            # Limpa e reinserir a lista de processos na árvore
            for i in self.tree.get_children():
                self.tree.delete(i)

            for process in self.process_list:
                self.tree.insert("", "end", values=process)

    def sort_column(self, column):
        # Ordena a coluna clicada
        col_index = self.tree["columns"].index(column)
        self.sort_reverse = not self.sort_reverse  # Inverte a ordem de classificação
        self.sort_column_index = col_index  # Armazena o índice da coluna a ser ordenada
        self.sort_process_list()  # Chama a função de ordenação

    def auto_update(self):
        self.update_process_list()  # Atualiza a lista de processos
        self.root.after(5000, self.auto_update)  # Agenda a próxima atualização em 5000 ms (5 segundos)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

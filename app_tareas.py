import tkinter as tk
from tkinter import ttk, messagebox

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Tareas")
        self.root.geometry("650x550")
        self.root.configure(bg='#2c3e50')  # Fondo oscuro

        # Inicializamos la lista de tareas
        self.task_list = []

        # Estilo avanzado
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Helvetica", 12), rowheight=30, background="#34495e", fieldbackground="#34495e", foreground="white")
        style.configure("Treeview.Heading", font=("Helvetica Bold", 14), background="#1abc9c", foreground="white")
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.map("TButton", background=[('active', '#16a085')])

        # Título
        self.title_label = tk.Label(root, text="GESTIÓN DE TAREAS", font=("Helvetica Bold", 20), bg='#2c3e50', fg="white")
        self.title_label.pack(pady=10)

        # Marco para tareas y botones
        main_frame = tk.Frame(root, bg='#2c3e50')
        main_frame.pack(pady=10, fill="both", expand=True)

        # Panel de entrada y lista
        left_frame = tk.Frame(main_frame, bg='#2c3e50')
        left_frame.pack(side="left", padx=10, fill="both", expand=True)

        # Configuración de la entrada para añadir tareas
        self.entry = tk.Entry(left_frame, font=("Helvetica", 14), width=40, borderwidth=2, relief="flat", bg="#F0F8FF", fg="black")
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.add_task)  # Atajo para añadir tareas

        # Configuración del Treeview para mostrar las tareas
        self.task_box = ttk.Treeview(left_frame, height=12)
        self.task_box.pack(pady=10, fill="both", expand=True)
        self.task_box["columns"] = ("Task")
        self.task_box.column("#0", width=0, stretch=tk.NO)
        self.task_box.column("Task", anchor=tk.W, width=400)
        self.task_box.heading("Task", text="Tareas", anchor=tk.W)

        # Panel de botones (Lateral derecho)
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(side="right", padx=10, fill="y")

        add_button = ttk.Button(button_frame, text="Añadir Tarea", command=self.add_task, style="TButton")
        add_button.pack(pady=10, fill="x")

        complete_button = ttk.Button(button_frame, text="Marcar Completada", command=self.complete_task, style="TButton")
        complete_button.pack(pady=10, fill="x")

        delete_button = ttk.Button(button_frame, text="Eliminar Tarea", command=self.delete_task, style="TButton")
        delete_button.pack(pady=10, fill="x")

        # Enlace de eventos de teclado
        root.bind("<c>", self.handle_complete_task)  # Atajo "c minuscula" para completar tarea
        root.bind("<C>", self.handle_complete_task)  # Atajo "C mayuscula" para completar tarea
        root.bind("<d>", self.handle_delete_task)  # Atajo "d minuscula" para eliminar tarea
        root.bind("<D>", self.handle_delete_task)  # Atajo "D mayuscula" para eliminar tarea
        root.bind("<Delete>", self.handle_delete_task)  # Atajo "Delete" para eliminar tarea
        root.bind("<Escape>", lambda e: root.quit())  # Atajo "Escape" para cerrar

    # Función para añadir una tarea
    def add_task(self, event=None):
        task = self.entry.get()
        if task:
            self.task_list.append({"task": task, "completed": False})
            self.entry.delete(0, tk.END)
            self.update_task_list()
        else:
            messagebox.showwarning("Entrada vacía", "No puedes añadir una tarea vacía.")

    # Función para marcar una tarea como completada
    def complete_task(self):
        selected_task = self.task_box.focus()
        if selected_task:
            index = int(self.task_box.index(selected_task))
            self.task_list[index]["completed"] = True
            self.update_task_list()
        else:
            messagebox.showwarning("No seleccionada", "Selecciona una tarea para marcar como completada.")

    # Función para eliminar una tarea
    def delete_task(self):
        selected_task = self.task_box.focus()
        if selected_task:
            index = int(self.task_box.index(selected_task))
            del self.task_list[index]
            self.update_task_list()
        else:
            messagebox.showwarning("No seleccionada", "Selecciona una tarea para eliminar.")

    # Manejo de atajo de teclado para completar una tarea
    def handle_complete_task(self, event):
        if self.task_box.focus():
            self.complete_task()

    # Manejo de atajo de teclado para eliminar una tarea
    def handle_delete_task(self, event):
        if self.task_box.focus():
            self.delete_task()

    # Actualizar la lista de tareas visualmente con colores de fondo
    def update_task_list(self):
        self.task_box.delete(*self.task_box.get_children())
        for index, task in enumerate(self.task_list):
            task_id = self.task_box.insert("", tk.END, text="", values=(task["task"],))
            if task["completed"]:
                self.task_box.item(task_id, tags=("completed",))
            else:
                self.task_box.item(task_id, tags=("pending",))

        # Configuramos los colores de las tareas
        self.task_box.tag_configure("completed", background="lightgreen", font=("Helvetica Italic", 12))
        self.task_box.tag_configure("pending", background="lightcoral", font=("Helvetica", 12))

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Config ----------
WINDOW_W = 1080
WINDOW_H = 720
# ----------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Seu Cantinho")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.resizable(False, False)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Screen in (LoginScreen, CreateUserScreen):#, MenuScreen, BookingScreen):
            frame = Screen(container, self)
            self.frames[Screen] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginScreen)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


# ---------- Login ----------
class LoginScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # centraliza
        frame = ttk.Frame(self, padding="20")
        frame.place(relx=0.5, rely=0.45, anchor="center")

        # fonte e titulo
        ttk.Label(frame, text="Login", font=("Arial", 32,)).pack(pady=10)
        
        # user input
        self.username_entry = self.createInput(frame, "Usuário")

        # senha input
        self.password_entry = self.createInput(frame, "Senha")
        self.password_entry.config(show="*")

        # Botão de login
        ttk.Button(frame, text="Criar Novo", command=lambda: controller.show_frame(CreateUserScreen)).pack(side="left", padx=5)
        ttk.Button(frame, text="Entrar", command=self.login).pack(side='right',padx=20, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin":
            messagebox.showinfo("Login", "Login realizado com sucesso!")
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos!")

    def createInput(self, frame, text):
        f = ttk.Frame(frame)
        f.pack(fill="x", pady=5, expand=True)
        entry = ttk.Entry(f)

        ttk.Label(f, text=text, anchor="w").pack(anchor="center")
        entry.pack(fill="x", expand=True)
        return entry

class CreateUserScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = ttk.Frame(self, padding="20")
        frame.place(relx=0.5, rely=0.45, anchor="center")

        ttk.Label(frame, text="Criar Usuário", font=("Arial", 32)).pack(pady=10)

        self.new_username = self.createInput(frame, "Novo Usuário")
        self.new_password = self.createInput(frame, "Nova Senha")
        self.new_password.config(show="*")
        self.is_admin = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Privilégios Administrativos", variable=self.is_admin).pack(pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20, fill="x")
        ttk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame(LoginScreen)).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Criar", command=self.create_user).pack(side="right", padx=5)


    def createInput(self, frame, text):
        f = ttk.Frame(frame)
        f.pack(fill="x", pady=5)
        entry = ttk.Entry(f)
        ttk.Label(f, text=text, anchor="w").pack(anchor="center")
        entry.pack(fill="x", expand=True)
        return entry

    def create_user(self):
        username = self.new_username.get()
        password = self.new_password.get()
        if username and password:
            messagebox.showinfo("Criar Usuário", f"Usuário '{username}' criado com sucesso!")
            self.controller.show_frame(LoginScreen)
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

if __name__ == "__main__":
    app = App()
    app.mainloop()

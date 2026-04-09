import tkinter as tk
from tkinter import scrolledtext
import cv2
from PIL import Image, ImageTk

class ConsoleUI:
    def __init__(self, event_bus):
        self.event_bus = event_bus

        self.root = tk.Tk()
        self.root.title("Asistencia Médica IA PRO")
        self.root.geometry("900x600")

        # Layout principal
        self.left_frame = tk.Frame(self.root, width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root, width=500)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Chat
        self.chat = scrolledtext.ScrolledText(self.left_frame, wrap=tk.WORD)
        self.chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.left_frame)
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        self.button = tk.Button(self.left_frame, text="Enviar", command=self.send_message)
        self.button.pack(pady=5)

        # Estado
        self.status = tk.Label(self.left_frame, text="Estado: Activo", fg="green")
        self.status.pack(pady=5)

        # Cámara
        self.camera_label = tk.Label(self.right_frame)
        self.camera_label.pack()

        self.cap = cv2.VideoCapture(0)

        self.update_camera()

    def send_message(self, event=None):
        text = self.entry.get()
        if text:
            self.chat.insert(tk.END, f"Tú: {text}\n")
            self.chat.see(tk.END)
            self.entry.delete(0, tk.END)
            self.event_bus.publish("voice_input", text)

    def display(self, text):
        self.chat.insert(tk.END, "\n" + "="*50 + "\n")
        self.chat.insert(tk.END, "Respuesta de IA:\n\n")
        self.chat.insert(tk.END, text + "\n")
        self.chat.insert(tk.END, "="*50 + "\n")
        self.chat.see(tk.END)
    
    def _safe_display(self, text):
        self.chat.insert(tk.END, f"IA: {text}\n")
        self.chat.see(tk.END)

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)

        self.root.after(10, self.update_camera)

    def run(self):
        self.root.mainloop()
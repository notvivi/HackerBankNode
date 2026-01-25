import customtkinter as ctk
from tkinter import filedialog
import json

class FrontPage(ctk.CTkFrame):
    def __init__(self, master, on_config_saved, config_path):
        super().__init__(master)
        self.on_config_saved = on_config_saved
        self.config_path = config_path

        self.log_file = ctk.StringVar()
        self.port = ctk.StringVar(value="65525")
        self.timeout = ctk.StringVar(value="5")

        ctk.CTkLabel(self, text="LOG file").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.log_file, width=400).pack()
        ctk.CTkButton(self, text="Select file", command=self.select_file).pack(pady=5)

        ctk.CTkLabel(self, text="Port").pack(pady=5)
        ctk.CTkOptionMenu(
            self,
            values=[str(p) for p in range(65525, 65536)],
            variable=self.port
        ).pack()

        ctk.CTkLabel(self, text="Timeout").pack(pady=5)
        ctk.CTkOptionMenu(
            self,
            values=["5", "10", "30", "60"],
            variable=self.timeout
        ).pack()

        ctk.CTkButton(self, text="Save configuration", command=self.save).pack(pady=15)

        ctk.CTkButton(
            self,
            text="Exit",
            command=master.destroy
        ).pack(pady=20)

    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.log_file.set(path)

    def save(self):
        data = {
            "log_file": self.log_file.get(),
            "port": int(self.port.get()),
            "timeout": int(self.timeout.get())
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self.on_config_saved(data)


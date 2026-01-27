#Author: Tomanová Vilma
import ipaddress

import customtkinter as ctk
from tkinter import filedialog, messagebox
import json

class FrontPage(ctk.CTkFrame):
    """
    Class for Front Page
    """
    def __init__(self, master, on_config_saved, config_path):
        super().__init__(master)
        self.on_config_saved = on_config_saved
        self.config_path = config_path

        self.log_file = ctk.StringVar()
        self.ip_network = ctk.StringVar(value="192.168.1.0")
        self.ip_mask = ctk.StringVar(value="24")
        self.port = ctk.StringVar(value="65525")
        self.timeout = ctk.StringVar(value="5")

        ctk.CTkLabel(self, text="LOG file").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.log_file, width=400).pack()
        ctk.CTkButton(self, text="Select file", command=self.select_file).pack(pady=5)

        ctk.CTkLabel(self, text="Ip Network").pack(pady=5)
        ctk.CTkOptionMenu(
            self,
            values=["5", "10", "30", "60"],
            variable=self.timeout
        ).pack()

        ctk.CTkLabel(self, text="IP Network").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.ip_network, width=200).pack()

        ctk.CTkLabel(self, text="IP Mask").pack(pady=5)
        ctk.CTkOptionMenu(
            self,
            values=[str(p) for p in range(1, 33)],
            variable=self.ip_mask
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
        """
        Opens file explorer for selecting a file.
        """
        path = filedialog.askopenfilename()
        if path:
            self.log_file.set(path)

    def save(self):
        """
        Saves data from ui to config file.
        """
        network = self.validate_network_ip()
        if not network:
            return

        data = {
            "log_file": self.log_file.get(),
            "port": int(self.port.get()),
            "timeout": int(self.timeout.get()),
            "ip_network": self.ip_network.get(),
            "ip_mask": int(self.ip_mask.get())
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self.on_config_saved(data)

    def validate_network_ip(self):
        """
        Validates network ip address.
        """
        try:
            network = ipaddress.IPv4Network(
                f"{self.ip_network.get()}/{self.ip_mask.get()}",
                strict=True
            )
            return network
        except ValueError:
            messagebox.showwarning(
                title="Invalid IP",
                message="Inserted IP is invalid.",
                icon="warning"
            )
            return None


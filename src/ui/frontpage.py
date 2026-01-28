# Author: Tomanová Vilma
import ipaddress
import customtkinter as ctk
from tkinter import filedialog, messagebox
import json


class FrontPage(ctk.CTkFrame):
    """
    Class for Front Page with centered grid layout
    """
    def __init__(self, master, on_config_saved, config_path):
        super().__init__(master)
        self.on_config_saved = on_config_saved
        self.config_path = config_path

        # Variables
        self.log_file = ctk.StringVar()
        self.ip_network = ctk.StringVar(value="192.168.1.0")
        self.ip_mask = ctk.StringVar(value="24")
        self.port = ctk.StringVar(value="65525")
        self.timeout = ctk.StringVar(value="5")

        # Center frame container
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0, padx=20, pady=20)

        # LOG file
        ctk.CTkLabel(center_frame, text="LOG file:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ctk.CTkEntry(center_frame, textvariable=self.log_file, width=300).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(center_frame, text="Select file", command=self.select_file).grid(row=0, column=2, padx=5, pady=5)

        # IP Network
        ctk.CTkLabel(center_frame, text="IP Network:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ctk.CTkEntry(center_frame, textvariable=self.ip_network, width=300).grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkLabel(
            center_frame,
            text="(Network that will be scanned for hacking/robbing.)",
            text_color="gray"
        ).grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # IP Mask
        ctk.CTkLabel(center_frame, text="IP Mask:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        mask_container = ctk.CTkFrame(center_frame, fg_color="transparent")
        mask_container.grid(row=2, column=1, columnspan=2, sticky="w")

        ctk.CTkOptionMenu(mask_container, values=[str(p) for p in range(16, 33)], variable=self.ip_mask,
                          width=100).pack(side="left", padx=5)
        ctk.CTkLabel(mask_container, text="(Mask defining the size of IP network.)", text_color="gray").pack(
            side="left", padx=5)

        # Port
        ctk.CTkLabel(center_frame, text="Port:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        port_container = ctk.CTkFrame(center_frame, fg_color="transparent")
        port_container.grid(row=3, column=1, columnspan=2, sticky="w")

        ctk.CTkOptionMenu(port_container, values=[str(p) for p in range(65525, 65536)], variable=self.port,
                          width=100).pack(side="left", padx=5)
        ctk.CTkLabel(port_container, text="(TCP port on which the bank node listens.)", text_color="gray").pack(
            side="left", padx=5)

        # Timeout
        ctk.CTkLabel(center_frame, text="Timeout:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        timeout_container = ctk.CTkFrame(center_frame, fg_color="transparent")
        timeout_container.grid(row=4, column=1, columnspan=2, sticky="w")

        ctk.CTkOptionMenu(timeout_container, values=["5", "10", "30", "60"], variable=self.timeout, width=100).pack(
            side="left", padx=5)
        ctk.CTkLabel(timeout_container, text="(Global timeout in seconds.)", text_color="gray").pack(side="left",
                                                                                                     padx=5)

        # Save button
        ctk.CTkButton(center_frame, text="Save configuration", command=self.save) \
            .grid(row=5, column=0, columnspan=3, pady=15, sticky="we", padx=5)

        # Exit button
        ctk.CTkButton(center_frame, text="Exit", command=master.destroy) \
            .grid(row=6, column=0, columnspan=3, pady=10, sticky="we", padx=5)

        # Center the frame in the parent
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def select_file(self):
        """
        Used for selecting a file.
        """
        path = filedialog.askopenfilename()
        if path:
            self.log_file.set(path)

    def save(self):
        """
        Saving into config.json file.
        """
        network = self.validate_network_ip()
        if not network:
            return

        sqlite_path = "db/hackerbank.db"
        data = {
            "log_file": self.log_file.get(),
            "port": int(self.port.get()),
            "timeout": int(self.timeout.get()),
            "ip_network": self.ip_network.get(),
            "ip_mask": int(self.ip_mask.get()),
            "database": {"sqlite_path": sqlite_path}
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self.on_config_saved(data)

    def validate_network_ip(self):
        """
        Validates network IP address.
        """
        try:
            network = ipaddress.IPv4Network(f"{self.ip_network.get()}/{self.ip_mask.get()}", strict=True)
            return network
        except ValueError:
            messagebox.showwarning(title="Invalid IP", message="Inserted IP is invalid.", icon="warning")
            return None

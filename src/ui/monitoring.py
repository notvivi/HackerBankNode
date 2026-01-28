#Author: Tomanová Vilma
from datetime import datetime
import threading
import customtkinter as ctk
import socket

from tcp_client import send_tcp_command
from parser import parse_command_responses

class MonitoringPage(ctk.CTkFrame):
    """
    Class for monitoring page.
    """
    def __init__(self, master, on_back, config):
        super().__init__(master)
        self.on_back = on_back
        self.config = config

        ctk.CTkLabel(self, text="Monitoring Page", font=("Arial", 24)).grid(
            row=0, column=0, columnspan=4, pady=20, sticky="nsew"
        )
        ctk.CTkLabel(self, text="Bank IP:").grid(row=1, column=0, sticky="e", padx=5)
        self.bank_ip_label = ctk.CTkLabel(self, text="...")
        self.bank_ip_label.grid(row=1, column=1, sticky="w", padx=5)

        ctk.CTkLabel(self, text="Bank port:").grid(row=2, column=0, sticky="e", padx=5)
        self.bank_port_label = ctk.CTkLabel(self, text="...")
        self.bank_port_label.grid(row=2, column=1, sticky="w", padx=5)

        ctk.CTkLabel(self, text="Last refreshed:").grid(row=3, column=0, sticky="e", padx=5)
        self.last_refreshed_label = ctk.CTkLabel(self, text="...")
        self.last_refreshed_label.grid(row=3, column=1, sticky="w", padx=5)

        ctk.CTkLabel(self, text="Total balance:").grid(row=1, column=2, sticky="e", padx=5)
        self.balance_label = ctk.CTkLabel(self, text="...")
        self.balance_label.grid(row=1, column=3, sticky="w", padx=5)

        ctk.CTkLabel(self, text="Total clients:").grid(row=2, column=2, sticky="e", padx=5)
        self.clients_label = ctk.CTkLabel(self, text="...")
        self.clients_label.grid(row=2, column=3, sticky="w", padx=5)

        ctk.CTkLabel(self, text="Active clients:").grid(row=3, column=2, sticky="e", padx=5)
        self.active_clients_label = ctk.CTkLabel(self, text="...")
        self.active_clients_label.grid(row=3, column=3, sticky="w", padx=5)

        ctk.CTkButton(self, text="Refresh Data", command=self.start_monitoring_thread).grid(row=4, column=0,
                                                                                            columnspan=2, pady=20,
                                                                                       sticky="we", padx=5)
        ctk.CTkButton(self, text="Return to Configuration", command=self.on_back).grid(row=4, column=2, pady=20,
                                                                                       sticky="we", padx=5)
        ctk.CTkButton(self, text="Exit", command=self.master.destroy).grid(row=4, column=3, pady=20, sticky="we",
                                                                           padx=5)

        for col in range(4):
            self.grid_columnconfigure(col, weight=1)

    def get_local_ip(self):
        """
        Return: Socket IP address.
        """
        return socket.gethostbyname(socket.gethostname())

    def start_monitoring_thread(self):
        """
        Starts monitoring thread.
        """
        thread = threading.Thread(target=self.start_monitoring)
        thread.daemon = True
        thread.start()

    def start_monitoring(self):
        """
        Starts monitoring
        """
        host = self.get_local_ip()
        port = int(self.master.app_config.get("port", 65530))
        timeout = self.master.app_config.get("timeout", 5)

        self.bank_ip_label.configure(text=f"{host}")
        self.bank_port_label.configure(text=f"{port}")

        commands = ["BA", "BN", "CC"]
        results = {}

        for cmd in commands:
            raw = send_tcp_command(host, port, cmd, timeout)
            results[cmd] = parse_command_responses(raw, cmd)

        self.after(0, lambda: self.update_ui(results, host, port))

    def update_ui(self, data, ip, port):
        """
        Updates UI with recent data from server response.
        """
        ba = data.get('BA', {})
        if isinstance(ba, dict):
            ba_value = ba.get('BA', 0)
        else:
            ba_value = ba
        self.balance_label.configure(text=str(ba_value))

        bn = data.get('BN', {})
        if isinstance(bn, dict):
            bn_value = bn.get('BN', 0)
        else:
            bn_value = bn or 0
        try:
            total_clients = max(0, int(bn_value) - 1)
        except (TypeError, ValueError):
            total_clients = "ERROR"
        self.clients_label.configure(text=str(total_clients))

        self.bank_ip_label.configure(text=str(ip))
        self.bank_port_label.configure(text=str(port))
        self.last_refreshed_label.configure(
            text=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        cc = data.get('CC', {})
        if isinstance(cc, dict):
            cc_value = cc.get('CC', 0)
        else:
            cc_value = cc or 0
        try:
            active_clients = max(0, int(cc_value) - 1)
        except (TypeError, ValueError):
            active_clients = "ERROR"

        self.active_clients_label.configure(text=str(active_clients))


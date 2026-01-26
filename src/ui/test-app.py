import os
import json
import sys
import customtkinter as ctk
from frontpage import FrontPage
from monitoring import MonitoringPage
from tkinter import messagebox
import resource_path

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_path, "..", "lib"))
sys.path.insert(0, os.path.join(base_path, "lib"))


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_PATH = resource_path.resource_path("src/config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def is_config_ok(cfg):
        try:
            log_ok = isinstance(cfg.get("log_file"), str) and len(cfg.get("log_file").strip()) > 0
            port_ok = isinstance(cfg.get("port"), int) and 65525 <= cfg.get("port") <= 65535
            timeout_ok = isinstance(cfg.get("timeout"), int) and cfg.get("timeout") > 0
            return log_ok and port_ok and timeout_ok
        except TypeError:
            return False

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hacker Bank Node")
        self.geometry("600x500")

        self.app_config = load_config()
        self.frontpage = FrontPage(self, self.update_config_and_monitoring, CONFIG_PATH)
        self.monitoring = None

        if is_config_ok(self.app_config):
            self.after(0, self.open_monitoring)
        else:
            self.frontpage.pack(fill="both", expand=True)

    def update_config_and_monitoring(self, new_config):
        self.app_config = new_config

        if not is_config_ok(self.app_config):
            messagebox.showwarning(
                title="Configuration error",
                message="Configuration is incomplete. Please fill all required fields.",
            )
            return
        else:
            self.open_monitoring()
    def open_monitoring(self):
        self.frontpage.pack_forget()

        if self.monitoring is None:
            self.monitoring = MonitoringPage(self, self.open_frontpage)

        self.monitoring.pack(fill="both", expand=True)

    def open_frontpage(self):
        if self.monitoring:
            self.monitoring.pack_forget()
        self.frontpage.pack(fill="both", expand=True)

if __name__ == "__main__":
    App().mainloop()
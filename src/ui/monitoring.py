#Author: Tomanová Vilma

import customtkinter as ctk

class MonitoringPage(ctk.CTkFrame):
    """
    Class for Monitoring Page
    """
    def __init__(self, master,on_back):
        super().__init__(master)
        self.on_back = on_back

        ctk.CTkLabel(
            self,
            text="Monitoring Page",
            font=("Arial", 24)
        ).pack(pady=30)

        self.balance_label = ctk.CTkLabel(self, text="Total balance: ...")
        self.balance_label.pack(pady=10)

        ctk.CTkButton(self, text="Return to Configuration", command=self.on_back).pack(side="left", padx=10)
        ctk.CTkButton(self, text="Exit", command=master.destroy).pack(pady=20)


import tkinter as tk

class DataAnalyserModule:
    def __init__(self, parent_frame, user_data, is_admin):
        self.parent = parent_frame
        self.user_data = user_data
        self.is_admin = is_admin
        self.build_ui()

    def build_ui(self):
        for widget in self.parent.winfo_children(): widget.destroy()
        role = "ADMIN" if self.is_admin else "USER"
        tk.Label(self.parent, text="SYSTEM DASHBOARD", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.parent, text=f"Welcome, {self.user_data[1]} | Role: {role}").pack()
        tk.Frame(self.parent, width=300, height=100, bg="#f0f0f0", bd=1, relief="sunken").pack(pady=20)
        tk.Label(self.parent, text="[ Feature Skeleton Content Area ]", fg="gray").pack()
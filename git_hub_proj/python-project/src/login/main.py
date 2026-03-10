import tkinter as tk
from tkinter import messagebox, simpledialog
from .database import DatabaseManager
from .mailer import Mailer
from .analyser import DataAnalyserModule
import sys

from login.database import DatabaseManager
from login.mailer import Mailer
from login.analyser import DataAnalyserModule

class SystemApp:
    def __init__(self, root, skip_dashboard=False):
        self.root = root
        self.root.title("Secure OOP System")
        self.root.geometry("500x650")
        self.db = DatabaseManager()
        self.current_user = None
        self.is_admin = False
        self.skip_dashboard = skip_dashboard

        self.check_initial_setup()
        self.show_login_screen()

    def check_initial_setup(self):
        """Forces the creation of an admin and SMTP config. Exits if cancelled."""
        if not self.db.get_all_users():
            messagebox.showinfo("First Run", "System uninitialized. Setup is REQUIRED.")
            
            s_email = simpledialog.askstring("Setup", "Sender Email:")
            s_pwd = simpledialog.askstring("Setup", "App Password:", show="*")
            uname = simpledialog.askstring("Setup", "Admin Username:")
            pwd = simpledialog.askstring("Setup", "Admin Password:", show="*")

            if not all([s_email, s_pwd, uname, pwd]):
                messagebox.showerror("Fatal Error", "Setup incomplete. Exiting...")
                return

            self.db.cursor.execute("INSERT INTO settings VALUES ('sys_email', ?), ('sys_pwd', ?)", (s_email, s_pwd))
            self.db.add_user("Admin", uname, "admin@sys.com", pwd, is_admin=1)
            

            self.db.conn.commit()
            messagebox.showinfo("Success", "System Ready.")

    def get_mailer(self):
        self.db.cursor.execute("SELECT value FROM settings WHERE key='sys_email'")
        e = self.db.cursor.fetchone()[0]
        self.db.cursor.execute("SELECT value FROM settings WHERE key='sys_pwd'")
        p = self.db.cursor.fetchone()[0]
        return Mailer(e, p)

    def clear_screen(self):
        for w in self.root.winfo_children(): w.destroy()

    def show_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="System Login", font=("Arial", 18, "bold")).pack(pady=30)
        tk.Label(self.root, text="Username").pack()
        u_ent = tk.Entry(self.root); u_ent.pack(pady=5)
        tk.Label(self.root, text="Password").pack()
        p_ent = tk.Entry(self.root, show="*"); p_ent.pack(pady=5)
        tk.Button(self.root, text="Login", width=15, command=lambda: self.handle_login(u_ent.get(), p_ent.get())).pack(pady=10)
        tk.Button(self.root, text="Create New Account", fg="blue", command=self.show_registration).pack()
        tk.Button(self.root, text="Quit", bg="#ffcccc", command=self.root.destroy).pack(side="bottom", pady=20)

    def handle_login(self, u, p):
        user = self.db.authenticate(u, p)
        if user:
            self.current_user = user
            self.is_admin = bool(user[5])
            if self.skip_dashboard:
                self.root.destroy()
            else:
                self.show_dashboard()
        else: messagebox.showerror("Error", "Invalid Credentials")

    def show_registration(self):
        self.clear_screen()
        tk.Label(self.root, text="New Registration", font=("Arial", 14)).pack(pady=20)
        fields = {}
        for f in ["Name", "Username", "Email", "Password"]:
            tk.Label(self.root, text=f).pack()
            e = tk.Entry(self.root, show="*" if f=="Password" else "")
            e.pack(); fields[f] = e

        def do_reg():
            email = fields["Email"].get()
            if email != "": #Edit 3 skip email verification if none set
                token = self.get_mailer().send_confirmation(email, "Registration")
                if not token or simpledialog.askstring("Verify", f"Code sent to {email}:") != token:
                    messagebox.showerror("Error", "Failed Verification"); return
            if self.db.add_user(fields["Name"].get(), fields["Username"].get(), email, fields["Password"].get()):
                messagebox.showinfo("Success", "Account created!"); self.show_login_screen()
            else: messagebox.showerror("Error", "Username/Email exists.")

        tk.Button(self.root, text="Register", command=do_reg).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_login_screen).pack()

    def show_dashboard(self):
        self.clear_screen()
        content = tk.Frame(self.root, bd=1, relief="sunken")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        DataAnalyserModule(content, self.current_user, self.is_admin)

        nav = tk.Frame(self.root); nav.pack(fill="x", side="bottom", pady=20)
        if self.is_admin:
            tk.Button(nav, text="Manage Users", command=self.show_admin_panel).pack(side="left", padx=5)
        
        tk.Button(nav, text="Delete My Account", fg="red", command=self.handle_self_deletion).pack(side="left", padx=5)
        tk.Button(nav, text="Logout", command=self.handle_logout).pack(side="left", padx=5)
        tk.Button(nav, text="Quit", bg="#f44336", fg="white", command=self.root.quit).pack(side="right", padx=10)

    def handle_self_deletion(self):
        email = self.current_user[3]
        if email == "": #Edit 2 skip email verification if none set
                    if messagebox.askyesno("Confirm", "Delete your account forever?"):
                        self.db.delete_user(self.current_user[0])
                        self.show_login_screen()
        else:
            token = self.get_mailer().send_confirmation(self.current_user[3], "Account Deletion")
            if token and simpledialog.askstring("Confirm", "Enter deletion code:") == token:
                if messagebox.askyesno("Confirm", "Delete your account forever?"):
                    self.db.delete_user(self.current_user[0])
                    self.show_login_screen()
    def show_admin_panel(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Console", font=("Arial", 12, "bold")).pack(pady=10)
        for u in self.db.get_all_users():
            f = tk.Frame(self.root, relief="ridge", bd=1); f.pack(fill="x", padx=10, pady=2)
            #tk.Label(f, text=f"{u[2]} | {u[3]}").pack(side="left") #View ID along with username and email 
            tk.Label(f,text=f"ID: {u[0]}   Name: {u[1]}   Username: {u[2]}   Email: {u[3]}").pack(side="left")
            if u[0] != self.current_user[0]:
                tk.Button(f, text="Delete", command=lambda uid=u[0]: [self.db.delete_user(uid), self.show_admin_panel()]).pack(side="right")
                tk.Button(f, text="Reset", command=lambda uid=u[0]: self.admin_reset(uid)).pack(side="right")
        tk.Button(self.root, text="Back", command=self.show_dashboard).pack(pady=10)

    def admin_reset(self, uid):
        new_p = simpledialog.askstring("Reset", "New Password:", show="*")
        if new_p: self.db.reset_password(uid, new_p); messagebox.showinfo("OK", "Updated.")

    def handle_logout(self):
        self.clear_screen()
        tk.Label(self.root, text="Logging out...\nGoodbye!", font=("Arial", 14), fg="green").pack(expand=True)
        self.root.after(2000, sys.exit)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemApp(root)
    root.mainloop()

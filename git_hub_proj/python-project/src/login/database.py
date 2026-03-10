import sqlite3
import hashlib
import pathlib

class DatabaseManager:
    def __init__(self, db_name="system.db"):
        # TODO NOTE This does not work! It still spits the database into the source code and not the user_database folder (where it belongs)
        path_here = pathlib.Path(__file__)
        path_db = path_here.parent / db_name

        self.conn = sqlite3.connect(path_db)
        self.cursor = self.conn.cursor()
        self.setup_db()

    def setup_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, user_name TEXT UNIQUE, email TEXT UNIQUE,
            password TEXT, is_admin INTEGER DEFAULT 0)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
        self.conn.commit()

    def hash_pwd(self, pwd):
        return hashlib.sha256(pwd.encode()).hexdigest()

    def add_user(self, name, uname, email, pwd, is_admin=0):
        try:
            hashed = self.hash_pwd(pwd)
            self.cursor.execute("INSERT INTO users (name, user_name, email, password, is_admin) VALUES (?,?,?,?,?)",
                               (name, uname, email, hashed, is_admin))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError: return False

    # --- CRITICAL: THE AUTHENTICATE METHOD ---
    def authenticate(self, uname, pwd):
        hashed = self.hash_pwd(pwd)
        self.cursor.execute("SELECT * FROM users WHERE user_name=? AND password=?", (uname, hashed))
        return self.cursor.fetchone()

    # --- CRITICAL: THE RESET METHOD ---
    def reset_password(self, user_id, new_password):
        hashed = self.hash_pwd(new_password)
        self.cursor.execute("UPDATE users SET password=? WHERE userID=?", (hashed, user_id))
        self.conn.commit()
        return True

    def delete_user(self, uid):
        self.cursor.execute("DELETE FROM users WHERE userID=?", (uid,))
        self.conn.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT userID, name, user_name, email, is_admin FROM users")
        return self.cursor.fetchall()

    # TODO not sure what the format of fetchall is (propably list or tuple)
    def get_user_data(self, userID:str): 
        """ Gets all the data connected to a user (Without PW/PW-hash)"""
        self.cursor.execute(f"SELECT userID, name, user_name, email, is_admin FROM users WHERE userID = {userID}")
        return self.cursor.fetchall()


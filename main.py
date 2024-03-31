import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib


class aiAuthLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login/Register")

        # Center the login window
        self.center_window()

        label_style = {"bg": "#242424", "fg": "white",
                       "font": ("Arial", 16), "pady": 5, "padx": 10}

        # Login elements
        self.login_frame = tk.Frame(self.root, bg="#242424")
        self.login_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.username_label = tk.Label(
            self.login_frame, text="Enter your username", **label_style)
        self.username_label.pack()

        self.username_entry = tk.Entry(
            self.login_frame, width=40, bg="#2E2E2E", fg="white", font=("Arial", 16))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(
            self.login_frame, text="Enter your password", **label_style)
        self.password_label.pack()

        self.password_entry = tk.Entry(
            self.login_frame, width=40, bg="#2E2E2E", fg="white", font=("Arial", 16), show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(
            self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(
            self.login_frame, text="Register", command=self.register_user)
        self.register_button.pack(pady=10)

        label_style = {"bg": "#242424", "fg": "white",
                       "font": ("Arial", 16), "pady": 5, "padx": 10}

        # Prompt elements
        self.prompt_frame = tk.Frame(self.root, bg="#242424")
        self.prompt_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.prompt_label = tk.Label(
            self.prompt_frame, text="Secure a prompt", **label_style)
        self.prompt_label.pack(pady=5)

        self.prompt_entry = tk.Entry(
            self.prompt_frame, width=40, bg="#2E2E2E", fg="white", font=("Arial", 16))
        self.prompt_entry.pack(pady=5)

        self.add_prompt_button = ctk.CTkButton(
            self.prompt_frame, text="Add Prompt", command=self.add_prompt)
        self.add_prompt_button.pack(pady=10)

        # Initially hide the prompt elements
        self.prompt_frame.pack_forget()

        self.create_table()

    def center_window(self):
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate x and y coordinates to center the window
        x = (screen_width - 400) // 2  # 400 is the width of the window
        y = (screen_height - 300) // 2  # 300 is the height of the window

        # Set the window to the center
        self.root.geometry(f"400x300+{x}+{y}")

    def create_table(self):
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                prompt TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
        conn.close()

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))

            conn.commit()
            conn.close()

            self.show_message("User registered successfully!")

        else:
            self.show_message("Please enter both username and password.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute(
                'SELECT * FROM users WHERE username=? AND password=?', (username, hashed_password))
            user = cursor.fetchone()

            conn.close()

            if user:
                self.show_message("Login successful!")

                # Hide login elements after successful login
                self.login_frame.pack_forget()

                # Display the prompt_frame in the same position
                self.prompt_frame.pack(side=tk.LEFT, padx=10, pady=10)

            else:
                self.show_message(
                    "Invalid username or password. Please try again.")

        else:
            self.show_message("Please enter both username and password.")

    def enable_prompt_elements(self):
        # Show elements for adding prompts
        self.prompt_label.pack()
        self.prompt_entry.pack()
        self.add_prompt_button.pack()

    def add_prompt(self):
        username = self.username_entry.get()
        prompt_text = self.prompt_entry.get()
        prompt_text = prompt_text.lower()

        if username and prompt_text:
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()

            # Get user ID based on the username
            cursor.execute(
                'SELECT id FROM users WHERE username=?', (username,))
            user_id = cursor.fetchone()

            if user_id:
                user_id = user_id[0]

                # Insert prompt into the database
                cursor.execute(
                    'INSERT INTO prompts (user_id, prompt) VALUES (?, ?)', (user_id, prompt_text))

                conn.commit()
                conn.close()

                self.show_message("Prompt added successfully!")
            else:
                self.show_message("User not found. Please log in again.")

        else:
            self.show_message("Please enter both username and prompt.")

    def show_message(self, message):
        messagebox.showinfo("Message", message)


if __name__ == "__main__":
    root = ctk.CTk()
    app = aiAuthLogin(root)
    root.mainloop()

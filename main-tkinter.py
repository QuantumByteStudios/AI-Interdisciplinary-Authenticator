import tkinter as tk
from tkinter import scrolledtext, font
import threading
import utils
import bard

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Chat App")
        self.master.geometry("400x600")
        self.master.config(bg="#121212")  # Set background color to dark

        # Configure column and row weights to make the window responsive
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Set the default font to Arial
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial")

        # Create and configure the text widget for displaying messages (read-only)
        self.chat_display = scrolledtext.ScrolledText(
            master, wrap=tk.WORD, width=40, height=25, state=tk.DISABLED, bg="#1E1E1E", fg="white", font=("Arial", 10)
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Allow the scrolled text widget to expand with the window
        self.chat_display.grid_rowconfigure(0, weight=1)
        self.chat_display.grid_columnconfigure(0, weight=1)

        # Create and configure the entry widget for user input
        self.input_entry = tk.Entry(master, width=40, bg="#2E2E2E", fg="white", font=("Arial", 10))
        self.input_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10), ipady=5, ipadx=5)  # Added ipady for internal padding

        # Allow the entry widget to expand horizontally with the window
        self.input_entry.grid_columnconfigure(0, weight=1)

        # Create a button to send messages
        self.send_button = tk.Button(master, text="Send", command=self.send_message, bg="#007BFF", fg="white", font=("Arial", 10))
        self.send_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Create a button to clear chat
        self.clear_chat_button = tk.Button(master, text="Clear Chat", command=self.clear_chat, bg="#DC3545", fg="white", font=("Arial", 10))
        self.clear_chat_button.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # Allow the buttons to expand with the window horizontally
        self.send_button.grid_columnconfigure(0, weight=1)
        self.clear_chat_button.grid_columnconfigure(0, weight=1)

    def send_message(self):
        message = self.input_entry.get()
        if message:
            self.display_message(f"You: {message}")
            self.input_entry.delete(0, tk.END)  # Clear the input field

            # Simulate bot typing in a separate thread
            threading.Thread(target=self.process_bot_response, args=(bard.askBard(message.lower()),)).start()

    def process_bot_response(self, message):
        bot_response = f"Bot: {message}"
        self.display_message(bot_response)

    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)  # Set state to normal to modify the widget
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)  # Set state back to disabled after modifying

    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)  # Set state to normal to modify the widget
        self.chat_display.delete(1.0, tk.END)  # Delete all text in the widget
        self.chat_display.config(state=tk.DISABLED)  # Set state back to disabled after modifying

if __name__ == "__main__":
    utils.clear_screen()
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

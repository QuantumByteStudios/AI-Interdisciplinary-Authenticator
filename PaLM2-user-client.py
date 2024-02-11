import tkinter as tk
import customtkinter as ctk
import threading
import utils
import bard

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generative AI Chat - PaLM 2 - Google AI")
        self.geometry("400x600")
        self.iconbitmap("src/icon/icon.ico")
        self.config(bg="#121212")

        self.option_add("*Font", "Arial")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial")

        # Create a frame for chat display
        self.chat_frame = tk.Frame(bg="#1E1E1E")
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(self.chat_frame, orient="vertical", takefocus=0)
        scrollbar.pack_forget()  # Hide the scrollbar

        # Create and configure the text widget for displaying messages (read-only)
        self.chat_display = tk.Text(
            self.chat_frame,
            wrap=tk.WORD,
            width=40,
            height=25,
            padx=10,
            pady=10,
            state=tk.DISABLED,
            bg="#1E1E1E", fg="white",
            font=("Arial", 14),
            yscrollcommand=scrollbar.set
        )

        self.chat_display.pack(expand=True, fill="both")

        scrollbar.config(command=self.chat_display.yview)

        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        # Create and configure the entry widget for user input
        self.input_entry = tk.Entry(width=40, bg="#2E2E2E", fg="white", font=("Arial", 16))
        self.input_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10), ipady=15, ipadx=15)
        self.input_entry.grid_columnconfigure(0, weight=1)

        # Create a button to send messages
        self.send_button = tk.Button(text="Ask PaLM 2", command=self.send_message, bg="#007BFF", fg="white", font=("Arial", 12))
        self.send_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10, sticky="ew")
        self.send_button.grid_columnconfigure(0, weight=1)

        # Create a button to clear chat
        self.clear_chat_button = tk.Button(text="Clear Chat", command=self.clear_chat, bg="#DC3545", fg="white", font=("Arial", 12))
        self.clear_chat_button.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), ipadx=10, ipady=10, sticky="ew")
        self.clear_chat_button.grid_columnconfigure(0, weight=1)

    # send message to chat display
    def send_message(self):
        message = self.input_entry.get()
        if message:
            self.display_message(f"\nYou: {message}")
            self.input_entry.delete(0, tk.END)

            response = utils.aiInterdisciplinaryAuth(message.lower())

            print(response)

            if response["status"] == "NEGATIVE":
                self.display_message("\nPaLM 2: \nI'm sorry, I cannot respond to that.")
            else:
                threading.Thread(target=self.process_bot_response, args=(bard.askBard(message.lower()),)).start()

    # process bot response
    def process_bot_response(self, message):
        bot_response = f"\nPaLM 2: \n{message}"
        self.display_message(bot_response)

    # display message in chat display
    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)

    # clear chat display
    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    utils.clear_screen()
    app = ChatApp()
    app.mainloop()
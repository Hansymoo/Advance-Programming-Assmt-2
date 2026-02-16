import tkinter as tk
import random

class AlexaJokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("400x400")  # Define a fixed window size
        self.root.config(bg="#f0f4f8")  # Light background color
        self.jokes = self.load_jokes("randomJokes.txt")
        self.current_joke = None

        # Title Label with improved styling
        self.title_label = tk.Label(root, text="Alexa Joke Teller", font=("Helvetica", 20, "bold"), fg="#4A90E2", bg="#f0f4f8")
        self.title_label.pack(pady=30)

        # Joke setup label with larger font
        self.label = tk.Label(root, text="Say: Alexa tell me a joke", font=("Helvetica", 16), wraplength=350, justify="center", bg="#f0f4f8")
        self.label.pack(pady=10)

        # Joke telling button with custom styling
        self.button = tk.Button(root, text="Alexa tell me a joke", command=self.tell_joke, font=("Helvetica", 14), bg="#4A90E2", fg="white", relief="raised", width=20, height=2, bd=0, highlightthickness=0)
        self.button.pack(pady=20)

        # Punchline button
        self.punchline_button = tk.Button(root, text="Show Punchline", command=self.show_punchline, font=("Helvetica", 14), bg="#E94E77", fg="white", relief="raised", width=20, height=2, bd=0, highlightthickness=0)
        self.punchline_button.pack(pady=10)
        self.punchline_button.config(state="disabled")

        # Quit button with new style
        self.quit_button = tk.Button(root, text="Quit", command=root.destroy, font=("Helvetica", 14), bg="#D9534F", fg="white", relief="raised", width=20, height=2, bd=0, highlightthickness=0)
        self.quit_button.pack(pady=30)

    def load_jokes(self, filename):
        jokes = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if '?' in line:
                        setup, punch = line.strip().split('?', 1)
                        jokes.append((setup + '?', punch.strip()))
        except FileNotFoundError:
            jokes = [("File not found!", "Please add randomJokes.txt")]
        return jokes

    def tell_joke(self):
        self.current_joke = random.choice(self.jokes)
        self.label.config(text=f"Alexa: {self.current_joke[0]}")
        self.punchline_button.config(state="normal")

    def show_punchline(self):
        if self.current_joke:
            self.label.config(text=f"Alexa: {self.current_joke[1]}")
        self.punchline_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    AlexaJokeApp(root)
    root.mainloop()

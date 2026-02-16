import tkinter as tk
import random

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("600x500")
        self.root.config(bg="#f4f7fa")

        # Initialize game variables
        self.score = 0
        self.question_count = 0
        self.difficulty = 1
        self.num1 = 0
        self.num2 = 0
        self.operation = "+"
        self.correct_answer = 0

        self.create_menu()

    def create_menu(self):
        """Main menu with a simple, clean design."""
        self.menu_frame = tk.Frame(self.root, bg="#f4f7fa")
        self.menu_frame.pack(expand=True)

        title_label = tk.Label(
            self.menu_frame,
            text="🧮 Arithmetic Quiz",
            font=("Helvetica", 22, "bold"),
            fg="#2e3b4e",
            bg="#f4f7fa"
        )
        title_label.pack(pady=30)

        subtitle = tk.Label(
            self.menu_frame,
            text="Select your difficulty level:",
            font=("Helvetica", 14),
            fg="#4a5568",
            bg="#f4f7fa"
        )
        subtitle.pack(pady=10)

        button_style = {"font": ("Helvetica", 14, "bold"), "width": 20, "height": 2, "bd": 0, "relief": "flat"}

        self.easy_button = tk.Button(
            self.menu_frame, text="Easy (1-9)", bg="#A0D995", fg="#2e3b4e",
            command=lambda: self.start_quiz(1), **button_style
        )
        self.easy_button.pack(pady=8)

        self.moderate_button = tk.Button(
            self.menu_frame, text="Moderate (10-99)", bg="#FFD580", fg="#2e3b4e",
            command=lambda: self.start_quiz(2), **button_style
        )
        self.moderate_button.pack(pady=8)

        self.advanced_button = tk.Button(
            self.menu_frame, text="Advanced (1000-9999)", bg="#FFB6B6", fg="#2e3b4e",
            command=lambda: self.start_quiz(3), **button_style
        )
        self.advanced_button.pack(pady=8)

    def start_quiz(self, difficulty):
        """Hide menu and start the quiz."""
        self.difficulty = difficulty
        self.score = 0
        self.question_count = 0
        self.menu_frame.pack_forget()
        self.show_next_question()

    def show_next_question(self):
        """Display the next math problem."""
        if self.question_count < 10:
            self.question_count += 1
            self.num1, self.num2 = self.random_numbers(self.difficulty)
            self.operation = random.choice(["+", "-"])
            self.correct_answer = self.num1 + self.num2 if self.operation == "+" else self.num1 - self.num2
            self.display_question()
        else:
            self.show_results()

    def random_numbers(self, difficulty):
        """Generate random numbers based on difficulty."""
        if difficulty == 1:
            return random.randint(1, 9), random.randint(1, 9)
        elif difficulty == 2:
            return random.randint(10, 99), random.randint(10, 99)
        else:
            return random.randint(1000, 9999), random.randint(1000, 9999)

    def display_question(self):
        """Display current question."""
        self.quiz_frame = tk.Frame(self.root, bg="#f4f7fa")
        self.quiz_frame.pack(expand=True)

        label = tk.Label(
            self.quiz_frame,
            text=f"Question {self.question_count}/10",
            font=("Helvetica", 16, "bold"),
            fg="#4a5568",
            bg="#f4f7fa"
        )
        label.pack(pady=10)

        problem = tk.Label(
            self.quiz_frame,
            text=f"{self.num1} {self.operation} {self.num2} = ?",
            font=("Helvetica", 22, "bold"),
            fg="#2e3b4e",
            bg="#f4f7fa"
        )
        problem.pack(pady=20)

        self.answer_entry = tk.Entry(self.quiz_frame, font=("Helvetica", 18), justify="center")
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()

        submit_btn = tk.Button(
            self.quiz_frame,
            text="Submit",
            font=("Helvetica", 14, "bold"),
            bg="#5EAAA8",
            fg="white",
            width=12,
            command=self.check_answer
        )
        submit_btn.pack(pady=15)

        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 14), bg="#f4f7fa")
        self.feedback_label.pack(pady=10)

    def check_answer(self):
        """Check if the answer is correct."""
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.correct_answer:
                self.score += 10
                self.feedback_label.config(text="✅ Correct!", fg="#2F855A")
            else:
                self.score += 5
                self.feedback_label.config(text=f"❌ Incorrect. The answer was {self.correct_answer}.", fg="#C53030")
            self.root.after(1000, self.next_question)
        except ValueError:
            self.feedback_label.config(text="Please enter a number!", fg="#C53030")

    def next_question(self):
        """Clean up and go to next question."""
        self.quiz_frame.pack_forget()
        self.show_next_question()

    def show_results(self):
        """Display final score and rank."""
        self.result_frame = tk.Frame(self.root, bg="#f4f7fa")
        self.result_frame.pack(expand=True)

        score_label = tk.Label(
            self.result_frame,
            text=f"Your Final Score: {self.score}/100",
            font=("Helvetica", 20, "bold"),
            fg="#2e3b4e",
            bg="#f4f7fa"
        )
        score_label.pack(pady=20)

        rank = self.calculate_rank()
        rank_label = tk.Label(
            self.result_frame,
            text=f"Rank: {rank}",
            font=("Helvetica", 18),
            fg="#4a5568",
            bg="#f4f7fa"
        )
        rank_label.pack(pady=10)

        play_again_btn = tk.Button(
            self.result_frame,
            text="Play Again",
            font=("Helvetica", 14, "bold"),
            bg="#5EAAA8",
            fg="white",
            width=14,
            command=self.restart_game
        )
        play_again_btn.pack(pady=20)

    def calculate_rank(self):
        """Return a letter grade based on score."""
        if self.score >= 90:
            return "A+"
        elif self.score >= 80:
            return "A"
        elif self.score >= 70:
            return "B"
        elif self.score >= 60:
            return "C"
        else:
            return "F"

    def restart_game(self):
        """Restart the quiz."""
        self.result_frame.pack_forget()
        self.create_menu()

def main():
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Data Functions ----------

def load_students(filename):
    """Load student records from text file."""
    students = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            total_students = int(file.readline().strip())
            for line in file:
                parts = [x.strip() for x in line.split(",")]
                if len(parts) == 6:
                    number = parts[0]
                    name = parts[1]
                    coursework = list(map(int, parts[2:5]))
                    exam = int(parts[5])
                    students.append({
                        "number": number,
                        "name": name,
                        "coursework": coursework,
                        "exam": exam
                    })
        return students
    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt not found.")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file:\n{e}")
        return []

def calculate_total(student):
    cw_total = sum(student["coursework"])
    exam = student["exam"]
    percent = round((cw_total + exam) / 160 * 100, 2)
    return cw_total, exam, percent

def get_grade(percent):
    if percent >= 70: return "A"
    elif percent >= 60: return "B"
    elif percent >= 50: return "C"
    elif percent >= 40: return "D"
    else: return "F"

# ---------- Display Functions ----------

def show_student(student):
    cw, exam, percent = calculate_total(student)
    grade = get_grade(percent)
    return (f"Name: {student['name']}\n"
            f"Student Number: {student['number']}\n"
            f"Coursework Total: {cw}/60\n"
            f"Exam Mark: {exam}/100\n"
            f"Overall Percentage: {percent}%\n"
            f"Grade: {grade}\n")

# ---------- GUI Actions ----------

def view_all():
    output_text.delete(1.0, tk.END)
    if not students:
        output_text.insert(tk.END, "No data loaded.")
        return
    total_percent = 0
    for s in students:
        cw, exam, percent = calculate_total(s)
        total_percent += percent
        output_text.insert(tk.END, show_student(s) + "\n")
    avg = round(total_percent / len(students), 2)
    output_text.insert(tk.END, f"Class Size: {len(students)}\nAverage Percentage: {avg}%")

def view_individual():
    name = student_combo.get()
    output_text.delete(1.0, tk.END)
    if not name:
        messagebox.showinfo("Select Student", "Please choose a student.")
        return
    for s in students:
        if s["name"] == name:
            output_text.insert(tk.END, show_student(s))
            return
    output_text.insert(tk.END, "Student not found.")

def show_highest():
    output_text.delete(1.0, tk.END)
    if not students:
        output_text.insert(tk.END, "No data loaded.")
        return
    top = max(students, key=lambda s: calculate_total(s)[2])
    output_text.insert(tk.END, "--- Highest Overall Score ---\n\n" + show_student(top))

def show_lowest():
    output_text.delete(1.0, tk.END)
    if not students:
        output_text.insert(tk.END, "No data loaded.")
        return
    low = min(students, key=lambda s: calculate_total(s)[2])
    output_text.insert(tk.END, "--- Lowest Overall Score ---\n\n" + show_student(low))

def quit_app():
    root.destroy()

# ---------- GUI Layout ----------

root = tk.Tk()
root.title("Student Manager")
root.geometry("700x500")
root.config(bg="#f7f7f7")

students = load_students("studentMarks.txt")

# Title
title_label = tk.Label(root, text="🎓 Student Manager", font=("Arial", 18, "bold"), bg="#f7f7f7")
title_label.pack(pady=10)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f7f7f7")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="View All Students", command=view_all, width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Highest Score", command=show_highest, width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Lowest Score", command=show_lowest, width=20).grid(row=0, column=2, padx=5, pady=5)

# Student Selector
select_frame = tk.Frame(root, bg="#f7f7f7")
select_frame.pack(pady=10)

tk.Label(select_frame, text="Select Student:", bg="#f7f7f7", font=("Arial", 11)).grid(row=0, column=0, padx=5)
student_names = [s["name"] for s in students]
student_combo = ttk.Combobox(select_frame, values=student_names, width=30, state="readonly")
student_combo.grid(row=0, column=1, padx=5)
tk.Button(select_frame, text="View Record", command=view_individual, width=15).grid(row=0, column=2, padx=5)

# Output Area
output_text = tk.Text(root, width=80, height=18, wrap=tk.WORD, font=("Courier New", 11))
output_text.pack(pady=10)

# Quit Button
tk.Button(root, text="Quit", command=quit_app, width=12, font=("Arial", 11)).pack(pady=10)

root.mainloop()
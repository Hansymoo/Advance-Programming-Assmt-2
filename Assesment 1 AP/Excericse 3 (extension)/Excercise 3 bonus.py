import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ---------- Data Functions ----------

FILE_NAME = "studentMarks.txt"

def load_students(filename=FILE_NAME):
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
        messagebox.showerror("Error", f"{filename} not found.")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file:\n{e}")
        return []

def save_students(students, filename=FILE_NAME):
    """Save student records to the file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"{len(students)}\n")
        for s in students:
            line = f"{s['number']}, {s['name']}, {s['coursework'][0]}, {s['coursework'][1]}, {s['coursework'][2]}, {s['exam']}\n"
            file.write(line)

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

def refresh_dropdown():
    student_names = [s["name"] for s in students]
    student_combo['values'] = student_names

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

def sort_students():
    if not students:
        messagebox.showinfo("Sort Students", "No students to sort.")
        return
    order = messagebox.askquestion("Sort Order", "Sort ascending? (No = descending)")
    ascending = True if order == "yes" else False
    students.sort(key=lambda s: calculate_total(s)[2], reverse=not ascending)
    view_all()
    refresh_dropdown()

def add_student():
    num = simpledialog.askstring("Student Number", "Enter student number (1000-9999):")
    name = simpledialog.askstring("Name", "Enter student name:")
    cw1 = simpledialog.askinteger("Coursework 1", "Enter mark (0-20):", minvalue=0, maxvalue=20)
    cw2 = simpledialog.askinteger("Coursework 2", "Enter mark (0-20):", minvalue=0, maxvalue=20)
    cw3 = simpledialog.askinteger("Coursework 3", "Enter mark (0-20):", minvalue=0, maxvalue=20)
    exam = simpledialog.askinteger("Exam", "Enter exam mark (0-100):", minvalue=0, maxvalue=100)
    if None in [num, name, cw1, cw2, cw3, exam]:
        messagebox.showinfo("Add Student", "Student creation cancelled.")
        return
    students.append({"number": num, "name": name, "coursework":[cw1, cw2, cw3], "exam": exam})
    save_students(students)
    refresh_dropdown()
    messagebox.showinfo("Add Student", f"{name} added successfully.")

def delete_student():
    name = student_combo.get()
    if not name:
        messagebox.showinfo("Delete Student", "Please select a student to delete.")
        return
    for i, s in enumerate(students):
        if s["name"] == name:
            confirm = messagebox.askyesno("Confirm Delete", f"Delete {name}?")
            if confirm:
                students.pop(i)
                save_students(students)
                refresh_dropdown()
                output_text.delete(1.0, tk.END)
                messagebox.showinfo("Deleted", f"{name} has been deleted.")
            return
    messagebox.showinfo("Delete Student", "Student not found.")

def update_student():
    name = student_combo.get()
    if not name:
        messagebox.showinfo("Update Student", "Please select a student.")
        return
    for s in students:
        if s["name"] == name:
            # Sub-menu to choose what to update
            choice = simpledialog.askstring("Update", "Update: name, number, cw1, cw2, cw3, exam?")
            if not choice:
                return
            choice = choice.lower()
            if choice == "name":
                new_val = simpledialog.askstring("Update Name", "Enter new name:")
                if new_val: s["name"] = new_val
            elif choice == "number":
                new_val = simpledialog.askstring("Update Number", "Enter new number:")
                if new_val: s["number"] = new_val
            elif choice in ["cw1","cw2","cw3"]:
                index = int(choice[-1]) - 1
                new_val = simpledialog.askinteger(f"Update {choice}", "Enter new mark (0-20):", minvalue=0, maxvalue=20)
                if new_val is not None: s["coursework"][index] = new_val
            elif choice == "exam":
                new_val = simpledialog.askinteger("Update Exam", "Enter new exam mark (0-100):", minvalue=0, maxvalue=100)
                if new_val is not None: s["exam"] = new_val
            else:
                messagebox.showinfo("Update", "Invalid field.")
                return
            save_students(students)
            refresh_dropdown()
            output_text.delete(1.0, tk.END)
            messagebox.showinfo("Update", f"{s['name']} updated successfully.")
            return
    messagebox.showinfo("Update", "Student not found.")

def quit_app():
    root.destroy()

# ---------- GUI Layout ----------

root = tk.Tk()
root.title("Extended Student Manager")
root.geometry("800x550")
root.config(bg="#f7f7f7")

students = load_students()

# Title
tk.Label(root, text="🎓 Extended Student Manager", font=("Arial", 18, "bold"), bg="#f7f7f7").pack(pady=10)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f7f7f7")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="View All Students", command=view_all, width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Highest Score", command=show_highest, width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Lowest Score", command=show_lowest, width=20).grid(row=0, column=2, padx=5, pady=5)
tk.Button(btn_frame, text="Sort Records", command=sort_students, width=20).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Add Student", command=add_student, width=20).grid(row=1, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Delete Student", command=delete_student, width=20).grid(row=1, column=2, padx=5, pady=5)
tk.Button(btn_frame, text="Update Student", command=update_student, width=20).grid(row=2, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Quit", command=quit_app, width=20).grid(row=2, column=2, padx=5, pady=5)

# Student Selector
select_frame = tk.Frame(root, bg="#f7f7f7")
select_frame.pack(pady=10)

tk.Label(select_frame, text="Select Student:", bg="#f7f7f7", font=("Arial", 11)).grid(row=0, column=0, padx=5)
student_combo = ttk.Combobox(select_frame, values=[s["name"] for s in students], width=30, state="readonly")
student_combo.grid(row=0, column=1, padx=5)
tk.Button(select_frame, text="View Record", command=view_individual, width=15).grid(row=0, column=2, padx=5)

# Output Area
output_text = tk.Text(root, width=90, height=20, wrap=tk.WORD, font=("Courier New", 11))
output_text.pack(pady=10)

root.mainloop()
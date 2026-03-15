import tkinter as tk
from tkinter import filedialog, messagebox
from csv_reader import read_csv, write_csv
from shift_logic import assign_shifts

class App:

    def __init__(self, root):
        self.root = root
        self.root.title("PSDC Shift Calculator")
        self.root.geometry("500x320")

        self.input_file = None
        self.output_file = None
        self.first_datetime = None

        tk.Label(root, text="PSDC Shift Calculator", font=("Arial", 16)).pack(pady=10)

        tk.Button(root, text="Wybierz CSV file", command=self.select_input).pack(pady=10)

        self.first_shift_label = tk.Label(
            root,
            text="Pierwsza zmiana [])"
        )
        self.first_shift_label.pack(pady=5)

        self.first_shift = tk.StringVar(value="NRT")
        tk.OptionMenu(root, self.first_shift, "NRT", "STH").pack()

        tk.Label(root, text="Kto prowadzi zmianę w środę").pack(pady=5)
        self.wed_team = tk.StringVar(value="FRONT")
        tk.OptionMenu(root, self.wed_team, "FRONT", "BACK").pack()

        tk.Button(root, text="Generate CSV", command=self.generate_shifts).pack(pady=20)

    def select_input(self):
        file = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv")]
        )

        if file:
            self.input_file = file
            try:
                rows = read_csv(file)
                if rows:
                    self.first_datetime = rows[0]["datetime"]
                    self.first_shift_label.config(
                        text=f"Pierwsza zmiana [{self.first_datetime}]"
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Błąd odczytu CSV: {e}")

    def generate_shifts(self):
        if not self.input_file:
            messagebox.showerror("Error", "Najpierw wybierz plik CSV")
            return

        file = filedialog.asksaveasfilename(
            title="Zapisz wynik jako",
            defaultextension=".csv",
            filetypes=[("Pliki CSV", "*.csv")]
        )

        if file:
            self.output_file = file
            try:
                rows = read_csv(self.input_file)
                rows.sort(key=lambda r: r["datetime"])

                state = {
                    "first_day_type": self.first_shift.get(),
                    "wednesday_team": self.wed_team.get(),
                }

                assign_shifts(rows, state)
                write_csv(rows, self.output_file)
                messagebox.showinfo("Success", f"Plik został zapisany:\n{self.output_file}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

def start_gui():
    root = tk.Tk()
    App(root)
    root.mainloop()
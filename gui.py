import tkinter as tk
from tkinter import filedialog, messagebox

from csv_reader import read_csv, write_csv
from shift_logic import assign_shifts


class App:

    def __init__(self, root):
        self.translations = {
            "pl": {
                "window_title": "PSDC Shift Calculator",
                "subtitle": "Wybierz plik CSV i wygeneruj wynik z obliczonymi zmianami",
                "language": "Język",
                "select_button": "Wybierz plik CSV",
                "generate_button": "Generuj CSV",
                "file_not_selected": "Plik: nie wybrano",
                "file_selected": "Plik: {path}",
                "first_date_empty": "Pierwsza data: —",
                "last_date_empty": "Ostatnia data: —",
                "first_date": "Pierwsza data: [{value}]",
                "last_date": "Ostatnia data: [{value}]",
                "dialog_select_csv": "Wybierz plik CSV",
                "dialog_save_as": "Zapisz wynik jako",
                "csv_filter": "Pliki CSV",
                "error_title": "Błąd",
                "error_read_csv": "Nie udało się odczytać CSV: {error}",
                "error_select_first": "Najpierw wybierz plik CSV",
                "success_title": "Sukces",
                "success_saved": "Plik zapisany:\n{path}",
            },
            "ru": {
                "window_title": "PSDC Shift Calculator",
                "subtitle": "Выберите CSV и сгенерируйте результат с рассчитанными сменами",
                "language": "Язык",
                "select_button": "Выбрать CSV",
                "generate_button": "Сгенерировать CSV",
                "file_not_selected": "Файл: не выбран",
                "file_selected": "Файл: {path}",
                "first_date_empty": "Первая дата: —",
                "last_date_empty": "Последняя дата: —",
                "first_date": "Первая дата: [{value}]",
                "last_date": "Последняя дата: [{value}]",
                "dialog_select_csv": "Выберите CSV файл",
                "dialog_save_as": "Сохранить результат как",
                "csv_filter": "CSV файлы",
                "error_title": "Ошибка",
                "error_read_csv": "Не удалось прочитать CSV: {error}",
                "error_select_first": "Сначала выберите CSV файл",
                "success_title": "Успешно",
                "success_saved": "Файл сохранён:\n{path}",
            },
            "en": {
                "window_title": "PSDC Shift Calculator",
                "subtitle": "Select a CSV file and generate output with calculated shifts",
                "language": "Language",
                "select_button": "Select CSV file",
                "generate_button": "Generate CSV",
                "file_not_selected": "File: not selected",
                "file_selected": "File: {path}",
                "first_date_empty": "First date: —",
                "last_date_empty": "Last date: —",
                "first_date": "First date: [{value}]",
                "last_date": "Last date: [{value}]",
                "dialog_select_csv": "Select CSV file",
                "dialog_save_as": "Save result as",
                "csv_filter": "CSV files",
                "error_title": "Error",
                "error_read_csv": "Failed to read CSV: {error}",
                "error_select_first": "Select CSV file first",
                "success_title": "Success",
                "success_saved": "File saved:\n{path}",
            },
        }

        self.language_labels = {
            "pl": "Polski",
            "ru": "Русский",
            "en": "English",
        }

        self.current_language = "pl"

        self.root = root
        self.root.title(self._t("window_title"))
        self.root.geometry("680x380")
        self.root.minsize(640, 360)
        self.root.configure(bg="#0f172a")

        self.input_file = None
        self.first_datetime = None
        self.last_datetime = None

        self.colors = {
            "bg": "#0f172a",
            "card": "#111827",
            "text": "#e5e7eb",
            "muted": "#94a3b8",
            "button_text": "#080065",
            "accent": "#1d4ed8",
            "accent_hover": "#1e40af",
            "success": "#059669",
            "success_hover": "#047857",
            "menu_bg": "#ffffff",
            "menu_text": "#111827",
            "menu_active_bg": "#e5e7eb",
            "menu_active_text": "#111827",
        }

        self.container = tk.Frame(root, bg=self.colors["bg"])
        self.container.pack(fill="both", expand=True, padx=24, pady=24)

        self.card = tk.Frame(self.container, bg=self.colors["card"], bd=0, highlightthickness=0)
        self.card.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.card,
            text=self._t("window_title"),
            font=("Arial", 20, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"],
        )
        self.title_label.pack(pady=(24, 4))

        self.subtitle_label = tk.Label(
            self.card,
            text=self._t("subtitle"),
            font=("Arial", 11),
            fg=self.colors["muted"],
            bg=self.colors["card"],
        )
        self.subtitle_label.pack(pady=(0, 10))

        language_frame = tk.Frame(self.card, bg=self.colors["card"])
        language_frame.pack(pady=(0, 14))

        self.language_label = tk.Label(
            language_frame,
            text=f"{self._t('language')}: ",
            font=("Arial", 10),
            fg=self.colors["muted"],
            bg=self.colors["card"],
        )
        self.language_label.pack(side="left", padx=(0, 8))

        self.language_var = tk.StringVar(value=self.language_labels[self.current_language])
        self.language_menu = tk.OptionMenu(
            language_frame,
            self.language_var,
            *self.language_labels.values(),
            command=self.on_language_change,
        )
        self.language_menu.config(
            bg=self.colors["menu_bg"],
            fg=self.colors["menu_text"],
            activebackground=self.colors["menu_active_bg"],
            activeforeground=self.colors["menu_active_text"],
            highlightthickness=0,
            bd=0,
            font=("Arial", 10),
            disabledforeground=self.colors["menu_text"],
        )
        self.language_menu["menu"].config(
            bg=self.colors["menu_bg"],
            fg=self.colors["menu_text"],
            activebackground=self.colors["menu_active_bg"],
            activeforeground=self.colors["menu_active_text"],
            bd=0,
            font=("Arial", 10),
        )
        self.language_menu.pack(side="left")

        self.select_button = tk.Button(
            self.card,
            text=self._t("select_button"),
            command=self.select_input,
            font=("Arial", 11, "bold"),
            fg=self.colors["button_text"],
            bg=self.colors["accent"],
            activebackground=self.colors["accent_hover"],
            activeforeground=self.colors["button_text"],
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            disabledforeground=self.colors["button_text"],
        )
        self.select_button.pack(pady=(0, 16))
        self.select_button.bind("<Enter>", lambda e: self.select_button.config(bg=self.colors["accent_hover"]))
        self.select_button.bind("<Leave>", lambda e: self.select_button.config(bg=self.colors["accent"]))

        info_frame = tk.Frame(self.card, bg="#1f2937", bd=0, highlightthickness=0)
        info_frame.pack(fill="x", padx=24, pady=(0, 20))

        self.file_label = tk.Label(
            info_frame,
            text=self._t("file_not_selected"),
            anchor="w",
            justify="left",
            font=("Arial", 10),
            fg=self.colors["muted"],
            bg="#1f2937",
            padx=12,
            pady=8,
        )
        self.file_label.pack(fill="x")

        self.first_label = tk.Label(
            info_frame,
            text=self._t("first_date_empty"),
            anchor="w",
            justify="left",
            font=("Arial", 10),
            fg=self.colors["text"],
            bg="#1f2937",
            padx=12,
            pady=6,
        )
        self.first_label.pack(fill="x")

        self.last_label = tk.Label(
            info_frame,
            text=self._t("last_date_empty"),
            anchor="w",
            justify="left",
            font=("Arial", 10),
            fg=self.colors["text"],
            bg="#1f2937",
            padx=12,
            pady=6,
        )
        self.last_label.pack(fill="x")

        self.generate_button = tk.Button(
            self.card,
            text=self._t("generate_button"),
            command=self.generate,
            font=("Arial", 11, "bold"),
            fg=self.colors["button_text"],
            bg=self.colors["success"],
            activebackground=self.colors["success_hover"],
            activeforeground=self.colors["button_text"],
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            disabledforeground=self.colors["button_text"],
        )
        self.generate_button.pack(pady=(0, 22))
        self.generate_button.bind("<Enter>", lambda e: self.generate_button.config(bg=self.colors["success_hover"]))
        self.generate_button.bind("<Leave>", lambda e: self.generate_button.config(bg=self.colors["success"]))

    def _t(self, key):
        return self.translations[self.current_language][key]

    def _apply_texts(self):
        self.root.title(self._t("window_title"))
        self.title_label.config(text=self._t("window_title"))
        self.subtitle_label.config(text=self._t("subtitle"))
        self.language_label.config(text=f"{self._t('language')}: ")
        self.select_button.config(text=self._t("select_button"))
        self.generate_button.config(text=self._t("generate_button"))

        if self.input_file:
            self.file_label.config(text=self._t("file_selected").format(path=self.input_file), fg=self.colors["text"])
        else:
            self.file_label.config(text=self._t("file_not_selected"), fg=self.colors["muted"])

        if self.first_datetime:
            self.first_label.config(text=self._t("first_date").format(value=self.first_datetime))
        else:
            self.first_label.config(text=self._t("first_date_empty"))

        if self.last_datetime:
            self.last_label.config(text=self._t("last_date").format(value=self.last_datetime))
        else:
            self.last_label.config(text=self._t("last_date_empty"))

    def on_language_change(self, selected_label):
        for code, label in self.language_labels.items():
            if label == selected_label:
                self.current_language = code
                break
        self._apply_texts()

    def select_input(self):
        file = filedialog.askopenfilename(
            title=self._t("dialog_select_csv"),
            filetypes=[(self._t("csv_filter"), "*.csv")]
        )
        if not file:
            return

        self.input_file = file
        self.file_label.config(text=self._t("file_selected").format(path=file), fg=self.colors["text"])

        try:
            rows = read_csv(file)
            if rows:
                rows.sort(key=lambda r: r["datetime"])
                self.first_datetime = rows[0]["datetime"]
                self.last_datetime = rows[-1]["datetime"]
                self.first_label.config(text=self._t("first_date").format(value=self.first_datetime))
                self.last_label.config(text=self._t("last_date").format(value=self.last_datetime))
            else:
                self.first_datetime = None
                self.last_datetime = None
                self.first_label.config(text=self._t("first_date_empty"))
                self.last_label.config(text=self._t("last_date_empty"))
        except Exception as e:
            messagebox.showerror(self._t("error_title"), self._t("error_read_csv").format(error=e))

    def generate(self):
        if not self.input_file:
            messagebox.showerror(self._t("error_title"), self._t("error_select_first"))
            return

        output_file = filedialog.asksaveasfilename(
            title=self._t("dialog_save_as"),
            defaultextension=".csv",
            filetypes=[(self._t("csv_filter"), "*.csv")]
        )
        if not output_file:
            return

        try:
            rows = read_csv(self.input_file)
            rows.sort(key=lambda r: r["datetime"])
            assign_shifts(rows)
            write_csv(rows, output_file)
            messagebox.showinfo(self._t("success_title"), self._t("success_saved").format(path=output_file))
        except Exception as e:
            messagebox.showerror(self._t("error_title"), str(e))


def start_gui():
    root = tk.Tk()
    App(root)
    root.mainloop()
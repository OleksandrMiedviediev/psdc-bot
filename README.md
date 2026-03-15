# PSDC Shift Calculator

Simple cross-platform script that reads a CSV file with timestamps and assigns warehouse shifts (**FRONT/BACK + NRT/STH**) based on day, night, and weekday rules.

The script works on **Windows** and **macOS** and can be started with a **double click**.

---

# Features

* Reads CSV file with timestamps
* Automatically determines:

  * **Day shift:** 06:30 – 17:00
  * **Night shift:** 18:00 – 04:30
* Assigns team:

  * **FRONT** → Sunday–Tuesday
  * **BACK** → Thursday–Saturday
  * **Wednesday** → chosen by user
* Alternates shift type:

  * **NRT**
  * **STH**
* Generates a new CSV with an additional **shift** column.

---

# Project Structure

```
psdc-bot/
│
├ main.py
├ csv_reader.py
├ shift_logic.py
├ source.csv
├ run_windows.bat
├ run_mac.command
└ data/
```

| File            | Description                 |
| --------------- | --------------------------- |
| main.py         | Main script                 |
| csv_reader.py   | Reads and writes CSV files  |
| shift_logic.py  | Logic for shift calculation |
| source.csv      | Input file                  |
| data/result.csv | Generated output file       |

---

# CSV Format

The CSV must contain one of the following columns:

```
First container scan to trailer
```

or

```
first_container_scan_to_trailer_time_local
```

Date format must be:

```
YYYY-MM-DD HH:MM:SS
```

Example:

```
first_container_scan_to_trailer_time_local
2026-03-06 19:19:00
2026-03-06 23:51:00
2026-03-07 00:00:00
```

---

# How To Run

## Windows

1. Place your CSV file in the project folder and name it:

```
source.csv
```

2. Double click:

```
run_windows.bat
```

The script will start and ask:

```
Kto pracuje w środę? FRONT czy BACK
Podaj typ pierwszej dziennej zmiany (NRT / STH)
```

The result will be saved to:

```
data/result.csv
```

---

## macOS

1. Open **Terminal** and go to the project folder:

```
cd ~/Desktop/psdc-bot
```

2. Make the script executable (only once):

```
chmod +x run_mac.command
```

3. Double click:

```
run_mac.command
```

The script will run and generate:

```
data/result.csv
```

---

# Output Example

Input:

```
2026-03-06 19:19:00
```

Output:

```
2026-03-06 19:19:00,BACK NRT
```

---

# Notes

* If `result.csv` is open in Excel, the script cannot overwrite it.
* Close the file and run the script again if you see a **PermissionError**.
* The script automatically creates the **data** folder if it does not exist.

---

# Requirements

Python **3.10+**

Check Python version:

```
python --version
```

or

```
python3 --version
```

---

# Author

Mode by: [@miedolek](https://github.com/OleksandrMiedviediev)

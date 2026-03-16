# PSDC Shift Calculator

Estetyczna i prosta aplikacja desktopowa na Tkinter do wyliczania zmian w plikach CSV.
Program odczytuje plik z datą/czasem i dodaje kolumnę `shift` w formacie:

- `FRONT STH`
- `BACK NRT`

Obsługiwane systemy: **macOS** i **Windows**.

---

## ✨ Co robi aplikacja

- otwiera plik CSV przez interfejs graficzny;
- pokazuje pierwszą i ostatnią datę z pliku;
- odczytuje datę/czas w wielu formatach i potrafi automatycznie wykryć kolumnę czasu;
- wylicza zmianę dla każdego wiersza według reguł okresu/zespołu/rotacji;
- zapisuje wynik do nowego pliku CSV.

---

## ⚙️ Zasady wyliczania zmian

### 1) Okres

- **DAY:** `06:30` – `17:00`
- **NIGHT:** `18:00` – `04:30`
- czas poza tymi zakresami otrzymuje pustą wartość `shift`.

### 2) Zespół (FRONT/BACK)

- **FRONT:** niedziela, poniedziałek, wtorek;
- **BACK:** czwartek, piątek, sobota;
- **środa:** wyznaczana automatycznie według tygodniowej rotacji.

Dla nocnych rekordów do `04:30` używana jest poprzednia data kalendarzowa.

### 3) Typ zmiany (STH/NRT)

- stosowana jest 28-dniowa rotacja względem daty bazowej;
- przypisanie `DAY/NIGHT` dla `STH/NRT` zmienia się cyklicznie.

Daty bazowe są ustawione w `shift_logic.py`:

- `BASE_DATE = 2026-03-08`
- `BASE_WEDNESDAY = 2026-03-11`

---

## 📄 Format wejściowego CSV

CSV musi zawierać jedną z kolumn czasu:

- `First container scan to trailer`
- `first_container_scan_to_trailer_time_local`

Format daty/czasu: `YYYY-MM-DD HH:MM:SS`

Przykład:

```csv
first_container_scan_to_trailer_time_local
2026-03-06 19:19:00
2026-03-06 23:51:00
2026-03-07 00:00:00
```

---

## 🐍 Instalacja Python

- Oficjalna strona pobierania Python: https://www.python.org/downloads/
- Instrukcja instalacji (oficjalna dokumentacja): https://docs.python.org/3/using/index.html

Zalecana wersja: **Python 3.10+**

Sprawdzenie wersji:

```bash
python --version
# lub
python3 --version
```

---

## ▶️ Uruchomienie

### Windows

1. Kliknij dwukrotnie `run_windows.bat`
2. Wybierz wejściowy plik CSV
3. Kliknij **Generate CSV**
4. Wybierz miejsce zapisu wyniku

### macOS

1. Jednorazowo nadaj plikowi uruchomieniowemu uprawnienia do wykonania:

   ```bash
   chmod +x run_mac.command
   ```

2. Kliknij dwukrotnie `run_mac.command`
3. Wybierz wejściowy CSV i zapisz wynik

### Uruchomienie ręczne

```bash
python main.py
# lub
python3 main.py
```

---

## 🗂️ Struktura projektu

| Plik | Przeznaczenie |
| --- | --- |
| `main.py` | punkt wejścia (start GUI) |
| `gui.py` | interfejs i obsługa działań użytkownika |
| `csv_reader.py` | odczyt/zapis CSV |
| `shift_logic.py` | logika wyliczania zmian |
| `run_windows.bat` | szybkie uruchomienie na Windows |
| `run_mac.command` | szybkie uruchomienie na macOS |
| `data/` | folder na pliki wyjściowe |

---

## 📝 Uwagi

- Jeśli wyjściowy CSV jest otwarty w Excelu, zapis może zakończyć się błędem dostępu.
- Folder docelowy tworzony jest automatycznie (jeśli nie istnieje).

---

## 👤 Autor

[@miedolek](https://github.com/OleksandrMiedviediev)
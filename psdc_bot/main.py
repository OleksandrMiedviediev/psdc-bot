from psdc_bot.csv_reader import read_csv, write_csv
from psdc_bot.shift_logic import assign_shift_for_row
from datetime import timedelta

SOURCE_FILE = "source.csv"
OUTPUT_FILE = "data/result.csv"

def main():
    print("Dzień dobry 👋 Ja bot zmian")

    rows = read_csv(SOURCE_FILE)
    rows.sort(key=lambda r: r["datetime"])
    print("\nNajwcześniejszy zapis:", rows[0]["datetime"])

    try:
        wednesday_team = input("\nKto pracuje w środę? FRONT czy BACK: ").strip().upper()
        if wednesday_team not in ["FRONT", "BACK"]:
            print("Nieprawidłowy wybór, używamy domyślnie FRONT")
            wednesday_team = "FRONT"
    except KeyboardInterrupt:
        print("\n⏩ Do zobaczenia!")
        exit(0)

    # zmienne przekazywane między wierszami
    state = {
        "first_day_type": None,
        "night_team": None,
        "night_type": None,
        "night_end": None,
        "wednesday_team": wednesday_team
    }

    for row in rows:
        assign_shift_for_row(row, state)

    write_csv(rows, OUTPUT_FILE)
    print("\n✅ Plik stworzony:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
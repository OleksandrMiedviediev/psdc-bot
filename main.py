from csv_reader import read_csv, write_csv
from shift_logic import assign_shifts

SOURCE_FILE = "source.csv"
OUTPUT_FILE = "data/result.csv"


def main():
    print("Cześć 👋 Jestem botem do liczenia zmian")

    try:
        rows = read_csv(SOURCE_FILE)
    except FileNotFoundError:
        print("❌ Nie znaleziono pliku source.csv")
        return

    if not rows:
        print("❌ CSV jest pusty")
        return

    rows.sort(key=lambda r: r["datetime"])
    print("\nNajwcześniejszy wpis:", rows[0]["datetime"])

    # Спрашиваем среду
    try:
        wednesday_team = input(
            "\nKto pracuje w środę? FRONT czy BACK: "
        ).strip().upper()

        if wednesday_team not in ["FRONT", "BACK"]:
            print("Niepoprawny wybór, używam FRONT")
            wednesday_team = "FRONT"

    except KeyboardInterrupt:
        print("\nDo zobaczenia!")
        return

    # Спрашиваем первую дневную смену
    try:
        first_day_type = input(
            "\nPodaj typ pierwszej dziennej zmiany (NRT / STH): "
        ).strip().upper()
        if first_day_type not in ["NRT", "STH"]:
            print("Niepoprawny typ, używam NRT")
            first_day_type = "NRT"
    except KeyboardInterrupt:
        print("\nDo zobaczenia!")
        return

    # Состояние для shift_logic
    state = {
        "first_day_type": first_day_type,
        "first_night_type": "STH" if first_day_type == "NRT" else "NRT",
        "wednesday_team": wednesday_team,
    }

    assign_shifts(rows, state)

    try:
        write_csv(rows, OUTPUT_FILE)
    except PermissionError:
        print(
            "\n❌ Nie można zapisać pliku data/result.csv. "
            "Zamknij plik, jeśli jest otwarty, i spróbuj ponownie."
        )
        return

    print("\n✅ Plik zapisany:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
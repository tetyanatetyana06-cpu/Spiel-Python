
from src.question import Frage
from src.category import Category

def main():
    """
    Hauptfunktion des Quiz:
    - Erstellt Kategorien mit Fragen.
    - Zeigt ein Menü für den Benutzer.
    - Zählt Punkte und zeigt am Ende das Gesamtergebnis.
    """
    # Fragen für Kategorie "Deutschland"
    fragen_deutschland = [
        Frage("Was ist die Hauptstadt von Deutschland?", ["Berlin", "München", "Hamburg"], 0),
        Frage("Welche Farben hat die deutsche Flagge?", ["Rot-Gelb-Blau", "Schwarz-Rot-Gold", "Grün-Weiß"], 1),
        Frage("Wie viele Bundesländer hat Deutschland?", ["14", "16", "18"], 1)
    ]

    # Weitere Kategorie "Mathematik"
    fragen_mathe = [
        Frage("Was ist 5 + 3?", ["6", "8", "10"], 1),
        Frage("Was ist die Wurzel aus 9?", ["2", "3", "4"], 1),
        Frage("Was ist 7 * 6?", ["42", "36", "48"], 0)
    ]

    # Kategorien erstellen
    kategorien = [
        Category("Deutschland", fragen_deutschland),
        Category("Mathematik", fragen_mathe)
    ]

    while True:
        # Punkte berechnen
        gesamt_score = sum(k.score for k in kategorien)

        print("\n=== Kategorien-Menü ===")
        print(f"Aktueller Punktestand: {gesamt_score}")
        for i, kat in enumerate(kategorien, start=1):
            print(f"{i}. {kat.name}")
        print(f"{len(kategorien)+1}. Beenden")

        auswahl = input("Bitte wählen: ")

        if auswahl.isdigit():
            auswahl = int(auswahl)
            if 1 <= auswahl <= len(kategorien):
                kategorien[auswahl - 1].play_category()
            elif auswahl == len(kategorien) + 1:
                gesamt_score = sum(k.score for k in kategorien)
                gesamt_versuche = sum(k.failed_attempts for k in kategorien)
                print("\n=== Endauswertung ===")
                print(f"Gesamtpunkte: {gesamt_score}")
                print(f"Gesamtversuche: {gesamt_versuche}")
                print("Quiz beendet.")
                break
            else:
                print("Ungültige Auswahl!")
        else:
            print("Bitte eine Zahl eingeben!")

if __name__ == "__main__":
    main()

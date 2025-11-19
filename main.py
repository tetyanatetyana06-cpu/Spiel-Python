
from src.question import Frage
from src.frage_ohne_index import FrageOhneIndex
from src.category import Category
from src.category import Category, UngueltigeAuswahlError

def main():
    """
    Hauptfunktion des Quiz:
    - Erstellt Kategorien mit Fragen.
    - Zeigt ein Menü für den Benutzer.
    - Zählt Punkte und zeigt am Ende das Gesamtergebnis.
    """
    # Fragen für Kategorie "Überraschung"
    fragen_überraschung = [
        Frage("Wie heisst der laengste Fluss der Welt?", ["Amazonas", "Nil", "Mississippi", "Jangtsekiang"], 1),
        Frage("Welche Sprache hat die meisten Muttersprachler?", ["Englisch", "Mandarin", "Spanisch", "Hindi"], 1),
        Frage("Welche Zahl kommt als Nächstes? 1-4-9-16-25-...", ["30", "49", "36", "50"], 2)
    ]

    # Weitere Kategorie "Programmierung"
    fragen_programmierung = [
        Frage("Was ist ein 'Dictionary' in Python?", ["Eine sortierte Liste", "Eine Sammlung aus Schlüssel-Wert-Paaren", "Eine unveränderte Datenstruktur", "Ein Datentyp für Texte"], 1),
        Frage("Wofür wird eine Funktion in Python verwendet?", ["Um Daten dauerhaft zu speichern", "Um wiederverwendbaren Code zu erstellen", "Um Dateien zu öffnen", "Um Programme zu beenden"], 1),
        Frage("Was ist ein wesentlicher Unterschied zwischen OOP und prozeduralem Programmieren?", ["OOP nutzt Variablen, prozedurale Sprachen nicht", "Prozedurale Programme können keine Funktionen haben", "OOP organisiert Code um Objekte, prozedurales Programmieren um Abläufe", "OOP ist nur für Spiele programmieren"], 2)
    ]

    # Weitere Kategorie "BWL"
    
    # Berechnung für die BWL-Frage
    mitarbeiter = 20000
    produktion = 40000
    produktivität = round(produktion / mitarbeiter, 2)  # Ergebnis: 2 Tische/Mitarbeiter/Jahr

    fragen_bwl = [
        Frage("Was verlangt das ökonomische Prinzip?", ["...das Verhältnis aus Transformations- und Produktionsaufwand zu optimieren", "...das Verhältnis aus Produktionsergebnis und Produktionseinsatz zu optimieren", "...die Rentabilität aus wertmäßigem Output und mengenmäßigem Input zu maximieren", "...die Arbeitsproduktivität sowie den Output zu maximieren"], 1),
        Frage("Was bedeutet 'Cashflow-Sicherung'?", ["Sicherstellen, dass genügend liquide Mittel vorhanden sind, um laufende Kosten zu decken", "Reduzierung von Betriebskosten und Optimierung der Produktionsprozesse", "Stärkung der Eigenkapitalbasis, um unabhängiger von Fremdkapital zu sein", "Erhöhung des Anteils am relevanten Eigenkapital"], 0),
        FrageOhneIndex(f"Eine große Möbelfirma hat {mitarbeiter} Mitarbeiter, die {produktion} Tische pro Jahr produzieren. Wie hoch ist die Arbeitsproduktivität pro Mitarbeiter gerundet auf zwei Nachkommastellen?", str(produktivität))
    ]

    #Weitere Kategorie "Marketing"
    fragen_marketing = [
        Frage("What does not belong in the area of Strategic Marketing?", ["Defining customer value", "Branding", "Organizational image", "CRM and customer service"], 3),
        Frage("What are Marketing Disstribution Channels?", ["Channels are a recurring and routine purchase decision", "Channels are a marketing effort of mutual benefit organizations", "Channels are a set of interdependent organizations involved in the process of making a product/service available for use and consumption", "Channels are transactions committed between employee and customers"], 2),
        Frage("What is the manager`s objective in a 1-way exchange?", ["To enhance personalization, credibility and co-responsibility", "To describe micro-economic transactions", "To achieve firm`s objective, integrate admin functions", "To achieve competetive advantage; adapt resources"], 1)
    ]
    # Kategorien erstellen
    kategorien = [
        Category("Überraschung", fragen_überraschung),
        Category("Programmierung", fragen_programmierung),
        Category("BWL", fragen_bwl),
        Category("Marketing", fragen_marketing)
    ]


    for kat in kategorien:
        kat.score = 0
        kat.attempts = 0
    gesamt_versuche = 0

    print("\nWillkommen zum Quiz! Punktestand beginnt bei 0.\n")

    while True:
        gesamt_score = sum(k.score for k in kategorien)

        print("\n=== Kategorien-Menü ===")
        print(f"Aktueller Punktestand: {gesamt_score} | Gesamtversuche: {gesamt_versuche}")
        for i, kat in enumerate(kategorien, start=1):
            print(f"{i}. {kat.name} (Score: {kat.score}, Versuche: {kat.attempts})")
        print(f"{len(kategorien)+1}. Beenden")

        try:
            auswahl = int(input("Bitte wählen: "))
            if auswahl < 1 or auswahl > len(kategorien) + 1:
                raise UngueltigeAuswahlError("Die gewählte Kategorie existiert nicht.")

            if 1 <= auswahl <= len(kategorien):
                versuche = kategorien[auswahl - 1].play_category()
                gesamt_versuche += versuche
            elif auswahl == len(kategorien) + 1:
                print("\nQuiz beendet.")
                print(f"Endergebnis: {gesamt_score} Punkte bei {gesamt_versuche} Versuchen.")
                print("\n=== Übersicht pro Kategorie ===")
                for kat in kategorien:
                    print(f"{kat.name}: {kat.score} Punkte bei {kat.attempts} Versuchen")
                break

        except ValueError:
            print("Ungültige Eingabe! Bitte eine Zahl eingeben.")
        except UngueltigeAuswahlError as e:
            print(f"Fehler: {e}")


if __name__ == "__main__":
    main()

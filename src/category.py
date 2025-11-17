
from typing import List
from src.question import Frage
from src.frage_ohne_index import FrageOhneIndex

class Category:
    """
    Repräsentiert eine Kategorie im Quiz.
    
    Attribute:
        name (str): Name der Kategorie.
        fragen (List): Liste der Fragen in dieser Kategorie (Frage oder FrageOhneIndex).
        score (int): Punkte, die in dieser Kategorie erzielt wurden.
        failed_attempts (int): Anzahl der fehlgeschlagenen Versuche.
        status (str): Status der Kategorie ('pending', 'completed', 'failed').
    """

    def __init__(self, name: str, fragen: List):
        self.name = name
        self.fragen = fragen
        self.score = 0
        self.failed_attempts = 0
        self.status = "pending"

    def play_category(self):
        """
        Spielt die Kategorie:
        - Maximal 3 Versuche (3 Fragen).
        - Bei richtiger Antwort: Kategorie abgeschlossen.
        - Bei 3 falschen Antworten: Kategorie fehlgeschlagen.
        """
        print(f"\nKategorie: {self.name}")
        max_attempts = 3

        for attempt in range(max_attempts):
            aktuelle_frage = self.fragen[attempt]

            # Sonderfrage ohne Antwortoptionen
            if isinstance(aktuelle_frage, FrageOhneIndex):
                print("\n(Sonderfrage ohne Antwortoptionen)")
                if aktuelle_frage.stellen():
                    self.score += 1
                    self.status = "completed"
                    print("Du hast die Kategorie bestanden!\n")
                    return
                else:
                    self.failed_attempts += 1
                    print(f"Versuch {attempt+1} fehlgeschlagen.\n")
            else:
                # Normale Frage mit Antwortoptionen
                aktuelle_frage.anzeigen()
                try:
                    auswahl = int(input("Deine Auswahl: "))
                    self.failed_attempts += 1
                    if aktuelle_frage.pruefe_antwort(auswahl):
                        self.score += 1
                        self.status = "completed"
                        print("Du hast die Kategorie bestanden!\n")
                        return
                    else:
                        print(f"Versuch {attempt+1} fehlgeschlagen.\n")
                except ValueError:
                    print("Ungültige Eingabe! Bitte eine Zahl eingeben.\n")

        self.status = "failed"
        print("Leider alle Versuche verbraucht. Kategorie fehlgeschlagen!\n")
        return
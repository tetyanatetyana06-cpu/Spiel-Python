
from typing import List
from src.question import Frage
from src.frage_ohne_index import FrageOhneIndex

class UngueltigeAuswahlError(Exception):
    """Wird ausgelöst, wenn die Eingabe außerhalb des gültigen Bereichs liegt."""
    pass   

class Category:
    def __init__(self, name: str, fragen: List):
        self.name = name
        self.fragen = fragen
        self.score = 0
        self.attempts = 0  # Gesamtversuche pro Kategorie
        self.failed_attempts = 0
        self.status = "pending"  # pending, completed, failed

    def play_category(self):
        """
        Spielt die Kategorie einmal durch. Gibt die Anzahl der Versuche zurück.
        """
        print(f"\nKategorie: {self.name}")
        max_attempts = len(self.fragen)
        versuche_in_dieser_runde = 0

        for attempt in range(max_attempts):
            aktuelle_frage = self.fragen[attempt]

            if isinstance(aktuelle_frage, FrageOhneIndex):
                print("\n(Sonderfrage ohne Antwortoptionen)")
                if aktuelle_frage.stellen():
                    self.score += 1
                    self.status = "completed"
                    versuche_in_dieser_runde += 1
                    print(" Du hast die Kategorie bestanden!\n")
                    break
                else:
                    self.failed_attempts += 1
                    versuche_in_dieser_runde += 1
                    print(f" Versuch {attempt+1} fehlgeschlagen.\n")
            else:
                aktuelle_frage.anzeigen()
                try:
                    auswahl = int(input("Deine Auswahl: "))
                    
                    if auswahl < 1 or auswahl > len(aktuelle_frage.antworten):
                        raise UngueltigeAuswahlError("Die Auswahl liegt außerhalb des gültigen Bereichs.")
                    
                    versuche_in_dieser_runde += 1
                    self.failed_attempts += 1

                    if aktuelle_frage.pruefe_antwort(auswahl):
                        self.score += 1
                        self.status = "completed"
                        print(" Du hast die Kategorie bestanden!\n")
                        break
                    else:
                        print(f" Versuch {attempt+1} fehlgeschlagen.\n")
                except ValueError:
                    print("Ungültige Eingabe! Bitte eine Zahl eingeben.\n")
                except UngueltigeAuswahlError as e:
                    print(f"Fehler: {e}\n")

        if self.status != "completed":
            self.status = "failed"
            print("Leider alle Versuche verbraucht. Kategorie fehlgeschlagen!\n")

        # Gesamtversuche aktualisieren
        self.attempts += versuche_in_dieser_runde
        return versuche_in_dieser_runde

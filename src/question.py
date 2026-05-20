from typing import List, Optional

class Frage:
    """
    Repräsentiert eine einzelne Frage mit Text, Antwortmöglichkeiten und richtiger Antwort.
    Attribute:
        text (str): Der Fragetext.
        antworten (List[str]): Liste der möglichen Antworten.
        richtige_antwort (int): Index der richtigen Antwort in der Liste 'antworten' (0-basiert).
        image_path (Optional[str]): Optionaler Pfad zu einem Bild für diese Frage.
    """

    def __init__(self, text: str, antworten: List[str], richtige_antwort: int, image_path: Optional[str] = None):
        self.text = text
        self.antworten = antworten
        self.richtige_antwort = richtige_antwort
        self.image_path = image_path

    def anzeigen(self):
        """CLI-Ausgabe (bestehend)"""
        print(self.text)
        for i, antwort in enumerate(self.antworten, start=1):
            print(f"{i}. {antwort}")

    def pruefe_antwort(self, auswahl: int) -> bool:
        """
        CLI-Prüfung (bestehend, mit print)
        auswahl ist 1-basiert
        """
        if auswahl - 1 == self.richtige_antwort:
            print("Richtige Antwort!")
            return True
        else:
            print("Leider Falsch.")
            return False

    # --- Neu: GUI-/Test-freundlich ohne print ---
    def is_correct(self, auswahl_1_based: int) -> bool:
        """Prüft korrekt/inkorrekt ohne print. (auswahl bleibt 1-basiert)"""
        return (auswahl_1_based - 1) == self.richtige_antwort

    def correct_choice_1_based(self) -> int:
        """Gibt die richtige Auswahl 1-basiert zurück (praktisch für GUI-Markierung)."""
        return self.richtige_antwort + 1

    def correct_answer_text(self) -> str:
        """Text der richtigen Antwort."""
        if 0 <= self.richtige_antwort < len(self.antworten):
            return self.antworten[self.richtige_antwort]
        return ""
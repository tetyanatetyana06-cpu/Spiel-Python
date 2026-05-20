from typing import Optional

class FrageOhneIndex:
    """
    Repräsentiert eine Frage ohne Antwortoptionen, nur mit einer richtigen Antwort.
    Attribute:
        text (str): Der Fragetext.
        richtige_antwort (str): Die richtige Antwort als String.
        image_path (Optional[str]): Optionaler Pfad zu einem Bild für diese Frage.
    """

    def __init__(self, text: str, richtige_antwort: str, image_path: Optional[str] = None):
        self.text = text
        self.richtige_antwort = richtige_antwort
        self.image_path = image_path

    def stellen(self) -> bool:
        """CLI-Version (bestehend)"""
        print(self.text)
        antwort = input("Deine Antwort: ").strip()
        if antwort == self.richtige_antwort:
            print("Richtige Antwort!")
            return True
        else:
            print(f"Falsch! Die richtige Antwort wäre: {self.richtige_antwort}")
            return False

    # --- Neu: GUI-/Test-freundlich ---
    def is_correct(self, antwort: str) -> bool:
        """Prüft ohne print."""
        return antwort.strip() == self.richtige_antwort
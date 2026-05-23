from typing import List, Optional

class FrageOhneIndex:
    """
    Repräsentiert eine Frage ohne Antwortoptionen, nur mit einer richtigen Antwort.
    Attribute:
        text (str): Der Fragetext.
        richtige_antwort (str): Die richtige Antwort als String.
        image_path (Optional[str]): Optionaler Pfad zu einem Bild für diese Frage.
    """

    def __init__(
        self,
        text: str,
        richtige_antwort: str,
        image_path: Optional[str] = None,
        accepted_answers: Optional[List[str]] = None,
    ):
        self.text = text
        self.richtige_antwort = richtige_antwort
        self.image_path = image_path
        self.accepted_answers = accepted_answers or []

    @staticmethod
    def _normalize(value: str) -> str:
        normalized = value.strip().lower().replace(",", ".")
        return " ".join(normalized.split())

    def stellen(self) -> bool:
        """CLI-Version (bestehend)"""
        print(self.text)
        antwort = input("Deine Antwort: ").strip()
        if self.is_correct(antwort):
            print("Richtige Antwort!")
            return True
        else:
            print(f"Falsch! Die richtige Antwort wäre: {self.richtige_antwort}")
            return False

    # --- Neu: GUI-/Test-freundlich ---
    def is_correct(self, antwort: str) -> bool:
        """Prüft ohne print."""
        normalized = self._normalize(antwort)
        if normalized == self._normalize(self.richtige_antwort):
            return True
        return any(normalized == self._normalize(candidate) for candidate in self.accepted_answers)
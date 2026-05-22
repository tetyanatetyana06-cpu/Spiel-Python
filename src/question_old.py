
from typing import List

class Frage:
    """
    Repräsentiert eine einzelne Frage mit Text, Antwortmöglichkeiten und richtiger Antwort.
    
    Attribute:
        text (str): Der Fragetext.
        antworten (List[str]): Liste der möglichen Antworten.
        richtige_antwort (int): Index der richtigen Antwort in der Liste 'antworten'.
    """

    def __init__(self, text: str, antworten: List[str], richtige_antwort: int):
        """
        Initialisiert eine Frage.
        
        Args:
            text (str): Der Fragetext.
            antworten (List[str]): Liste der Antwortmöglichkeiten.
            richtige_antwort (int): Index der richtigen Antwort.
        """
        self.text = text
        self.antworten = antworten
        self.richtige_antwort = richtige_antwort

    def anzeigen(self):
        """
        Zeigt die Frage und die Antwortmöglichkeiten an.
        """
        print(self.text)
        for i, antwort in enumerate(self.antworten, start=1):
            print(f"{i}. {antwort}")

    def pruefe_antwort(self, auswahl: int) -> bool:
        """
        Prüft, ob die gegebene Auswahl korrekt ist und gibt direkt Feedback aus.
        
        Args:
            auswahl (int): Die vom Benutzer gewählte Antwort (1-basiert).
        
        Returns:
            bool: True, wenn korrekt, sonst False.
        """
        if auswahl - 1 == self.richtige_antwort:
            print("Richtige Antwort!")
            return True
        else:
            print("Leider Falsch.")
            return False

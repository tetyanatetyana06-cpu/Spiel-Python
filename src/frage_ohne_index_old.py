
class FrageOhneIndex:
    """
    Repräsentiert eine Frage ohne Antwortoptionen, nur mit einer richtigen Antwort.
    
    Attribute:
        text (str): Der Fragetext.
        richtige_antwort (str): Die richtige Antwort als String.
    """

    def __init__(self, text: str, richtige_antwort: str):
        self.text = text
        self.richtige_antwort = richtige_antwort

    def stellen(self) -> bool:
        """
        Zeigt die Frage an und prüft die Eingabe des Benutzers.
        
        Returns:
            bool: True, wenn die Antwort korrekt ist, sonst False.
        """
        print(self.text)
        antwort = input("Deine Antwort: ").strip()
        if antwort == self.richtige_antwort:
            print("Richtige Antwort!")
            return True
        else:
            print(f"Falsch! Die richtige Antwort wäre: {self.richtige_antwort}")
            return False
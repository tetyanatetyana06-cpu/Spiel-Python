import pytest
from src.question import Frage

@pytest.fixture
def frage():
    """Erstellt eine Beispiel-Frage für die Tests."""
    return Frage(
        text="Was ist die Hauptstadt von Deutschland?",
        antworten=["Berlin", "München", "Hamburg"],
        richtige_antwort=0
    )

def test_anzeigen(frage, capsys):
    """Test: Die Methode anzeigen() soll den Fragetext und die Antworten ausgeben."""
    frage.anzeigen()
    captured = capsys.readouterr()
    assert "Was ist die Hauptstadt von Deutschland?" in captured.out
    assert "1. Berlin" in captured.out
    assert "2. München" in captured.out
    assert "3. Hamburg" in captured.out

def test_pruefe_antwort_richtig(frage, capsys):
    """Test: Prüft, ob eine richtige Antwort True zurückgibt und die richtige Meldung ausgibt."""
    result = frage.pruefe_antwort(1)
    captured = capsys.readouterr()
    assert result is True
    assert "Richtige Antwort!" in captured.out

def test_pruefe_antwort_falsch(frage, capsys):
    """Test: Prüft, ob eine falsche Antwort False zurückgibt und die falsche Meldung ausgibt."""
    result = frage.pruefe_antwort(2)
    captured = capsys.readouterr()
    assert result is False
    assert "Leider Falsch." in captured.out

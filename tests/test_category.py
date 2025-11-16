
import pytest
from src.question import Frage
from src.category import Category

@pytest.fixture
def category():
    """Erstellt eine Beispiel-Kategorie mit drei Fragen."""
    fragen = [
        Frage("Frage 1?", ["A", "B", "C"], 0),
        Frage("Frage 2?", ["A", "B", "C"], 1),
        Frage("Frage 3?", ["A", "B", "C"], 2)
    ]
    return Category("Test-Kategorie", fragen)

def test_category_completed_on_correct_answer(monkeypatch, capsys, category):
    """
    Test: Wenn eine Frage richtig beantwortet wird, soll die Kategorie als 'completed' markiert werden.
    """
    # Simuliere Eingabe: Erste Antwort ist korrekt (1)
    monkeypatch.setattr("builtins.input", lambda _: "1")
    category.play_category()
    captured = capsys.readouterr()
    assert "Du hast die Kategorie bestanden!" in captured.out
    assert category.status == "completed"
    assert category.score == 1

def test_category_failed_after_three_wrong_attempts(monkeypatch, capsys, category):
    """
    Test: Wenn alle drei Fragen falsch beantwortet werden, soll die Kategorie als 'failed' markiert werden.
    """
    # Simuliere Eingaben: Alle Antworten falsch (immer '3')
    inputs = iter(["3", "3", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    category.play_category()
    captured = capsys.readouterr()
    assert "Kategorie fehlgeschlagen" in captured.out
    assert category.status == "failed"
    assert category.failed_attempts == 3

def test_category_stops_after_correct_answer(monkeypatch, capsys, category):
    """
    Test: Wenn die zweite Frage richtig beantwortet wird, soll die Kategorie sofort beendet werden.
    """
    # Simuliere Eingaben: Erste falsch, zweite richtig
    inputs = iter(["3", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    category.play_category()
    captured = capsys.readouterr()
    assert "Du hast die Kategorie bestanden!" in captured.out
    assert category.status == "completed"
    assert category.failed_attempts == 1

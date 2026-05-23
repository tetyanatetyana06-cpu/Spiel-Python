import pytest
from src.frage_ohne_index import FrageOhneIndex


def test_richtige_antwort(monkeypatch):
    frage = FrageOhneIndex("Wie heißt die Hauptstadt von Deutschland?", "Berlin")

    # Simuliere Eingabe "Berlin"
    monkeypatch.setattr('builtins.input', lambda _: "Berlin")

    assert frage.stellen() == True


def test_falsche_antwort(monkeypatch):
    frage = FrageOhneIndex("Wie heißt die Hauptstadt von Deutschland?", "Berlin")

    # Simuliere Eingabe "München"
    monkeypatch.setattr('builtins.input', lambda _: "München")

    assert frage.stellen() == False
import pytest
from src.category import Category, UngueltigeAuswahlError
from src.question import Frage
from src.frage_ohne_index import FrageOhneIndex


def make_category_with_three_questions():
    q1 = Frage("Q1?", ["a", "b", "c"], 0)
    q2 = Frage("Q2?", ["a", "b", "c"], 1)
    q3 = Frage("Q3?", ["a", "b", "c"], 2)
    return Category("Test", [q1, q2, q3])


# ---------------------------------------------------------
# TEST 1: Erste Antwort richtig → Kategorie bestanden
# ---------------------------------------------------------
def test_category_first_answer_correct(monkeypatch):
    cat = make_category_with_three_questions()

    monkeypatch.setattr("builtins.input", lambda _: "1")

    attempts = cat.play_category()

    assert cat.status == "completed"
    assert cat.score == 1
    assert attempts == 1
    assert cat.failed_attempts == 1


# ---------------------------------------------------------
# TEST 2: Erste falsch, zweite richtig → wie du erwartest
# ---------------------------------------------------------
def test_category_second_answer_correct(monkeypatch):
    cat = make_category_with_three_questions()

    inputs = iter(["2", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    attempts = cat.play_category()

    assert cat.status == "completed"
    assert cat.score == 1
    assert attempts == 2
    assert cat.failed_attempts == 2


# ---------------------------------------------------------
# TEST 3: Alle drei falsch → Kategorie failed
# ---------------------------------------------------------
def test_category_all_wrong(monkeypatch):
    cat = make_category_with_three_questions()

    inputs = iter(["3", "1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    attempts = cat.play_category()

    assert cat.status == "failed"
    assert cat.score == 0
    assert attempts == 3
    assert cat.failed_attempts == 3


# ---------------------------------------------------------
# TEST 4: FrageOhneIndex → richtige Antwort
# ---------------------------------------------------------
def test_category_frage_ohne_index_correct(monkeypatch):
    frage = FrageOhneIndex("Test?", "Ja")
    cat = Category("Geo", [frage])

    monkeypatch.setattr("builtins.input", lambda _: "Ja")

    attempts = cat.play_category()

    assert cat.status == "completed"
    assert attempts == 1
    assert cat.score == 1


# ---------------------------------------------------------
# TEST 5: ValueError (z.B. 'x') → springt zur nächsten Frage
# ---------------------------------------------------------
def test_category_invalid_input_valueerror(monkeypatch):
    cat = make_category_with_three_questions()

    # Ablauf:
    #   1) "x" → ValueError → Q2 wird angezeigt
    #   2) "2" → richtige Antwort für Q2
    inputs = iter(["x", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    cat.play_category()

    assert cat.status == "completed"
    assert cat.score == 1
    # failed_attempts erhöht sich NICHT bei ValueError
    assert cat.failed_attempts == 1


# ---------------------------------------------------------
# TEST 6: Auswahlbereichsfehler → springt zur nächsten Frage
# ---------------------------------------------------------
def test_category_out_of_range(monkeypatch, capsys):
    cat = make_category_with_three_questions()

    # Ablauf:
    #   1) "5" → Ungültige Auswahl → Q2 wird angezeigt
    #   2) "2" → richtige Antwort Q2
    inputs = iter(["5", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    cat.play_category()

    out = capsys.readouterr().out
    assert "Die Auswahl liegt außerhalb des gültigen Bereichs." in out
    assert cat.status == "completed"
    assert cat.score == 1
    # failed_attempts erhöht sich NICHT bei ungültiger Auswahl
    assert cat.failed_attempts == 1


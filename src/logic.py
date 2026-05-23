from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Union, Dict

from src.question import Frage
from src.frage_ohne_index import FrageOhneIndex
from src.category import Category

QuestionType = Union[Frage, FrageOhneIndex]
DEFAULT_TIME_LIMIT_SECONDS = 30


def build_categories() -> List[Category]:
  
    fragen_überraschung = [
        Frage("Wie heisst der laengste Fluss der Welt?", ["Amazonas", "Nil", "Mississippi", "Jangtsekiang"], 1),
        Frage("Welche Sprache hat die meisten Muttersprachler?", ["Englisch", "Mandarin", "Spanisch", "Hindi"], 1),
        Frage("Welche Zahl kommt als Nächstes? 1-4-9-16-25-...", ["30", "49", "36", "50"], 2),
    ]

    fragen_programmierung = [
        Frage("Was ist ein 'Dictionary' in Python?",
              ["Eine sortierte Liste", "Eine Sammlung aus Schlüssel-Wert-Paaren", "Eine unveränderte Datenstruktur", "Ein Datentyp für Texte"], 1),
        Frage("Wofür wird eine Funktion in Python verwendet?",
              ["Um Daten dauerhaft zu speichern", "Um wiederverwendbaren Code zu erstellen", "Um Dateien zu öffnen", "Um Programme zu beenden"], 1),
        Frage("Was ist ein wesentlicher Unterschied zwischen OOP und prozeduralem Programmieren?",
              ["OOP nutzt Variablen, prozedurale Sprachen nicht", "Prozedurale Programme können keine Funktionen haben",
               "OOP organisiert Code um Objekte, prozedurales Programmieren um Abläufe", "OOP ist nur für Spiele programmieren"], 2),
    ]

    mitarbeiter = 20000
    produktion = 40000
    produktivität = f"{round(produktion / mitarbeiter, 2):.2f}"

    fragen_bwl = [
        Frage("Was verlangt das ökonomische Prinzip?",
              ["...das Verhältnis aus Transformations- und Produktionsaufwand zu optimieren",
               "...das Verhältnis aus Produktionsergebnis und Produktionseinsatz zu optimieren",
               "...die Rentabilität aus wertmäßigem Output und mengenmäßigem Input zu maximieren",
               "...die Arbeitsproduktivität sowie den Output zu maximieren"], 1),
        Frage("Was bedeutet 'Cashflow-Sicherung'?",
              ["Sicherstellen, dass genügend liquide Mittel vorhanden sind, um laufende Kosten zu decken",
               "Reduzierung von Betriebskosten und Optimierung der Produktionsprozesse",
               "Stärkung der Eigenkapitalbasis, um unabhängiger von Fremdkapital zu sein",
               "Erhöhung des Anteils am relevanten Eigenkapital"], 0),
        FrageOhneIndex(
            f"Eine große Möbelfirma hat {mitarbeiter} Mitarbeiter, die {produktion} Tische pro Jahr produzieren. "
            f"Wie hoch ist die Arbeitsproduktivität pro Mitarbeiter gerundet auf zwei Nachkommastellen?",
            produktivität,
            accepted_answers=["2", "2,00", "2 Tische", "2,00 Tische"],
        ),
    ]

    fragen_marketing = [
        Frage("What does not belong in the area of Strategic Marketing?",
              ["Defining customer value", "Branding", "Organizational image", "CRM and customer service"], 3),
        Frage("What are Marketing Disstribution Channels?",
              ["Channels are a recurring and routine purchase decision",
               "Channels are a marketing effort of mutual benefit organizations",
               "Channels are a set of interdependent organizations involved in the process of making a product/service available for use and consumption",
               "Channels are transactions committed between employee and customers"], 2),
        Frage("What is the manager`s objective in a 1-way exchange?",
              ["To enhance personalization, credibility and co-responsibility",
               "To describe micro-economic transactions",
               "To achieve firm`s objective, integrate admin functions",
               "To achieve competetive advantage; adapt resources"], 1),
    ]

    return [
        Category("Überraschung", fragen_überraschung),
        Category("Programmierung", fragen_programmierung),
        Category("BWL", fragen_bwl),
        Category("Marketing", fragen_marketing),
    ]


def reset_quiz(categories: List[Category]) -> int:
    for kat in categories:
        kat.score = 0
        kat.attempts = 0
        kat.failed_attempts = 0
        kat.status = "pending"
    return 0


@dataclass
class SubmitResult:
    correct: bool
    message: str
    correct_choice_1_based: Optional[int] = None
    correct_text: Optional[str] = None
    finished_category: bool = False
    category_status: Optional[str] = None


class QuizEngine:
    """
    GUI-Engine, die exakt das Kategorie-Verhalten aus deinem CLI-Code abbildet:
      - max_attempts = len(fragen)
      - bei erster richtiger Antwort: Kategorie completed + score++
      - bei falscher Antwort oder Timeout: failed_attempts++ und nächste Frage
      - wenn alle Fragen durch: Kategorie failed
    """

    def __init__(self, categories: Optional[List[Category]] = None):
        self.categories: List[Category] = categories if categories is not None else build_categories()
        self.gesamt_versuche: int = 0

        self.selected_category: Optional[Category] = None
        self.current_index: int = 0
        self.versuche_in_runde: int = 0

    def reset_all(self):
        self.gesamt_versuche = reset_quiz(self.categories)
        self.selected_category = None
        self.current_index = 0
        self.versuche_in_runde = 0

    def category_list(self) -> List[Category]:
        return self.categories

    def select_category_by_index(self, idx: int) -> bool:
        if idx < 0 or idx >= len(self.categories):
            return False
        kat = self.categories[idx]
        if kat.status != "pending":
            return False
        self.selected_category = kat
        self.current_index = 0
        self.versuche_in_runde = 0
        return True

    def current_question(self) -> Optional[QuestionType]:
        if not self.selected_category:
            return None
        if not (0 <= self.current_index < len(self.selected_category.fragen)):
            return None
        return self.selected_category.fragen[self.current_index]

    def question_progress(self) -> str:
        if not self.selected_category:
            return ""
        return f"{self.current_index + 1} von {len(self.selected_category.fragen)}"

    def submit_answer(self, answer: Union[int, str, None], timed_out: bool = False) -> SubmitResult:
        q = self.current_question()
        if q is None or self.selected_category is None:
            return SubmitResult(False, "Keine aktive Frage/Kategorie.", finished_category=True)

        if timed_out:
            return self._handle_incorrect(q, reason="Time is up!")

        if isinstance(q, Frage):
            if not isinstance(answer, int):
                return SubmitResult(False, "Ungültige Eingabe: Bitte eine Antwort auswählen.",
                                   correct_choice_1_based=q.correct_choice_1_based())
            if answer < 1 or answer > len(q.antworten):
                return SubmitResult(False, "Ungültige Eingabe: Auswahl liegt außerhalb des Bereichs.",
                                   correct_choice_1_based=q.correct_choice_1_based())

            if q.is_correct(answer):
                return self._handle_correct(q, correct_choice=q.correct_choice_1_based())
            return self._handle_incorrect(q, reason="Leider falsch.", correct_choice=q.correct_choice_1_based())

        if isinstance(q, FrageOhneIndex):
            if not isinstance(answer, str) or not answer.strip():
                return SubmitResult(False, "Ungültige Eingabe: Bitte eine Antwort eingeben.",
                                   correct_text=q.richtige_antwort)
            if q.is_correct(answer):
                return self._handle_correct(q, correct_text=q.richtige_antwort)
            return self._handle_incorrect(q, reason="Falsch!", correct_text=q.richtige_antwort)

        return SubmitResult(False, "Unbekannter Fragetyp.", finished_category=True)

    def _handle_correct(self, q: QuestionType, correct_choice: Optional[int] = None, correct_text: Optional[str] = None) -> SubmitResult:
        kat = self.selected_category
        assert kat is not None

        self.versuche_in_runde += 1
        self.gesamt_versuche += 1

        kat.score += 1
        kat.attempts += 1
        kat.status = "completed"

        return SubmitResult(True, "Richtige Antwort!", correct_choice, correct_text, True, kat.status)

    def _handle_incorrect(self, q: QuestionType, reason: str, correct_choice: Optional[int] = None, correct_text: Optional[str] = None) -> SubmitResult:
        kat = self.selected_category
        assert kat is not None

        self.versuche_in_runde += 1
        self.gesamt_versuche += 1

        kat.failed_attempts += 1
        kat.attempts += 1

        if self.current_index + 1 >= len(kat.fragen):
            kat.status = "failed"
            return SubmitResult(False, reason, correct_choice, correct_text, True, kat.status)

        self.current_index += 1
        return SubmitResult(False, reason, correct_choice, correct_text, False, kat.status)

    def summary(self) -> Dict:
        total_correct = sum(k.score for k in self.categories)
        total_attempts = sum(k.attempts for k in self.categories)
        total_failed = sum(k.failed_attempts for k in self.categories)
        percent = (total_correct / total_attempts * 100.0) if total_attempts > 0 else 0.0

        by_cat = []
        for k in self.categories:
            cat_percent = (k.score / k.attempts * 100.0) if k.attempts > 0 else 0.0
            by_cat.append({
                "name": k.name,
                "score": k.score,
                "attempts": k.attempts,
                "failed_attempts": k.failed_attempts,
                "status": k.status,
                "percent": round(cat_percent, 2),
            })

        return {
            "score_total": total_correct,
            "attempts_total": total_attempts,
            "failed_total": total_failed,
            "percent_total": round(percent, 2),
            "by_category": by_cat,
            "gesamt_versuche_engine": self.gesamt_versuche,
        }
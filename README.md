# "Bist du gut vorbereitet?" - das Klausurvorbereitungsquiz


## Inhaltsverzeichnis
- [Projektbeschreibung](#projektbeschreibung)
- [Voraussetzungen und Installation](#voraussetzungen-und-installation)
- [Klassendiagramm](#klassendiagramm)
- [Ausführen](#ausführen-des-quiz)
- [Testen des Programms mit Pytest](#testen-des-programms-mit-pytest)
- [Mitwirkende am Quiz](#mitwirkende-am-quiz)

--------------------------------------------------------------------------------------------------------------------------------------------------------------
   
## 1. Projektbeschreibung: <br>
Ein Quiz, was unseren Kommilitonen helfen soll, ihr Wissen zu zwei unserer Prüfungsfächer aufzufrischen. 
Das Quiz beinhaltet Multipe-Choice-Fragen sowie Rechenaufgaben und eine kleine Spaß-Kategorie mit Fragen, die nichts mit Uni-Inhalten zu tun haben.
Das Quiz besteht aus vier Kategorien, die in beliebiger Reihenfolge abgearbeitet werden können. Jede Kategorie enthält
maximal drei Fragen. Beantwortet der Nutzer die erste Frage richtig, besteht er die Kategorie. Hat der Benutzer eine Frage falsch beantwortet, 
hat er noch zwei weitere Versuche mit zwei anderen Fragen, bevorer in der Kategorie druchfällt. Am Ende des Quiz wird das Ergebnis des 
Benutzers ausgewertet. Man kann das Quiz auch während des Versuchs neustarten, wobei alle bisherigen Eingaben des Durchlaufs gelöscht werden.

Unser Projekt wurde mithilfe von GitHub, Visual Studio Code und Pycharm erstellt. Zur Unterstützung unserer Arbeit
haben wir die KI-Tools ChatGPT und hauptsächlich Microsoft Copilot verwendet. 
  
--------------------------------------------------------------------------------------------------------------------------------------------------------------
## 2. Voraussetzungen und Installation <br>
  ### 2.1 Voraussetzungen für das Durchlaufen des Quiz: <br>
  -Python Version 3.13.2  <br>
  -Visual Studion Code (optional, andere IDE möglich) <br>
  -GitHub-Account <br>

   ### 2.2 Installationsanleitung Python 3.13.2: <br>
  Über die offizielle Python Website kann man diese Python installieren und sich einer detaillierten Installationsanleitung unter „downloads“ bedienen.
  [Python Download](https://www.python.org/downloads/)


  ### 2.3 Installationsanleitung Visual Studio Code: <br>
   Über die offizielle VS Code Website kann man diese IDE installieren und sich einer detaillierten Installationsanleitung unter „DOCS“ bedienen. 
   [VS Code Download](https://code.visualstudio.com/docs/)

 
  ### 2.4 Installationsanleitung des Quiz am Beispiel von Visual Studio Code: <br>
   Um das Repository lokal zu klonen, klickt man auf den grünen Code Button in der "Code"-Abteilung von GitHub. Dort kopiert man die URL des Repositories und        öffnet die Visual Studio Code App. Man wählt ganz links das Source-Control-Symbol in der Leiste aus und klickt auf das blaue Feld "Clone Repository". Jetzt
   kann man in die Suchleiste oben in der Mitte der Benutzeroberfläche die URL einfügen und die Projektstruktur sollte links im Explorer auftauchen.

   ### 2.5 Bedienung des feature/gui - branch
   Um sicherzustellen, dass Sie die GUI-Version des Quiz öffnen, können Sie folgende Commands nacheinander in Ihrem Terminal der IDE Ihrer Wahl eingeben, nachdem
   Sie das Repository bereits geklont haben: 
   ```bash
         <git checkout feature/gui>
	      <git pull>
   ```



--------------------------------------------------------------------------------------------------------------------------------------------------------------
3. Klassendiagramm

classDiagram

class UngueltigeAuswahlError { <br>
    << Exception >> <br>
} <br>

class Frage { <br>
    - text: str <br>
    - antworten: List[str] <br>
    - richtige_antwort: int <br>
    + init(text, antworten, richtige_antwort) <br>
    + anzeigen() <br>
    + pruefe_antwort(auswahl: int) bool <br>
} <br>

class FrageOhneIndex { <br>
    - text: str <br>
    - richtige_antwort: str <br>
    + init(text, richtige_antwort) <br>
    + stellen() bool <br>
} <br>

class Category { <br>
    - name: str <br>
    - fragen: List[Frage | FrageOhneIndex] <br>
    - score: int <br>
    - attempts: int <br>
    - failed_attempts: int <br>
    - status: str <br>
    + init(name, fragen) <br>
    + play_category() int <br>
} <br>

class main { <br>
    - erzeugt Kategorien: Category <br>
    - ruft play_category() auf <br>
    - verwaltet Gesamtpunkte <br>
    - Eingabe-/Auswahl- <br>
} <br>

UngueltigeAuswahlError <|-- Frage <br> 
UngueltigeAuswahlError <|-- FrageOhneIndex <br>

Frage --> main <br>
FrageOhneIndex --> Category <br>
Category --> main <br>


--------------------------------------------------------------------------------------------------------------------------------------------------------------

4. Ausführen des Quiz: <br>
   
Man wählt links im Explorer die main.py-Datei aus. Diese ist die Datei, in der das eigentliche Quiz ausgeführt wird.
Dauraufhin klickt man auf das "Run Python File"-Symbol (ein nach links zeigendes Dreieck), das sich rechts in der Tab-Leiste
im oberen Bereich des Bildschirms befindet. Nun sollte unten im Terminal Folgendes erscheinen:

=== Kategorien-Menü ===
Aktueller Punktestand: 0 | Gesamtversuche: 0
1. Überraschung (Score: 0, Versuche: 0, Status: pending)
2. Programmierung (Score: 0, Versuche: 0, Status: pending)
3. BWL (Score: 0, Versuche: 0, Status: pending)
4. Marketing (Score: 0, Versuche: 0, Status: pending)
5. Beenden
6. Neustart
Bitte wählen:

Dies ist das Menü unseres Quiz. Mit der Eingabe einer Zahl von 1-4, direkt hinter dem "Bitte wählen" im Terminal kann man eine beliebige Kategorie auswählen.
Beispiel: Folgendes sollte erscheinen, wenn man die Zahl "2" eingibt:

Kategorie: Programmierung
Was ist ein 'Dictionary' in Python?
1. Eine sortierte Liste
2. Eine Sammlung aus Schlüssel-Wert-Paaren
3. Eine unveränderte Datenstruktur
4. Ein Datentyp für Texte
Deine Auswahl:

Gibt man die richtige Antwort ein, wird die Kategorie als bestanden gezählt und man wird zu einem veränderten Menü weitergeleitet:

=== Kategorien-Menü ===
Aktueller Punktestand: 1 | Gesamtversuche: 1
1. Überraschung (Score: 0, Versuche: 0, Status: pending)
2. Programmierung (Score: 1, Versuche: 1, Status: completed)
3. BWL (Score: 0, Versuche: 0, Status: pending)
4. Marketing (Score: 0, Versuche: 0, Status: pending)
5. Beenden
6. Neustart
Bitte wählen:

Gibt man die falsche Antwort ein, wird man zu einer Frage innerhalb der Kategorie weitergeleitet:


Wofür wird eine Funktion in Python verwendet?
1. Um Daten dauerhaft zu speichern
2. Um wiederverwendbaren Code zu erstellen
3. Um Dateien zu öffnen
4. Um Programme zu beenden
Deine Auswahl:

Wenn man auch diese Aufgabe falsch beantwortet, bekommt man noch eine weitere Frage innerhalb der Kategorie. Hat man auch diese falsch,
fällt man in der Kategorie mit 0 Punkten durch und wird zurück zum leicht veränderten hauptmenü weitergeleitet, um die nächste kategorie auswählen.
So sieht das aus:

=== Kategorien-Menü ===
Aktueller Punktestand: 0 | Gesamtversuche: 3
1. Überraschung (Score: 0, Versuche: 0, Status: pending)
2. Programmierung (Score: 0, Versuche: 3, Status: failed)
3. BWL (Score: 0, Versuche: 0, Status: pending)
4. Marketing (Score: 0, Versuche: 0, Status: pending)
5. Beenden
6. Neustart
Bitte wählen:

Wenn man alle Kategorien abgearbeitet hat, kann man die Zahl "5" eingeben, um das Quiz zu beenden. Um einen erneuten Druchlauf zu starten, klickt man wieder
auf das "Run Python File"-Symbol. Man kann auch die Zahl "6" eingeben, wodurch die Daten des bisherigen Durchlaufs gelöscht werden und ein neuer Durchlauf beginnt, ohne die vorherigen Ergebnisse in die Bewertung einzubeziehen.


Quiz beendet.
Endergebnis: 2 Punkte bei 8 Versuchen.

=== Übersicht pro Kategorie ===
Überraschung: 1 Punkte bei 1 Versuchen (Status: completed)
Programmierung: 0 Punkte bei 3 Versuchen (Status: failed)
BWL: 1 Punkte bei 1 Versuchen (Status: completed)
Marketing: 0 Punkte bei 3 Versuchen (Status: failed)

Dies wäre eine beispielhafte Auswertung des Quiz.


--------------------------------------------------------------------------------------------------------------------------------------------------------------
5.Testen des Programms mit Pytest:
Falls Sie das Quiz auf Fehler im Code testen möchten, können Sie dies mit Pytest tun. <br>
Wählen Sie eine der Testdateien links in der Explorer-leiste innerhalb des „tests“-Ordners aus. Daraufhin gehen Sie NICHT 
auf den „Run Python File“-Button, sondern öffnen ein Terminal, indem Sie in der obersten Leiste die drei Punkte zwischen 
„Run“ und dem Pfeil nach links auswählen, dann „Terminal“ und dann „New Terminal“.
Alternativ können Sie ein bestehendes Terminal unten rechts neben dem Terminalfeld auswählen, die alle „Python“ heißen.<br>
Daraufhin schreibt man in das Terminal „pytest -v“ rein, und die Dateien werden getestet. Eine Fehleranalyse sollte in dem Terminal auftauchen.


--------------------------------------------------------------------------------------------------------------------------------------------------------------


6. Mitwirkende am Quiz: <br>

  Lead Developer: Sarah Friedmann <br>
  Testverantwortliche: Tetiana Martyniuk <br>
  Dokumentationsverantwortliche: Darja Scherbina <br>
  Präsentationsverantwortliche: Javeria Mohammad


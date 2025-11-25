"Bist du gut vorbereitet?" - das Klausurvorbereitungsquiz


Inhaltsverzeichnis:
1. Projektbeschreibung
2. Voraussetzung und Installation
  2.1 Voraussetzungen für das Durchlaufen des Quiz
  2.2 Installationsanleitung Python 3.13.2
  2.3 Installationsanleitung Visual Studio Code
  2.4 Installationsanleitung des Quiz am Beisiel von Visual Studio Code
3. Ausführen des Quiz
4. Mitwirkende am Quiz

--------------------------------------------------------------------------------------------------------------------------------------------------------------
   
1. Projektbeschreibung: <br>
Ein Quiz, was unsere Komilitonen helfen soll, ihr Wissen zu zwei unserer Prüfungsfächer aufzufrischen. 
Das Quiz beinhaltet Multipe-Choice-Fragen, sowie Rechenaufgaben und eine kleine Spaß-Kategorie, die Fragen stellt,
welche nichts mit Uni-Inhalten gemein haben.
Das Quiz besteht aus vier Kategorien, die in beliebiger Reihenfolge abgearbeitet werden können. Jede Kategorie enthält
maximal drei Fragen. Beantwortet der Nutzer die erste Frage richtig, besteht er die Kategorie. Hat der Benutzer eine Frage falsch beantwortet, 
hat er noch zwei weitere Versuche mit zwei anderen Fragen, bevorer in der Kategorie druchfällt. Am Ende des Quiz wird das Ergebnis des 
Benutzers ausgewertet. Man kann das Quiz auch während des Versuchs neustarten, wobei alle bisherigen Eingaben des Durchlaufs gelöscht werden.

Unser Projekt wurde mithilfe von GitHub, Visual Studio Code und Pycharm erstellt. ZUr Unterstützung unserer Arbeit
haben wir die KI-Tools ChatGPT und hauptsächlich Microsoft Copilot verwendet. 
  
--------------------------------------------------------------------------------------------------------------------------------------------------------------

2. Voraussetzungen und Installation <br>
  2.1 Voraussetzungen für das Durchlaufen des Quiz: <br>

  -Python Version 3.13.2 muss auf dem Rechner installiert sein.
  -Visual Studion Code, bzw eine andere Code-Editor Software, muss auf dem Rechner installiert sein.
  -Es muss ein GitHub-Account vorhanden sein, der mit dem Code-Editor-Programm verbunden ist.


  2.2 Installationsanleitung Python 3.13.2: <br>
   Windows <br>
   Man geht auf die offzielle Python Website (Python.org) und geht zu python.org/downloads.
   Daraufhin wählt man Python 3.13.2 aus und lädt den Installer für Windows herunter.Nun kann man die .exe Datei ausführen,
   wobei es wichtig ist die Option "Add Python to PATH" auszuwählen, und dann klickt man auf Install Now.
   Jetzt öffnet man das Rechnerterminal und prüft mit "python --version", ob der Download erfolgreich war.

   macOS <br>
   Für macOS empfiehlt es sich homebrew zu verwenden. Dort tippt man "brew install python@3.13" ein, und danach passt man es mit
   "echo 'export PATH="/usr/local/opt/python@3.13/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc" an.
   Alternativ kann man sich auch das macOS-Paket von Python herunterladen und installieren.


   2.3 Installationsanleitung Visual Studio Code: <br>
   Windows <br>
    Man begibt sich zu https://code.visualstudio.com/ und lädt den Installer für Windows herunter.
    Daraufhin führt man die heruntrgeladene .exe Datei aus und wählt für diese "Add to PATH" und "Create Desktop Icon" aus.
    Anschließend klickt man auf "Install". Nun kann man VS Code über das Startmenü öffnen.

   macOS <br>
    Man begibt sich zu https://code.visualstudio.com/ und lädt die .zip Datei für macOS herunter.
    Jetzt entpackt man die Datei und verschiebt sie in den Ordner "Programme". Nun kann man VS Code aus dem Programme Ordner oder
    über das Spotlight öffnen.

 

   2.4 Installationsanleitung des Quiz am Beispiel von Visual Studio Code: <br>
    Man öffnet Visual Studio Code und klickt auf das Account-icon in der Status-Leiste. Dort kann man "Sign in to GitHub"
    auswählen. Ist dies nicht vorhanden, kann man auf die Suchleiste in Visual Studio Code klicken und dort "GitHub" eingeben.
    Als eins der Ergebnisse sollte ein blaues Feld mit "sign in to sync settings" auftauchen, welches man auswählt. Man
    wird zu der Online-Seite weitergeleitet, wo man Visual Studio Code authorisieren muss. Es sollte eine Box mit dem 
    eigenen GitHub-Account auftauchen, wo man auf das grüne Feld "Continue" klickt. Daraufhin erscheint das Visual Studio Code 
    Zeichen und man wird zu der Visual Studio Code Desktop App weitergeleitet.
    Dort kann man per Klick auf das Account-Icon überprüfen können, ob man eingeloggt ist.
    
    Repository Clonen: <br>
    Man klickt auf den grünen Code Button in der "Code" Abteilung von GitHub. Dort kopiert man die URL des Repositorys
    und öffnet die Visual Studio Code App. Man wählt ganz links das Source Control-Zeichen in der Leiste aus und klickt auf das blaue
    Feld "Clone Repository". Jetzt kann man in die Suchleiste oben in der Mitte der Benutzeroberfläche die URL hineinkopieren und 
    die Projektstruktur sollte links im Explorer auftauchen.

--------------------------------------------------------------------------------------------------------------------------------------------------------------

3. Ausführen des Quiz: <br>
   
Man wählt links im Explorer die main.py Datei aus. Diese ist die Datei, in der das eigentliche Quiz ausgeführt wird.
Dauraufhin klickt man auf das "Run Python File" Zeichen (ein nach links zeigendes Dreieck), das sich rechts in der Tab-Leiste befindet,
im oberen Bereich des Bildschirms. Nun sollte unten im Terminal folgendes Auftauchen:

=== Kategorien-Menü ===
Aktueller Punktestand: 0 | Gesamtversuche: 0
1. Überraschung (Score: 0, Versuche: 0, Status: pending)
2. Programmierung (Score: 0, Versuche: 0, Status: pending)
3. BWL (Score: 0, Versuche: 0, Status: pending)
4. Marketing (Score: 0, Versuche: 0, Status: pending)
5. Beenden
6. Neustart
Bitte wählen:

Dies ist das Menü unseres Quiz. Mit der Eingabe einer Zahl von 1-4, hinter dem "Bitte wählen." direkt im Terminal, kann man eine beliebige Kategorie auswählen.
Als Beispiel: Folgendes sollte auftauchen, wenn man die Zahl "2" eingibt:

Kategorie: Programmierung
Was ist ein 'Dictionary' in Python?
1. Eine sortierte Liste
2. Eine Sammlung aus Schlüssel-Wert-Paaren
3. Eine unveränderte Datenstruktur
4. Ein Datentyp für Texte
Deine Auswahl:

Würde man die richtige Antwort eingeben, würde die Kategorie als bestanden gezählt werden und man würde zu einem veränderten Menü weitergeleitet werden:

=== Kategorien-Menü ===
Aktueller Punktestand: 1 | Gesamtversuche: 1
1. Überraschung (Score: 0, Versuche: 0, Status: pending)
2. Programmierung (Score: 1, Versuche: 1, Status: completed)
3. BWL (Score: 0, Versuche: 0, Status: pending)
4. Marketing (Score: 0, Versuche: 0, Status: pending)
5. Beenden
6. Neustart
Bitte wählen:

Würde man die falsche Antwort eingeben, würde man zu einer weiteren Frage innerhalb der Kategorie weitergeleitet werden:


Wofür wird eine Funktion in Python verwendet?
1. Um Daten dauerhaft zu speichern
2. Um wiederverwendbaren Code zu erstellen
3. Um Dateien zu öffnen
4. Um Programme zu beenden
Deine Auswahl:

Wenn man diese Aufgabe ebenfalls falsch hat, kriegt man noch eine weitere Frage innerhalb der Kategorie, doch hat man auch sie falsch,
fällt man in der Kategorie mit 0 Punkten durch und wird zurück zum leicht veränderten hauptmenü weitergeleitet und kann die nächste kategorie auswählen.
So würde das aussehen:

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
auf das "Run Python File" Zeichen. Man kann auch die Zahl "6" eingeben, was die Daten des bisherigen Durchlaufs während des Durchlaufs löscht, und einen Neuen anfängt,
ohne die verloren gegangenen Daten in die Bewertung mitzuzählen.


Quiz beendet.
Endergebnis: 2 Punkte bei 8 Versuchen.

=== Übersicht pro Kategorie ===
Überraschung: 1 Punkte bei 1 Versuchen (Status: completed)
Programmierung: 0 Punkte bei 3 Versuchen (Status: failed)
BWL: 1 Punkte bei 1 Versuchen (Status: completed)
Marketing: 0 Punkte bei 3 Versuchen (Status: failed)

Dies wäre eine beispielhafte Auswertung des Quiz.


--------------------------------------------------------------------------------------------------------------------------------------------------------------

4. Mitwirkende am Quiz: <br>

  Lead Developer: Sarah Friedmann
  Testverantwortliche: Tetiana Martyniuk
  Dokumentationsverantwortliche: Darja Scherbina
  Präsentationsverantwortliche: Javeria Mohammad


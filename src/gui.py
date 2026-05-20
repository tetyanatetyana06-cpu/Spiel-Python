import tkinter as tk
from tkinter import ttk, messagebox

from src.logic import QuizEngine, DEFAULT_TIME_LIMIT_SECONDS
from src.question_old import Frage
from src.frage_ohne_index_cli import FrageOhneIndex

try:
    from PIL import Image, ImageTk  # optional
except Exception:
    Image = None
    ImageTk = None


class QuizGUI:
    def __init__(self, root: tk.Tk, engine: QuizEngine, time_limit_seconds: int = DEFAULT_TIME_LIMIT_SECONDS):
        self.root = root
        self.engine = engine
        self.time_limit_seconds = time_limit_seconds

        self.root.title("Quiz (GUI)")
        self.root.geometry("920x560")
        self.root.minsize(860, 520)

        # Theme / Style
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        self.main = ttk.Frame(self.root, padding=12)
        self.main.pack(fill="both", expand=True)

        # Navigation / State
        self.timer_after_id = None
        self.remaining = 0
        self.current_image = None  # keep reference

        # UI Frames
        self.start_frame = ttk.Frame(self.main)
        self.quiz_frame = ttk.Frame(self.main)
        self.result_frame = ttk.Frame(self.main)

        self._build_start_frame()
        self._build_quiz_frame()
        self._build_result_frame()

        self.show_start()

    # ----------------------------
    # Frame switching
    # ----------------------------
    def _hide_all(self):
        for f in (self.start_frame, self.quiz_frame, self.result_frame):
            f.pack_forget()

    def show_start(self):
        self._cancel_timer()
        self._hide_all()
        self._refresh_start_categories()
        self.start_frame.pack(fill="both", expand=True)

    def show_quiz(self):
        self._hide_all()
        self._render_question()
        self.quiz_frame.pack(fill="both", expand=True)

    def show_results(self):
        self._cancel_timer()
        self._hide_all()
        self._render_results()
        self.result_frame.pack(fill="both", expand=True)

    # ----------------------------
    # START FRAME
    # ----------------------------
    def _build_start_frame(self):
        top = ttk.Frame(self.start_frame)
        top.pack(fill="x")

        btn_menu = ttk.Menubutton(top, text="Menu")
        btn_menu.pack(side="left", padx=(0, 8))

        menu = tk.Menu(btn_menu, tearoff=0)
        menu.add_command(label="Neues Quiz starten", command=self._menu_new_quiz)
        menu.add_command(label="Quiz neu starten", command=self._menu_restart_quiz)
        menu.add_separator()
        menu.add_command(label="Quiz beenden", command=self._menu_quit)
        btn_menu["menu"] = menu

        btn_infos = ttk.Button(top, text="Infos", command=self._open_infos)
        btn_infos.pack(side="left")

        # Header
        header = ttk.Label(self.start_frame, text="Kategorien auswählen", font=("Segoe UI", 18, "bold"))
        header.pack(anchor="w", pady=(14, 6))

        self.score_label = ttk.Label(self.start_frame, text="", font=("Segoe UI", 11))
        self.score_label.pack(anchor="w", pady=(0, 10))

        # Categories area
        self.cat_container = ttk.Frame(self.start_frame)
        self.cat_container.pack(fill="both", expand=True)

        bottom = ttk.Frame(self.start_frame)
        bottom.pack(fill="x", pady=(10, 0))

        self.btn_show_results = ttk.Button(bottom, text="Show Results", command=self.show_results)
        self.btn_show_results.pack(side="right")

    def _refresh_start_categories(self):
        # Clear
        for w in self.cat_container.winfo_children():
            w.destroy()

        # Update stats label
        summary = self.engine.summary()
        self.score_label.config(
            text=f"Aktueller Punktestand: {summary['score_total']} | Gesamtversuche: {summary['gesamt_versuche_engine']}"
        )

        # Categories grid
        cats = self.engine.category_list()

        grid = ttk.Frame(self.cat_container)
        grid.pack(fill="both", expand=True)

        cols = 2
        for i, cat in enumerate(cats):
            r = i // cols
            c = i % cols

            card = ttk.Frame(grid, padding=10, relief="ridge")
            card.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)

            title = ttk.Label(card, text=cat.name, font=("Segoe UI", 14, "bold"))
            title.pack(anchor="w")

            meta = ttk.Label(
                card,
                text=f"Score: {cat.score} | Versuche: {cat.attempts} | Status: {cat.status}",
                font=("Segoe UI", 10)
            )
            meta.pack(anchor="w", pady=(2, 10))

            btn = ttk.Button(card, text="Kategorie starten", command=lambda idx=i: self._start_category(idx))
            btn.pack(anchor="e")

            if cat.status != "pending":
                btn.state(["disabled"])

        for c in range(cols):
            grid.columnconfigure(c, weight=1)
        for r in range((len(cats) + cols - 1) // cols):
            grid.rowconfigure(r, weight=1)

    def _start_category(self, idx: int):
        ok = self.engine.select_category_by_index(idx)
        if not ok:
            messagebox.showwarning("Hinweis", "Diese Kategorie kann aktuell nicht gestartet werden (bereits gespielt oder ungültig).")
            return
        self.show_quiz()

    # ----------------------------
    # INFOS / MENU actions
    # ----------------------------
    def _open_infos(self):
        win = tk.Toplevel(self.root)
        win.title("Infos")
        win.geometry("620x420")
        win.transient(self.root)

        nb = ttk.Notebook(win)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        tab_rules = ttk.Frame(nb, padding=10)
        tab_desc = ttk.Frame(nb, padding=10)
        tab_hint = ttk.Frame(nb, padding=10)

        nb.add(tab_rules, text="Regeln")
        nb.add(tab_desc, text="Spielbeschreibung")
        nb.add(tab_hint, text="Hinweise")

        # Beispieltexte: bewusst generisch (bitte anpassen)
        ttk.Label(tab_rules, text="Regeln (Beispieltext)", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))
        ttk.Label(
            tab_rules,
            text=(
                "• Wähle eine Kategorie.\n"
                "• Beantworte die Fragen innerhalb des Zeitlimits.\n"
                "• Bei richtiger Antwort ist die Kategorie bestanden.\n"
                "• Bei falscher Antwort geht es zur nächsten Frage.\n"
                "• Sind alle Fragen falsch, ist die Kategorie fehlgeschlagen."
            ),
            justify="left"
        ).pack(anchor="w")

        ttk.Label(tab_desc, text="Spielbeschreibung (Beispieltext)", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))
        ttk.Label(
            tab_desc,
            text=(
                "Dieses Quiz basiert auf deinem bestehenden CLI-Projekt.\n"
                "Die GUI ist eine zusätzliche Schicht darüber und bedient die gleiche Logik."
            ),
            justify="left"
        ).pack(anchor="w")

        ttk.Label(tab_hint, text="Anforderungen / Hinweise", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))
        ttk.Label(
            tab_hint,
            text=(
                "• Logik und GUI sind getrennt (logic.py / gui.py).\n"
                "• Fehlermeldungen werden als Dialog angezeigt.\n"
                f"• Standard-Zeitlimit pro Frage: {self.time_limit_seconds} Sekunden (anpassbar in gui.py)."
            ),
            justify="left"
        ).pack(anchor="w")

        ttk.Button(win, text="Schließen", command=win.destroy).pack(pady=(0, 10))

    def _menu_new_quiz(self):
        if messagebox.askyesno("Bestätigung", "Neues Quiz starten? (Alles wird zurückgesetzt)"):
            self.engine.reset_all()
            self.show_start()

    def _menu_restart_quiz(self):
        # gleiche Wirkung wie "Neues Quiz starten", aber im Menü getrennt vorhanden
        if messagebox.askyesno("Bestätigung", "Quiz neu starten? (Alles wird zurückgesetzt)"):
            self.engine.reset_all()
            self.show_start()

    def _menu_quit(self):
        if messagebox.askyesno("Beenden", "Quiz wirklich beenden?"):
            self.root.destroy()

    # ----------------------------
    # QUIZ FRAME
    # ----------------------------
    def _build_quiz_frame(self):
        top = ttk.Frame(self.quiz_frame)
        top.pack(fill="x")

        ttk.Button(top, text="← Hauptmenü", command=self.show_start).pack(side="left")
        self.lbl_category = ttk.Label(top, text="", font=("Segoe UI", 14, "bold"))
        self.lbl_category.pack(side="left", padx=12)

        self.lbl_progress = ttk.Label(top, text="", font=("Segoe UI", 11))
        self.lbl_progress.pack(side="left")

        self.lbl_timer = ttk.Label(top, text="", font=("Segoe UI", 11, "bold"))
        self.lbl_timer.pack(side="right")

        # Content area
        content = ttk.Frame(self.quiz_frame, padding=(0, 12))
        content.pack(fill="both", expand=True)

        self.img_label = ttk.Label(content)
        self.img_label.pack(anchor="center", pady=(0, 8))

        self.lbl_question = ttk.Label(content, text="", wraplength=860, justify="left", font=("Segoe UI", 13))
        self.lbl_question.pack(anchor="w", pady=(0, 12))

        self.answer_area = ttk.Frame(content)
        self.answer_area.pack(fill="x")

        # For free text
        self.entry_answer = ttk.Entry(content)
        # not packed by default

        # Action buttons
        bottom = ttk.Frame(self.quiz_frame)
        bottom.pack(fill="x", pady=(8, 0))

        self.btn_submit = ttk.Button(bottom, text="Antwort prüfen", command=self._submit_current)
        self.btn_submit.pack(side="right")

        self.btn_next = ttk.Button(bottom, text="Next →", command=self._next_after_feedback)
        self.btn_next.pack(side="right", padx=(0, 8))
        self.btn_next.state(["disabled"])

        self.feedback = ttk.Label(self.quiz_frame, text="", foreground="#a00")
        self.feedback.pack(anchor="w", pady=(6, 0))

        # State for MC
        self.choice_var = tk.IntVar(value=0)
        self.choice_buttons = []

    def _render_question(self):
        self._cancel_timer()
        self.btn_next.state(["disabled"])
        self.feedback.config(text="")
        self.choice_var.set(0)
        self.current_image = None
        self.img_label.config(image="")

        kat = self.engine.selected_category
        q = self.engine.current_question()
        if kat is None or q is None:
            # nothing selected -> back
            self.show_start()
            return

        self.lbl_category.config(text=f"Kategorie: {kat.name}")
        self.lbl_progress.config(text=f"Frage {self.engine.question_progress()}")

        # Question text
        self.lbl_question.config(text=q.text)

        # Image (optional)
        self._try_render_image(getattr(q, "image_path", None))

        # Clear answer area
        for w in self.answer_area.winfo_children():
            w.destroy()
        self.choice_buttons = []
        self.entry_answer.pack_forget()

        # Build controls depending on question type
        if isinstance(q, Frage):
            for i, ans in enumerate(q.antworten, start=1):
                rb = tk.Radiobutton(
                    self.answer_area,
                    text=f"{i}. {ans}",
                    variable=self.choice_var,
                    value=i,
                    anchor="w",
                    justify="left",
                    padx=8,
                    pady=6
                )
                rb.pack(fill="x", pady=2)
                self.choice_buttons.append(rb)
        else:
            ttk.Label(self.answer_area, text="Deine Antwort:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 4))
            self.entry_answer.pack(fill="x", pady=(0, 4))
            self.entry_answer.delete(0, "end")

        # start timer
        self._start_timer(self.time_limit_seconds)

    def _try_render_image(self, image_path):
        if not image_path:
            return
        if Image is None or ImageTk is None:
            self.feedback.config(text="Hinweis: Pillow nicht verfügbar – Bild kann nicht angezeigt werden.")
            return
        try:
            img = Image.open(image_path)
            img.thumbnail((760, 240))
            self.current_image = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.current_image)
        except Exception:
            self.feedback.config(text="Hinweis: Bild konnte nicht geladen werden (Pfad/Format prüfen).")

    # ----------------------------
    # Timer
    # ----------------------------
    def _start_timer(self, seconds: int):
        self.remaining = seconds
        self._tick()

    def _tick(self):
        self.lbl_timer.config(text=f"⏱ {self.remaining:02d}s")
        if self.remaining <= 0:
            self._on_time_up()
            return
        self.remaining -= 1
        self.timer_after_id = self.root.after(1000, self._tick)

    def _cancel_timer(self):
        if self.timer_after_id is not None:
            try:
                self.root.after_cancel(self.timer_after_id)
            except Exception:
                pass
        self.timer_after_id = None

    def _on_time_up(self):
        self._cancel_timer()
        # Timeout zählt als falscher Versuch, automatisch nächste Frage / Ende
        res = self.engine.submit_answer(None, timed_out=True)
        messagebox.showinfo("Time is up", "Time is up! Nächste Frage…")
        if res.finished_category:
            self.show_results()
        else:
            self.root.after(200, self._render_question)

    # ----------------------------
    # Submit / Feedback / Next
    # ----------------------------
    def _submit_current(self):
        self._cancel_timer()
        q = self.engine.current_question()
        if q is None:
            return

        # Determine answer
        if isinstance(q, Frage):
            ans = self.choice_var.get()
            res = self.engine.submit_answer(ans, timed_out=False)
            self._mark_mc_feedback(res, q)
        else:
            ans = self.entry_answer.get()
            res = self.engine.submit_answer(ans, timed_out=False)
            self._mark_text_feedback(res)

        if res.correct:
            self.feedback.config(text="Richtig!", foreground="#0a0")
        else:
            self.feedback.config(text=res.message, foreground="#a00")

        # Next enabled after checking
        self.btn_next.state(["!disabled"])

        # If category finished, Next sends to results
        if res.finished_category:
            self.btn_next.config(text="Ergebnis →")
        else:
            self.btn_next.config(text="Next →")

    def _mark_mc_feedback(self, res, q: Frage):
        # reset colors
        for rb in self.choice_buttons:
            rb.config(bg=self.root.cget("bg"))

        correct = res.correct_choice_1_based or q.correct_choice_1_based()
        # mark correct green
        if 1 <= correct <= len(self.choice_buttons):
            self.choice_buttons[correct - 1].config(bg="#c7f5d0")

        # mark wrong selection red
        chosen = self.choice_var.get()
        if chosen and chosen != correct and 1 <= chosen <= len(self.choice_buttons):
            self.choice_buttons[chosen - 1].config(bg="#f7c5c5")

        if not res.correct and res.message and chosen == 0:
            messagebox.showerror("Fehler", res.message)

    def _mark_text_feedback(self, res):
        if not res.correct and res.message.startswith("Ungültige"):
            messagebox.showerror("Fehler", res.message)

    def _next_after_feedback(self):
        # If category finished -> results
        kat = self.engine.selected_category
        if kat is None:
            self.show_start()
            return
        if kat.status in ("completed", "failed"):
            self.show_results()
        else:
            self._render_question()

    # ----------------------------
    # RESULT FRAME
    # ----------------------------
    def _build_result_frame(self):
        header = ttk.Label(self.result_frame, text="Ergebnis", font=("Segoe UI", 18, "bold"))
        header.pack(anchor="w", pady=(0, 10))

        self.result_text = tk.Text(self.result_frame, height=16, wrap="word")
        self.result_text.pack(fill="both", expand=True)

        bottom = ttk.Frame(self.result_frame)
        bottom.pack(fill="x", pady=(10, 0))

        ttk.Button(bottom, text="Neustart", command=self._menu_new_quiz).pack(side="left")
        ttk.Button(bottom, text="Hauptmenü", command=self.show_start).pack(side="left", padx=8)
        ttk.Button(bottom, text="Beenden", command=self._menu_quit).pack(side="left")

        ttk.Button(bottom, text="Show Results", command=self.show_results).pack(side="right")

    def _render_results(self):
        s = self.engine.summary()

        total_correct = s["score_total"]
        total_attempts = s["attempts_total"]
        total_failed = s["failed_total"]
        percent = s["percent_total"]

        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", f"Gesamtpunktzahl: {total_correct}\n")
        self.result_text.insert("end", f"Anzahl richtiger Antworten: {total_correct}\n")
        self.result_text.insert("end", f"Anzahl falscher Antworten: {total_failed}\n")
        self.result_text.insert("end", f"Gesamtversuche: {total_attempts}\n")
        self.result_text.insert("end", f"Prozentuale Auswertung: {percent}%\n\n")

        self.result_text.insert("end", "— Auswertung nach Kategorie —\n")
        for c in s["by_category"]:
            self.result_text.insert(
                "end",
                f"{c['name']}: Score={c['score']}, Versuche={c['attempts']}, Falsch={c['failed_attempts']}, "
                f"Status={c['status']}, Quote={c['percent']}%\n"
            )
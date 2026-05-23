import tkinter as tk
from tkinter import ttk, messagebox

from src.logic import QuizEngine, DEFAULT_TIME_LIMIT_SECONDS
from src.question import Frage
from src.frage_ohne_index import FrageOhneIndex


class QuizGUI:
    def __init__(self, root: tk.Tk, engine: QuizEngine, time_limit_seconds: int = DEFAULT_TIME_LIMIT_SECONDS):
        self.root = root
        self.engine = engine
        self.time_limit_seconds = time_limit_seconds

        self.root.title("Quiz (GUI)")
        self.root.geometry("1040x720")
        self.root.minsize(980, 680)
        self.root.configure(bg="#f4f7fb")

        # Theme / Style
        self._apply_theme()

        self.main = ttk.Frame(self.root, padding=18, style="Main.TFrame")
        self.main.pack(fill="both", expand=True)

        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0, bd=0, bg="#f4f7fb")
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.main.tkraise()
        self.root.bind("<Configure>", self._on_root_configure)

        # Navigation / State
        self.timer_after_id = None
        self.remaining = 0

        # UI Frames
        self.start_frame = ttk.Frame(self.main)
        self.quiz_frame = ttk.Frame(self.main)
        self.result_frame = ttk.Frame(self.main)

        self.category_bg_canvas = None

        self._build_start_frame()
        self._build_quiz_frame()
        self._build_result_frame()

        self.root.update_idletasks()
        self._draw_background_pattern()
        self.show_start()

    def _apply_theme(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("Main.TFrame", background="#f4f7fb")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Accent.TButton", background="#60a5fa", foreground="#0b1120", font=("Segoe UI", 11, "bold"), padding=(18, 10), relief="flat")
        style.configure("Neutral.TButton", background="#e0e7ff", foreground="#0b1120", font=("Segoe UI", 11, "bold"), padding=(16, 10), relief="flat")
        style.configure("Completed.TButton", background="#cbd5e1", foreground="#475569", font=("Segoe UI", 11, "bold"), padding=(18, 10), relief="flat")
        style.configure("Danger.TButton", background="#ef4444", foreground="#ffffff", font=("Segoe UI", 11, "bold"), padding=(16, 10), relief="flat")

        style.configure("TLabel", background="#f4f7fb", foreground="#0f172a")
        style.configure("TButton", font=("Segoe UI", 11), padding=(16, 10))
        style.configure("TFrame", background="#f4f7fb")
        style.configure("TEntry", fieldbackground="#ffffff", background="#ffffff", borderwidth=1)
        style.configure("Correct.TEntry", fieldbackground="#dcfce7", background="#dcfce7", borderwidth=1)
        style.configure("Incorrect.TEntry", fieldbackground="#fee2e2", background="#fee2e2", borderwidth=1)

        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#eef2ff", relief="flat")
        style.map("Treeview.Heading", background=[("active", "#dbeafe")])
        style.map("Accent.TButton", background=[("active", "#2563eb")], foreground=[("!disabled", "#ffffff")])
        style.map("Neutral.TButton", background=[("active", "#bfdbfe")], foreground=[("!disabled", "#0f172a")])
        style.map("Danger.TButton", background=[("active", "#dc2626")], foreground=[("!disabled", "#ffffff")])

    def _on_root_configure(self, event):
        if event.widget == self.root:
            self._draw_background_pattern()

    def _draw_background_pattern(self):
        self.bg_canvas.delete("all")
        w = max(self.root.winfo_width(), 1)
        h = max(self.root.winfo_height(), 1)

        self.bg_canvas.create_rectangle(0, 0, w, h, fill="#f6f8fd", outline="")
        for y in range(0, h, 90):
            shade = "#eef4ff" if (y // 90) % 2 == 0 else "#f9fbff"
            self.bg_canvas.create_rectangle(0, y, w, y + 60, fill=shade, outline="")
        blobs = [
            (110, 90, 52, "#e8eaff"),
            (305, 150, 76, "#e0f2fe"),
            (700, 170, 64, "#fce7f3"),
            (185, 430, 78, "#dcfce7"),
            (550, 360, 48, "#fef3c7"),
            (820, 470, 56, "#e0e7ff"),
            (930, 120, 40, "#f5f3ff"),
        ]
        for x, y, r, color in blobs:
            self.bg_canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")

        for x in range(0, w, 130):
            self.bg_canvas.create_line(x, 0, x + 45, h, fill="#dbe9ff", width=1)
        for x in range(0, w, 130):
            self.bg_canvas.create_line(x, 0, x + 45, h, fill="#dbe9ff", width=1)
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
        top = ttk.Frame(self.start_frame, style="Card.TFrame", padding=12)
        top.pack(fill="x")

        btn_menu = ttk.Menubutton(top, text="Menü")
        btn_menu.pack(side="left", padx=(0, 8))

        menu = tk.Menu(btn_menu, tearoff=0)
        menu.add_command(label="Quiz neu starten", command=self._menu_restart_quiz)
        menu.add_separator()
        menu.add_command(label="Quiz beenden", command=self._menu_quit)
        btn_menu["menu"] = menu

        btn_infos = ttk.Button(top, text="Infos", command=self._open_infos, style="Neutral.TButton")
        btn_infos.pack(side="left")

        # Header
        header = ttk.Label(self.start_frame, text="Kategorien auswählen", font=("Segoe UI", 20, "bold"), foreground="#1d4ed8")
        header.pack(anchor="w", pady=(16, 6))

        self.score_label = ttk.Label(self.start_frame, text="", font=("Segoe UI", 11), foreground="#334155")
        self.score_label.pack(anchor="w", pady=(0, 6))

        # Categories area
        self.cat_container = ttk.Frame(self.start_frame, padding=(30, 28, 30, 28))
        self.cat_container.pack(fill="both", expand=True, pady=(8, 0))

        bottom = ttk.Frame(self.start_frame)
        bottom.pack(fill="x", pady=(8, 0))

        self.btn_show_results = ttk.Button(bottom, text="Ergebnisse anzeigen", command=self.show_results, style="Accent.TButton")
        self.btn_show_results.pack(side="right")

    def _refresh_start_categories(self):
        for w in self.cat_container.winfo_children():
            if w is not self.category_bg_canvas:
                w.destroy()

        if self.category_bg_canvas is not None:
            self.category_bg_canvas.destroy()
            self.category_bg_canvas = None

        self.category_bg_canvas = tk.Canvas(self.cat_container, highlightthickness=0, bd=0, bg="#eef4ff")
        self.category_bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.category_bg_canvas.bind("<Configure>", self._on_category_bg_configure)
        self._draw_category_pattern()

        # Update stats label
        summary = self.engine.summary()
        self.score_label.config(
            text=f"Aktueller Punktestand: {summary['score_total']} | Gesamtversuche: {summary['gesamt_versuche_engine']}"
        )

        # Categories grid
        cats = self.engine.category_list()

        grid_frame = ttk.Frame(self.cat_container)
        grid_frame.place(relx=0.5, rely=0.5, anchor="center")

        cols = 2
        grid_frame.columnconfigure(0, weight=1, minsize=320)
        grid_frame.columnconfigure(1, weight=1, minsize=320)

        for i, cat in enumerate(cats):
            r = i // cols
            c = i % cols

            card = ttk.Frame(grid_frame, padding=20, style="Card.TFrame", width=320, height=200)
            card.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
            card.grid_propagate(False)

            title = ttk.Label(card, text=cat.name, font=("Segoe UI", 14, "bold"), foreground="#1d4ed8")
            title.pack(anchor="w")

            meta = ttk.Label(
                card,
                text=f"Punkte: {cat.score} | Versuche: {cat.attempts} | Status: {cat.status}",
                font=("Segoe UI", 10),
                foreground="#475569"
            )
            meta.pack(anchor="w", pady=(3, 14))

            button_style = "Completed.TButton" if cat.status != "pending" else "Accent.TButton"
            btn = ttk.Button(card, text="Kategorie starten", command=lambda idx=i: self._start_category(idx), style=button_style)
            btn.pack(anchor="center", fill="x", pady=(8, 0))

            if cat.status != "pending":
                btn.state(["disabled"])

        for r in range((len(cats) + cols - 1) // cols):
            grid_frame.rowconfigure(r, weight=1, minsize=220)

    def _on_category_bg_configure(self, event):
        if event.widget == self.category_bg_canvas:
            self._draw_category_pattern()

    def _draw_category_pattern(self):
        if self.category_bg_canvas is None:
            return

        self.category_bg_canvas.delete("all")
        w = max(self.cat_container.winfo_width(), 1)
        h = max(self.cat_container.winfo_height(), 1)

        self.category_bg_canvas.create_rectangle(0, 0, w, h, fill="#eef4ff", outline="")

        for x in range(0, w, 110):
            self.category_bg_canvas.create_line(x, 0, x + 50, h, fill="#dbeafe", width=1)

        for y in range(0, h, 110):
            self.category_bg_canvas.create_line(0, y, w, y + 40, fill="#e0f2fe", width=1)

        blobs = [
            (80, 70, 40, "#f5f3ff"),
            (220, 120, 56, "#dbeafe"),
            (360, 240, 42, "#e0f2fe"),
            (580, 180, 48, "#fef3c7"),
            (720, 320, 54, "#eef2ff"),
        ]
        for x, y, r, color in blobs:
            self.category_bg_canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")

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
        win.geometry("660x460")
        win.minsize(620, 420)
        win.configure(bg="#f4f7fb")
        win.transient(self.root)

        nb = ttk.Notebook(win)
        nb.pack(fill="both", expand=True, padx=16, pady=(16, 10))

        tab_rules = ttk.Frame(nb, padding=16)
        tab_desc = ttk.Frame(nb, padding=16)
        tab_hint = ttk.Frame(nb, padding=16)

        nb.add(tab_rules, text="Regeln")
        nb.add(tab_desc, text="Spielbeschreibung")
        nb.add(tab_hint, text="Hinweise")

        ttk.Label(tab_rules, text="Regeln", font=("Segoe UI", 13, "bold"), foreground="#1d4ed8").pack(anchor="w", pady=(0, 8))
        ttk.Label(
            tab_rules,
            text=(
                "• Wähle eine Kategorie im Hauptmenü aus.\n"
                "• Jede Kategorie kann nur einmal gespielt werden.\n"
                "• Beantworte die Fragen in der gewählten Kategorie.\n"
                "• Für jede Frage steht ein Zeitlimit zur Verfügung.\n"
                "• Eine richtige Antwort beendet die Kategorie erfolgreich.\n"
                "• Eine falsche Antwort führt zur nächsten Frage.\n"
                "• Wenn alle Fragen falsch beantwortet werden, gilt die Kategorie als nicht bestanden."
            ),
            justify="left",
            foreground="#334155",
            wraplength=560
        ).pack(anchor="w")

        ttk.Label(tab_desc, text="Spielbeschreibung", font=("Segoe UI", 13, "bold"), foreground="#1d4ed8").pack(anchor="w", pady=(0, 8))
        ttk.Label(
            tab_desc,
            text=(
                "Dieses Quiz ist ein Wissensspiel mit verschiedenen Themenbereichen wie Programmierung, Wirtschaft und Allgemeinwissen.\n\n"
                "Du testest dein Wissen, indem du Fragen beantwortest und Entscheidungen unter Zeitdruck triffst. Ziel ist es, möglichst viele Kategorien erfolgreich abzuschließen und ein gutes Ergebnis zu erreichen."
            ),
            justify="left",
            foreground="#334155",
            wraplength=560
        ).pack(anchor="w")

        ttk.Label(tab_hint, text="Hinweise", font=("Segoe UI", 13, "bold"), foreground="#1d4ed8").pack(anchor="w", pady=(0, 8))
        ttk.Label(
            tab_hint,
            text=(
                "• Lies jede Frage aufmerksam.\n"
                "• Achte auf das Zeitlimit und entscheide rechtzeitig.\n"
                "• Nutze dein Wissen und schließe falsche Antworten aus.\n"
                "• Jede Kategorie kann nur einmal gespielt werden."
            ),
            justify="left",
            foreground="#334155",
            wraplength=560
        ).pack(anchor="w")

        footer = ttk.Frame(win)
        footer.pack(fill="x", padx=16, pady=(0, 16))
        ttk.Button(footer, text="Schließen", command=win.destroy, style="Neutral.TButton").pack(anchor="e")

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
        top = ttk.Frame(self.quiz_frame, style="Card.TFrame", padding=12)
        top.pack(fill="x")

        ttk.Button(top, text="← Hauptmenü", command=self.show_start, style="Neutral.TButton").pack(side="left")
        self.lbl_category = ttk.Label(top, text="", font=("Segoe UI", 14, "bold"), foreground="#1d4ed8")
        self.lbl_category.pack(side="left", padx=12)

        self.lbl_progress = ttk.Label(top, text="", font=("Segoe UI", 11), foreground="#475569")
        self.lbl_progress.pack(side="left")

        self.lbl_timer = ttk.Label(top, text="", font=("Segoe UI", 16, "bold"), foreground="#1d4ed8")
        self.lbl_timer.pack(side="right")

        # Content area
        content = ttk.Frame(self.quiz_frame, padding=(0, 12))
        content.pack(fill="both", expand=True)

        self.lbl_question = ttk.Label(content, text="", wraplength=860, justify="left", font=("Segoe UI", 13), foreground="#0f172a")
        self.lbl_question.pack(anchor="w", pady=(0, 12))

        self.answer_area = ttk.Frame(content, style="Card.TFrame")
        self.answer_area.pack(fill="x", padx=2, pady=4)

        # For free text
        self.entry_answer = ttk.Entry(content)
        # not packed by default

        # Action buttons
        bottom = ttk.Frame(self.quiz_frame)
        bottom.pack(fill="x", pady=(8, 0))

        self.btn_submit = ttk.Button(bottom, text="Antwort prüfen", command=self._submit_current, style="Accent.TButton")
        self.btn_submit.pack(side="right")

        self.btn_next = ttk.Button(bottom, text="Weiter →", command=self._next_after_feedback, style="Accent.TButton")
        self.btn_next.pack(side="right", padx=(0, 8))
        self.btn_next.state(["disabled"])

        self.feedback = ttk.Label(self.quiz_frame, text="", foreground="#a00")
        self.feedback.pack(anchor="w", pady=(6, 0))

        # State for MC
        self.choice_var = tk.IntVar(value=0)
        self.choice_buttons = []

    def _reset_text_input_style(self):
        if hasattr(self, "entry_answer"):
            self.entry_answer.configure(style="TEntry")

    def _set_text_input_result(self, correct: bool):
        if hasattr(self, "entry_answer"):
            self.entry_answer.configure(style="Correct.TEntry" if correct else "Incorrect.TEntry")

    def _render_question(self):
        self._cancel_timer()
        self.btn_next.state(["disabled"])
        self.feedback.config(text="")
        self.choice_var.set(0)
        self._reset_text_input_style()

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
        messagebox.showinfo("Zeit abgelaufen", "Zeit abgelaufen! Nächste Frage…")
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

        # Next enabled after checking
        self.btn_next.state(["!disabled"])

        # If category finished, Next sends to results
        if res.finished_category:
            self.btn_next.config(text="Ergebnis →")
        else:
            self.btn_next.config(text="Weiter →")

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

    def _mark_text_feedback(self, res):
        if res.correct:
            self._set_text_input_result(True)
            self.feedback.config(text="Richtige Antwort!", foreground="#166534")
            return

        self._set_text_input_result(False)
        if res.message.startswith("Ungültige"):
            self.feedback.config(text=res.message, foreground="#991b1b")
            messagebox.showerror("Fehler", res.message)
            return

        self.feedback.config(text=res.message, foreground="#991b1b")

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
        header = ttk.Label(self.result_frame, text="Ergebnis", font=("Segoe UI", 20, "bold"), foreground="#1d4ed8")
        header.pack(anchor="w", pady=(0, 10))

        summary_frame = ttk.Frame(self.result_frame, style="Card.TFrame", padding=12)
        summary_frame.pack(fill="x", pady=(0, 10))

        self.summary_label = ttk.Label(
            summary_frame,
            text="",
            justify="left",
            font=("Segoe UI", 11),
            anchor="w",
            foreground="#334155",
        )
        self.summary_label.pack(anchor="w")

        table_frame = ttk.Frame(self.result_frame)
        table_frame.pack(fill="both", expand=True)

        self.result_tree = ttk.Treeview(
            table_frame,
            columns=("category", "score", "attempts", "failed", "status", "percent"),
            show="headings",
            height=8,
            selectmode="browse",
        )
        self.result_tree.pack(side="left", fill="both", expand=True)

        self.result_tree.heading("category", text="Kategorie")
        self.result_tree.heading("score", text="Punkte")
        self.result_tree.heading("attempts", text="Versuche")
        self.result_tree.heading("failed", text="Falsch")
        self.result_tree.heading("status", text="Status")
        self.result_tree.heading("percent", text="Prozent")

        self.result_tree.column("category", width=230, minwidth=180, anchor="w")
        self.result_tree.column("score", width=90, minwidth=80, anchor="center")
        self.result_tree.column("attempts", width=90, minwidth=80, anchor="center")
        self.result_tree.column("failed", width=90, minwidth=80, anchor="center")
        self.result_tree.column("status", width=120, minwidth=110, anchor="center")
        self.result_tree.column("percent", width=90, minwidth=80, anchor="center")

        self.result_tree.tag_configure("even", background="#f8fafc")
        self.result_tree.tag_configure("odd", background="#ffffff")

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.result_tree.yview)
        y_scroll.pack(side="right", fill="y")
        self.result_tree.configure(yscrollcommand=y_scroll.set)

        bottom = ttk.Frame(self.result_frame)
        bottom.pack(fill="x", pady=(10, 0))

        ttk.Button(bottom, text="Neustart", command=self._menu_new_quiz, style="Neutral.TButton").pack(side="left")
        ttk.Button(bottom, text="Hauptmenü", command=self.show_start, style="Neutral.TButton").pack(side="left", padx=8)
        ttk.Button(bottom, text="Beenden", command=self._menu_quit, style="Danger.TButton").pack(side="left")

        ttk.Button(bottom, text="Ergebnisse anzeigen", command=self.show_results, style="Accent.TButton").pack(side="right")


    def _render_results(self):
        s = self.engine.summary()

        total_correct = s["score_total"]
        total_attempts = s["attempts_total"]
        total_failed = s["failed_total"]
        percent = s["percent_total"]

        self.summary_label.config(
            text=(
                f"Gesamtpunktzahl: {total_correct} · Richtige Antworten: {total_correct} · "
                f"Falsche Antworten: {total_failed} · Gesamtversuche: {total_attempts} · "
                f"Auswertung: {percent}%"
            )
        )

        for row in self.result_tree.get_children():
            self.result_tree.delete(row)

        by_category = s["by_category"]
        self.result_tree.configure(height=min(len(by_category), 8))

        for idx, c in enumerate(by_category):
            self.result_tree.insert(
                "",
                "end",
                values=(
                    c["name"],
                    c["score"],
                    c["attempts"],
                    c["failed_attempts"],
                    c["status"],
                    f"{c['percent']}%",
                ),
                tags=("even" if idx % 2 == 0 else "odd",),
            )


import tkinter as tk

from src.logic import QuizEngine, build_categories
from src.gui import QuizGUI


def main():
    categories = build_categories()
    engine = QuizEngine(categories)

    root = tk.Tk()
    QuizGUI(root, engine)
    root.mainloop()


if __name__ == "__main__":
    main()
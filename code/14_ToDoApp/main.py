import os
import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def time_diff(start, end):
    fmt = "%Y-%m-%d %H:%M"
    
    start_dt = datetime.strptime(start, fmt)
    end_dt = datetime.strptime(end, fmt)
    
    delta = end_dt - start_dt
    return delta


# -------------------- MODEL --------------------
class Note:
    def __init__(self, id, text, created_at, done_at, completed):
        self.id = id
        self.text = text
        self.created_at = created_at
        self.done_at = done_at
        self.completed = completed

    def short_text(self, length=30):
        return self.text if len(self.text) <= length else self.text[:length] + "..."


# -------------------- DATABASE --------------------
class Database:
    def __init__(self, db_name="notes.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            created_at TEXT,
            done_at TEXT,
            completed INTEGER
        )
        """)

    def add_note(self, text):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        done_at = ""
        self.conn.execute(
            "INSERT INTO notes (text, created_at, done_at, completed) VALUES (?, ?, ?, 0)",
            (text, now, done_at)
        )
        self.conn.commit()

    def delete_note(self, note_id):
        self.conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
        self.conn.commit()

    def toggle_complete(self, note_id):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.conn.execute("""
            UPDATE notes
            SET completed = 1,
                done_at = ?
            WHERE id=?
        """, (now, note_id))
        self.conn.commit()

    def get_notes(self):
        cursor = self.conn.execute("SELECT id, text, created_at, done_at, completed FROM notes")
        return [Note(*row) for row in cursor.fetchall()]


# -------------------- UI --------------------
class App:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("To-Do App")

        # Input
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        self.add_btn = tk.Button(root, text="Add", command=self.add_note)
        self.add_btn.pack()

        # List
        self.tree = ttk.Treeview(root, columns=("date", "text", "time", "done"), show="headings")
        self.tree.heading("date", text="Date", command=lambda: self.sort_by("date"))
        self.tree.heading("text", text="Text", command=lambda: self.sort_by("text"))
        self.tree.heading("time", text="Time", command=lambda: self.sort_by("time"))
        self.tree.heading("done", text="Done", command=lambda: self.sort_by("done"))

        self.tree.pack(pady=10)

        # Buttons
        self.delete_btn = tk.Button(root, text="Delete", command=self.delete_note)
        self.delete_btn.pack()

        self.toggle_btn = tk.Button(root, text="Toggle Complete", command=self.toggle_complete)
        self.toggle_btn.pack()

        self.refresh()

    def sort_by(self, column):
        notes = self.db.get_notes()
        if column == "date":
            notes.sort(key=lambda n: n.created_at)
        elif column == "text":
            notes.sort(key=lambda n: n.text)
        elif column == "time":
            notes.sort(key=lambda n: time_diff(n.created_at, n.done_at if n.completed else datetime.now().strftime("%Y-%m-%d %H:%M")))
        elif column == "done":
            notes.sort(key=lambda n: n.completed)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for note in notes:
            self.tree.insert(
                "",
                "end",
                iid=note.id,
                values=(
                    note.created_at, 
                    note.short_text(),
                    time_diff(note.created_at,
                              note.done_at if note.completed else \
                                datetime.now().strftime("%Y-%m-%d %H:%M")),
                    f"✔ {note.done_at}" if note.completed else "-"
                )
            )
            
    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for note in self.db.get_notes():
            self.tree.insert(
                "",
                "end",
                iid=note.id,
                values=(
                    note.created_at, 
                    note.short_text(),
                    time_diff(note.created_at,
                              note.done_at if note.completed else \
                                datetime.now().strftime("%Y-%m-%d %H:%M")),
                    f"✔ {note.done_at}" if note.completed else "-"
                )
            )

    def add_note(self):
        text = self.entry.get()
        if text:
            self.db.add_note(text)
            self.entry.delete(0, tk.END)
            self.refresh()

    def delete_note(self):
        selected = self.tree.selection()
        if selected:
            self.db.delete_note(int(selected[0]))
            self.refresh()

    def toggle_complete(self):
        selected = self.tree.selection()
        if selected:
            self.db.toggle_complete(int(selected[0]))
            self.refresh()


# -------------------- RUN --------------------
root = tk.Tk()
app = App(root)
root.mainloop()
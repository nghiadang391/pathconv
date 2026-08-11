"""Tkinter desktop front-end for pathconv."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import List

from .config import load_config, resolve_config_path, save_config
from .core import TO_UNIX, TO_WINDOWS, Mapping, convert


class MappingEditor(tk.Toplevel):
    """Modal dialog to add/edit/remove mapping pairs, saved to the config."""

    def __init__(self, parent: "ConverterApp", mappings: List[Mapping]):
        super().__init__(parent)
        self.title("Edit mappings")
        self.parent = parent
        self.transient(parent)
        self.grab_set()

        self.tree = ttk.Treeview(
            self, columns=("windows", "unix"), show="headings", height=8
        )
        self.tree.heading("windows", text="Windows prefix")
        self.tree.heading("unix", text="Unix prefix")
        self.tree.column("windows", width=320)
        self.tree.column("unix", width=220)
        self.tree.grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="nsew")
        for m in mappings:
            self.tree.insert("", "end", values=(m.windows_prefix, m.unix_prefix))

        tk.Label(self, text="Windows:").grid(row=1, column=0, sticky="e")
        self.win_entry = tk.Entry(self, width=48)
        self.win_entry.grid(row=1, column=1, columnspan=3, padx=4, pady=2, sticky="we")
        tk.Label(self, text="Unix:").grid(row=2, column=0, sticky="e")
        self.unix_entry = tk.Entry(self, width=48)
        self.unix_entry.grid(row=2, column=1, columnspan=3, padx=4, pady=2, sticky="we")

        tk.Button(self, text="Add / Update", command=self._add).grid(
            row=3, column=0, padx=4, pady=6
        )
        tk.Button(self, text="Remove selected", command=self._remove).grid(
            row=3, column=1, padx=4, pady=6
        )
        tk.Button(self, text="Save", command=self._save).grid(
            row=3, column=2, padx=4, pady=6
        )
        tk.Button(self, text="Cancel", command=self.destroy).grid(
            row=3, column=3, padx=4, pady=6
        )

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def _on_select(self, _event=None) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        win, unix = self.tree.item(sel[0], "values")
        self.win_entry.delete(0, tk.END)
        self.win_entry.insert(0, win)
        self.unix_entry.delete(0, tk.END)
        self.unix_entry.insert(0, unix)

    def _add(self) -> None:
        win = self.win_entry.get().strip()
        unix = self.unix_entry.get().strip()
        if not win or not unix:
            messagebox.showwarning("Missing", "Both prefixes are required.", parent=self)
            return
        # Update in place if the Windows prefix already exists, else append.
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[0] == win:
                self.tree.item(item, values=(win, unix))
                return
        self.tree.insert("", "end", values=(win, unix))

    def _remove(self) -> None:
        for item in self.tree.selection():
            self.tree.delete(item)

    def _save(self) -> None:
        mappings = [
            Mapping(windows_prefix=v[0], unix_prefix=v[1])
            for v in (self.tree.item(i, "values") for i in self.tree.get_children())
        ]
        save_config(mappings, self.parent.config_path)
        self.parent.mappings = mappings
        self.parent.convert()
        self.destroy()


class ConverterApp(tk.Tk):
    def __init__(self, config_path: str = None):
        super().__init__()
        self.title("Path Converter — Unix <-> Windows")
        self.config_path = config_path
        self.mappings = load_config(config_path)

        pad = {"padx": 8, "pady": 4}

        tk.Label(self, text="Input path(s):").grid(row=0, column=0, sticky="w", **pad)
        self.input = tk.Text(self, width=72, height=5)
        self.input.grid(row=1, column=0, columnspan=4, sticky="nsew", **pad)

        # Options row.
        self.use_mapping = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self, text="Apply directory mapping", variable=self.use_mapping,
            command=self.convert,
        ).grid(row=2, column=0, sticky="w", **pad)

        self.direction = tk.StringVar(value="auto")
        for i, (label, val) in enumerate(
            [("Auto", "auto"), ("-> Unix", TO_UNIX), ("-> Windows", TO_WINDOWS)]
        ):
            tk.Radiobutton(
                self, text=label, variable=self.direction, value=val,
                command=self.convert,
            ).grid(row=2, column=1 + i, sticky="w", **pad)

        tk.Button(self, text="Convert", command=self.convert).grid(
            row=3, column=0, sticky="w", **pad
        )
        tk.Button(self, text="Copy result", command=self.copy_result).grid(
            row=3, column=1, sticky="w", **pad
        )
        tk.Button(self, text="Edit mappings...", command=self.edit_mappings).grid(
            row=3, column=2, sticky="w", **pad
        )

        tk.Label(self, text="Result:").grid(row=4, column=0, sticky="w", **pad)
        self.output = tk.Text(self, width=72, height=5, state="disabled")
        self.output.grid(row=5, column=0, columnspan=4, sticky="nsew", **pad)

        cfg = resolve_config_path(config_path)
        tk.Label(self, text=f"config: {cfg}", fg="gray").grid(
            row=6, column=0, columnspan=4, sticky="w", **pad
        )

        # Let the text boxes grow/shrink with the window; other rows stay fixed.
        self.rowconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)
        for col in range(4):
            self.columnconfigure(col, weight=1)

        # Live conversion as the user types.
        self.input.bind("<KeyRelease>", lambda _e: self.convert())

    def _direction_arg(self):
        val = self.direction.get()
        return None if val == "auto" else val

    def convert(self) -> None:
        text = self.input.get("1.0", tk.END).rstrip("\n")
        lines = text.split("\n") if text else [""]
        results = [
            convert(
                line,
                mappings=self.mappings,
                use_mapping=self.use_mapping.get(),
                direction=self._direction_arg(),
            )
            for line in lines
        ]
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", "\n".join(results))
        self.output.config(state="disabled")

    def copy_result(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(self.output.get("1.0", tk.END).rstrip("\n"))

    def edit_mappings(self) -> None:
        MappingEditor(self, self.mappings)


def main() -> int:
    app = ConverterApp()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

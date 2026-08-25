# pathconv — Unix ↔ Windows path converter

Convert file paths between Windows and Unix conventions. Handles `\` ↔ `/`,
UNC (`\\server\share`) and drive (`C:`) prefixes, and an **optional**
configurable *prefix mapping* between a network-share root and a mount point.

Ships as a desktop GUI and a CLI. Pure Python 3 + Tkinter — no external
dependencies, works on Windows and Linux.

## Why

Standard tools (`cygpath`, `wslpath`, `pathlib`) handle separators and UNC
mechanics but can't rewrite an arbitrary share root to a mount point, e.g.:

```
\\fileserver01.example.com\Project\prj_example\...   (Windows)
/mnt/project/prj_example/...                            (Ubuntu)
```

The prefix mapping is toggleable: turn it **off** and only separators are
swapped.

## Install

The simplest install is [pipx](https://pipx.pypa.io), which puts the commands
on your PATH in an isolated environment:

```bash
pipx install pathconv
```

Don't have pipx yet? Install it once (using an explicit `python3` avoids any
`pip`/`pip3` ambiguity):

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Plain `pip` works too (`pip install pathconv`), and for local development use
`pip install -e .`. Either way you get two commands, `pathconv` (CLI) and
`pathconv-gui` (GUI). Without installing, you can still run everything via
`python -m pathconv.cli` / `python -m pathconv.gui`.

## Double-click launch (GUI)

To open the GUI by double-clicking instead of typing a command, use the files
in [`launchers/`](launchers):

- **Windows:** double-click `pathconv-gui.bat` (or `pathconv-gui.pyw` for no
  console window). Right-click either → *Send to → Desktop (create shortcut)*
  for a desktop icon. This assumes Python + pathconv are installed.
- **Linux:** copy `pathconv-gui.desktop` into `~/.local/share/applications/`
  (and/or `~/Desktop/`) so it appears in your app menu and is double-clickable
  in the file manager. It runs the installed `pathconv-gui` command.

The GUI needs Tkinter. It ships with the python.org installers and on Windows,
but some Linux distros package it separately (e.g. `sudo apt install
python3-tk`).

## CLI

```bash
pathconv "\\fileserver01.example.com\Project\prj_example\x"
# -> /mnt/project/prj_example/x

pathconv --to-windows "/mnt/project/prj_example/x"
# -> \\fileserver01.example.com\Project\prj_example\x

pathconv --no-map "C:\a\b\c"   # -> C:/a/b/c  (separators only)
pathconv --list                # show configured mappings
echo "C:\a\b" | pathconv       # reads stdin, one path per line
```

(Not installed? Replace `pathconv` with `python -m pathconv.cli`.)

Direction is auto-detected (a `\`, drive letter, or `\\` means Windows input);
force it with `--to-unix` / `--to-windows`.

## GUI

```bash
pathconv-gui
# or, without installing: python -m pathconv.gui
```

- Input/output boxes with live conversion as you type.
- **"Apply directory mapping"** checkbox (the toggle).
- Direction: Auto / → Unix / → Windows.
- "Edit mappings…" to add/edit/remove share↔mount pairs.

## Configuration

Mappings live in a JSON file shared by the CLI and GUI:

- Linux: `~/.config/pathconv/mappings.json` (or `$XDG_CONFIG_HOME`)
- Windows: `%APPDATA%\pathconv\mappings.json`
- Override with `--config PATH` or the `PATHCONV_CONFIG` env var.

```json
{
  "mappings": [
    {
      "windows_prefix": "\\\\fileserver01.example.com\\Project",
      "unix_prefix": "/mnt/project"
    }
  ]
}
```

The Windows prefix is matched case-insensitively; the longest matching prefix
wins.

## Tests

```bash
python -m unittest discover -s tests
```

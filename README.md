# pathconv — Unix ↔ Windows path converter

Convert paths between Windows and Unix. Swaps `\` ↔ `/`, handles UNC
(`\\server\share`) and drive (`C:`) prefixes, and optionally rewrites a
network-share root to its mount point:

```
\\fileserver01.example.com\Project\prj_example\x   (Windows)
/mnt/project/prj_example/x                          (Unix)
```

Turn the prefix mapping off and only separators are swapped. Pure Python 3 +
Tkinter, no dependencies, runs on Windows and Linux.

## Install

```bash
pipx install pathconv
```

No pipx? Install it once — the `python3 -m` form avoids `pip`/`pip3`
ambiguity:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

`pip install pathconv` also works (`pip install -e .` for development). Either
way you get two commands: `pathconv` (CLI) and `pathconv-gui` (GUI). Or skip
installing and run `python -m pathconv.cli` / `python -m pathconv.gui`.

## Double-click the GUI

Launchers live in [`launchers/`](launchers):

- **Windows:** double-click `pathconv-gui.bat` (or `pathconv-gui.pyw` for no
  console window). Right-click → *Send to → Desktop* for an icon.
- **Linux:** copy `pathconv-gui.desktop` into
  `~/.local/share/applications/` (or `~/Desktop/`).

Both need Python + pathconv installed. The GUI also needs Tkinter — bundled on
Windows and python.org builds, but `sudo apt install python3-tk` on some
distros.

## CLI

```bash
pathconv "\\fileserver01.example.com\Project\x"   # -> /mnt/project/x
pathconv --to-windows "/mnt/project/x"            # force direction
pathconv --no-map "C:\a\b\c"                      # separators only -> C:/a/b/c
pathconv --list                                   # show mappings
echo "C:\a\b" | pathconv                          # one path per line from stdin
```

Direction auto-detects (`\`, a drive letter, or `\\` means Windows input);
force it with `--to-unix` / `--to-windows`. Not installed? Use
`python -m pathconv.cli`.

## GUI

Input/output boxes with live conversion (result auto-copied to the clipboard),
an "Apply directory mapping" toggle, Auto / → Unix / → Windows direction, and
"Edit mappings…" to manage share↔mount pairs.

## Configuration

Mappings are stored as JSON, shared by CLI and GUI:

- Linux: `~/.config/pathconv/mappings.json` (or `$XDG_CONFIG_HOME`)
- Windows: `%APPDATA%\pathconv\mappings.json`
- Override with `--config PATH` or `PATHCONV_CONFIG`.

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

Windows prefixes match case-insensitively; the longest match wins. Seeded with
a default on first run.

## Tests

```bash
python -m unittest discover -s tests
```

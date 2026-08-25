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

Requires Python 3.8+. Install straight from GitHub with
[pipx](https://pipx.pypa.io) (isolated, puts the commands on your PATH):

```bash
pipx install git+https://github.com/nghiadang391/pathconv.git
```

Or with plain pip:

```bash
pip install git+https://github.com/nghiadang391/pathconv.git
```

From a local clone (for development or offline install):

```bash
git clone https://github.com/nghiadang391/pathconv.git
cd pathconv
pip install .          # or: pip install -e .  (editable, for development)
```

Either way you get two commands: `pathconv-cli` (CLI) and `pathconv` (GUI).

Don't have pipx? Install it once, then reopen your terminal (use `python3` on
Linux/macOS, `python` on Windows):

```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

## CLI

```bash
pathconv-cli "\\fileserver01.example.com\Project\x"   # -> /mnt/project/x
pathconv-cli --to-windows "/mnt/project/x"            # force direction
pathconv-cli --no-map "C:\a\b\c"                      # separators only -> C:/a/b/c
pathconv-cli --list                                   # show mappings
echo "C:\a\b" | pathconv-cli                          # one path per line from stdin
```

Direction auto-detects (`\`, a drive letter, or `\\` means Windows input);
force it with `--to-unix` / `--to-windows`. Not installed? Use
`python -m pathconv.cli`.

## GUI

Once installed, run `pathconv` — or double-click a launcher in
[`launchers/`](launchers): `pathconv-gui.bat` (Windows, no console window) or
`pathconv-gui.sh` (Linux; `chmod +x` it first). On Windows, right-click the
`.bat` → *Send to → Desktop (create shortcut)* for a desktop icon.

The window has input/output boxes with live conversion (result auto-copied to
the clipboard), an "Apply directory mapping" toggle, Auto / → Unix / → Windows
direction, and "Edit mappings…" for share↔mount pairs. Needs Tkinter — bundled
on Windows and python.org builds; `sudo apt install python3-tk` on some Linux
distros.

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

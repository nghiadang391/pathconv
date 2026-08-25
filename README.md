# pathconv — Unix ↔ Windows path converter

Paste a path, get it converted — that's the whole tool.

```
\\fileserver01.example.com\Project\prj_example\x   (Windows)
/mnt/project/prj_example/x                          (Unix)
```

Swaps `\` ↔ `/`, handles UNC/drive prefixes, and knows the mapping above by
heart — configure your own share↔mount pairs once and never retype them.
Pure Python 3 + Tkinter, no dependencies, runs on Windows and Linux.

## Install

Requires Python 3.8+. Recommended: [pipx](https://pipx.pypa.io) (isolated,
puts commands on your PATH):

```bash
pipx install git+https://github.com/nghiadang391/pathconv.git
```

Don't have pipx? `python -m pip install --user pipx && python -m pipx ensurepath`,
then reopen your terminal. Or skip it and use plain pip:

```bash
pip install git+https://github.com/nghiadang391/pathconv.git
```

Working from a clone instead:

```bash
git clone https://github.com/nghiadang391/pathconv.git
cd pathconv
pip install .          # add -e for an editable/development install
```

Any of these gives you two commands: `pathconv-cli` and `pathconv` (GUI).

## CLI

```bash
pathconv-cli "\\fileserver01.example.com\Project\x"   # -> /mnt/project/x
pathconv-cli --to-windows "/mnt/project/x"            # force direction
pathconv-cli --no-map "C:\a\b\c"                      # separators only
pathconv-cli --list                                   # show mappings
echo "C:\a\b" | pathconv-cli                          # stdin, one path per line
```

Direction auto-detects; force with `--to-unix`/`--to-windows`.

## GUI

Once installed, run `pathconv`, or double-click a launcher in [`launchers/`](launchers):
`pathconv-gui.bat` (Windows) / `pathconv-gui.sh` (Linux, `chmod +x` first).
Live conversion, clipboard auto-copy, direction toggle, and a mapping editor.
Needs Tkinter (`sudo apt install python3-tk` on some distros).

## Configuration

Each mapping pairs a Windows share root with its Unix mount point (like the
example in the intro). They live in JSON, shared by CLI and GUI — override
with `--config PATH` or `PATHCONV_CONFIG`:

- Linux: `~/.config/pathconv/mappings.json`
- Windows: `%APPDATA%\pathconv\mappings.json`

```json
{"mappings": [{"windows_prefix": "\\\\fileserver01.example.com\\Project", "unix_prefix": "/mnt/project"}]}
```

Longest prefix match wins; Windows side is case-insensitive.

## Tests

```bash
python -m unittest discover -s tests
```

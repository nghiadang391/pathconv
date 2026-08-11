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
\\rvc-vnas-01.rvc.renesas.com\MobAP2\prj_RCAR_MBD\...   (Windows)
/shsv/MobAP2/prj_RCAR_MBD/...                            (Ubuntu)
```

The prefix mapping is toggleable: turn it **off** and only separators are
swapped.

## Install

```bash
pip install -e .
```

This registers two commands, `pathconv` and `pathconv-gui`. Without
installing, you can still run everything via `python -m pathconv.cli` /
`python -m pathconv.gui`.

## CLI

```bash
pathconv "\\rvc-vnas-01.rvc.renesas.com\MobAP2\prj_RCAR_MBD\x"
# -> /shsv/MobAP2/prj_RCAR_MBD/x

pathconv --to-windows "/shsv/MobAP2/prj_RCAR_MBD/x"
# -> \\rvc-vnas-01.rvc.renesas.com\MobAP2\prj_RCAR_MBD\x

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
      "windows_prefix": "\\\\rvc-vnas-01.rvc.renesas.com\\MobAP2",
      "unix_prefix": "/shsv/MobAP2"
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

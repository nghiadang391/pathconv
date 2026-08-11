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

## CLI

```bash
python -m pathconv.cli "\\rvc-vnas-01.rvc.renesas.com\MobAP2\prj_RCAR_MBD\x"
# -> /shsv/MobAP2/prj_RCAR_MBD/x

python -m pathconv.cli --to-windows "/shsv/MobAP2/prj_RCAR_MBD/x"
# -> \\rvc-vnas-01.rvc.renesas.com\MobAP2\prj_RCAR_MBD\x

python -m pathconv.cli --no-map "C:\a\b\c"   # -> C:/a/b/c  (separators only)
python -m pathconv.cli --list                # show configured mappings
echo "C:\a\b" | python -m pathconv.cli       # reads stdin, one path per line
```

Direction is auto-detected (a `\`, drive letter, or `\\` means Windows input);
force it with `--to-unix` / `--to-windows`.

## GUI

```bash
python -m pathconv.gui
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
python -m unittest discover -s path_converter/tests
```

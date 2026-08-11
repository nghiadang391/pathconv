"""Load and save the JSON mapping config shared by the CLI and GUI."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from .core import Mapping

ENV_VAR = "PATHCONV_CONFIG"

# Seeded on first run so the tool is useful out of the box.
DEFAULT_MAPPINGS: List[Mapping] = [
    Mapping(
        windows_prefix=r"\\fileserver01.example.com\Project",
        unix_prefix="/mnt/project",
    ),
]


def default_config_path() -> Path:
    """Return the platform-appropriate default config file path."""
    if os.name == "nt":
        base = os.environ.get("APPDATA") or str(Path.home())
        return Path(base) / "pathconv" / "mappings.json"
    base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(base) / "pathconv" / "mappings.json"


def resolve_config_path(path: Optional[str] = None) -> Path:
    """Resolve which config file to use: explicit arg > env var > default."""
    if path:
        return Path(path)
    env = os.environ.get(ENV_VAR)
    if env:
        return Path(env)
    return default_config_path()


def load_config(path: Optional[str] = None) -> List[Mapping]:
    """Load mappings from ``path``.

    If the file does not exist, seed it with :data:`DEFAULT_MAPPINGS` and
    return those. Malformed entries are skipped.
    """
    cfg_path = resolve_config_path(path)
    if not cfg_path.exists():
        save_config(DEFAULT_MAPPINGS, str(cfg_path))
        return list(DEFAULT_MAPPINGS)

    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return list(DEFAULT_MAPPINGS)

    mappings: List[Mapping] = []
    for entry in data.get("mappings", []):
        win = entry.get("windows_prefix")
        unix = entry.get("unix_prefix")
        if isinstance(win, str) and isinstance(unix, str):
            mappings.append(Mapping(windows_prefix=win, unix_prefix=unix))
    return mappings


def save_config(mappings: List[Mapping], path: Optional[str] = None) -> Path:
    """Write ``mappings`` to the resolved config path, creating parents."""
    cfg_path = resolve_config_path(path)
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "mappings": [
            {"windows_prefix": m.windows_prefix, "unix_prefix": m.unix_prefix}
            for m in mappings
        ]
    }
    cfg_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return cfg_path

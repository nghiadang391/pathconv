"""Pure, filesystem-free conversion logic.

The source path generally does not exist on the machine running the
conversion (a Windows UNC path is being converted on Linux, or vice versa),
so everything here operates on strings only. No ``os.path`` calls that would
consult the local filesystem or the local separator.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

TO_UNIX = "to_unix"
TO_WINDOWS = "to_windows"

# Matches a leading drive-letter root, e.g. "C:" or "C:\".
_DRIVE_RE = re.compile(r"^[A-Za-z]:")


@dataclass(frozen=True)
class Mapping:
    """A single prefix-mapping pair.

    ``windows_prefix`` is the network-share/drive root as seen on Windows
    (e.g. ``\\\\rvc-vnas-01.rvc.renesas.com\\MobAP2``) and ``unix_prefix`` is
    the equivalent mount point on Unix (e.g. ``/shsv/MobAP2``). Neither is
    expected to end with a separator.
    """

    windows_prefix: str
    unix_prefix: str

    def normalized(self) -> "Mapping":
        """Return a copy with trailing separators trimmed from both prefixes."""
        return Mapping(
            windows_prefix=self.windows_prefix.rstrip("\\/"),
            unix_prefix=self.unix_prefix.rstrip("\\/"),
        )


def detect_direction(path: str) -> str:
    """Guess the conversion direction from the shape of ``path``.

    A path containing a backslash, or starting with a drive letter or a UNC
    ``\\\\`` prefix, is treated as a Windows path (convert ``to_unix``).
    Otherwise it is treated as a Unix path (convert ``to_windows``).
    """
    stripped = path.strip()
    if "\\" in stripped or _DRIVE_RE.match(stripped) or stripped.startswith("\\\\"):
        return TO_UNIX
    return TO_WINDOWS


def _swap_separators(text: str, direction: str) -> str:
    if direction == TO_UNIX:
        return text.replace("\\", "/")
    return text.replace("/", "\\")


def _collapse_separators(text: str, sep: str) -> str:
    """Collapse runs of ``sep`` into a single ``sep`` (used on the remainder)."""
    if sep == "\\":
        return re.sub(r"\\+", "\\\\", text)
    return re.sub(r"/+", "/", text)


def _match_mapping(
    path: str, mappings: List[Mapping], direction: str
) -> Optional[Mapping]:
    """Return the best (longest) mapping whose source prefix matches ``path``.

    The Windows side is matched case-insensitively; the Unix side is matched
    case-sensitively. Longest source prefix wins so more specific mappings
    take precedence.
    """
    candidates = []
    for raw in mappings:
        m = raw.normalized()
        if direction == TO_UNIX:
            src = m.windows_prefix
            if path[: len(src)].lower() == src.lower():
                candidates.append((len(src), m))
        else:
            src = m.unix_prefix
            if path.startswith(src):
                candidates.append((len(src), m))
    if not candidates:
        return None
    candidates.sort(key=lambda pair: pair[0], reverse=True)
    return candidates[0][1]


def convert(
    path: str,
    mappings: Optional[List[Mapping]] = None,
    use_mapping: bool = True,
    direction: Optional[str] = None,
) -> str:
    """Convert ``path`` between Windows and Unix conventions.

    Parameters
    ----------
    path:
        The input path string.
    mappings:
        Prefix-mapping pairs to consider when ``use_mapping`` is true.
    use_mapping:
        When true, attempt to rewrite a known prefix (share root <-> mount
        point). When false, or when no mapping matches, only separators are
        swapped.
    direction:
        ``TO_UNIX`` or ``TO_WINDOWS`` to force direction; ``None`` auto-detects.
    """
    if not path:
        return path

    mappings = mappings or []
    direction = direction or detect_direction(path)

    # Preserve surrounding whitespace so pasted paths round-trip cleanly.
    lead_ws = path[: len(path) - len(path.lstrip())]
    trail_ws = path[len(path.rstrip()):]
    body = path.strip()

    target_sep = "/" if direction == TO_UNIX else "\\"

    if use_mapping:
        matched = _match_mapping(body, mappings, direction)
        if matched is not None:
            if direction == TO_UNIX:
                src_prefix, dst_prefix = matched.windows_prefix, matched.unix_prefix
            else:
                src_prefix, dst_prefix = matched.unix_prefix, matched.windows_prefix

            remainder = body[len(src_prefix):]
            remainder = _swap_separators(remainder, direction)
            # Drop any leftover leading separators; we re-join explicitly.
            remainder = remainder.lstrip("\\/")
            remainder = _collapse_separators(remainder, target_sep)

            if remainder:
                result = dst_prefix + target_sep + remainder
            else:
                result = dst_prefix
            # Preserve a trailing separator if the input had one.
            if body[-1:] in ("\\", "/") and not result.endswith(target_sep):
                result += target_sep
            return lead_ws + result + trail_ws

    # Fallback: separators only.
    return lead_ws + _swap_separators(body, direction) + trail_ws

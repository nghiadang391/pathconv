"""Command-line front-end for pathconv.

Examples
--------
    pathconv "\\\\server\\share\\dir\\file"   # auto-detect, mapping ON
    pathconv --no-map "C:\\a\\b"               # separators only
    pathconv --to-windows "/mnt/project/x"     # force direction
    pathconv --config ./my.json ...
    pathconv --list                            # print current mappings
    echo "C:\\a\\b" | pathconv                 # read from stdin
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .config import load_config, resolve_config_path
from .core import TO_UNIX, TO_WINDOWS, convert


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pathconv",
        description="Convert file paths between Windows and Unix conventions.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to convert. If omitted, each line of stdin is converted.",
    )
    parser.add_argument(
        "--no-map",
        dest="use_mapping",
        action="store_false",
        help="Only swap separators; do not apply the prefix mapping.",
    )
    direction = parser.add_mutually_exclusive_group()
    direction.add_argument(
        "--to-unix",
        dest="direction",
        action="store_const",
        const=TO_UNIX,
        help="Force conversion to a Unix path.",
    )
    direction.add_argument(
        "--to-windows",
        dest="direction",
        action="store_const",
        const=TO_WINDOWS,
        help="Force conversion to a Windows path.",
    )
    parser.add_argument(
        "--config",
        help="Path to the mappings JSON file (overrides PATHCONV_CONFIG).",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the configured mappings and exit.",
    )
    parser.set_defaults(use_mapping=True, direction=None)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    mappings = load_config(args.config)

    if args.list:
        cfg_path = resolve_config_path(args.config)
        print(f"# config: {cfg_path}")
        if not mappings:
            print("(no mappings)")
        for m in mappings:
            print(f"{m.windows_prefix}  <->  {m.unix_prefix}")
        return 0

    def do(line: str) -> str:
        return convert(
            line,
            mappings=mappings,
            use_mapping=args.use_mapping,
            direction=args.direction,
        )

    if args.path is not None:
        print(do(args.path))
        return 0

    # No positional path: convert each line of stdin (strip the newline only).
    if sys.stdin.isatty():
        parser.error("no path given and stdin is a terminal")
    for line in sys.stdin:
        print(do(line.rstrip("\n")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

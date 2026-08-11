"""Unit tests for pathconv.core (pure string conversion)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pathconv.core import (  # noqa: E402
    TO_UNIX,
    TO_WINDOWS,
    Mapping,
    convert,
    detect_direction,
)

MAP = [
    Mapping(
        windows_prefix=r"\\fileserver01.example.com\Project",
        unix_prefix="/mnt/project",
    )
]

WIN = (
    "\\\\fileserver01.example.com\\Project\\prj_example\\05_from_vendor"
    "\\260810_EXAMPLE_Release\\"
)
UNIX = (
    "/mnt/project/prj_example/05_from_vendor/"
    "260810_EXAMPLE_Release/"
)


class DirectionTests(unittest.TestCase):
    def test_unc_is_to_unix(self):
        self.assertEqual(detect_direction(r"\\server\share"), TO_UNIX)

    def test_drive_is_to_unix(self):
        self.assertEqual(detect_direction(r"C:\a\b"), TO_UNIX)

    def test_backslash_is_to_unix(self):
        self.assertEqual(detect_direction(r"a\b"), TO_UNIX)

    def test_slash_is_to_windows(self):
        self.assertEqual(detect_direction("/mnt/project"), TO_WINDOWS)


class MappingTests(unittest.TestCase):
    def test_user_example_win_to_unix(self):
        self.assertEqual(convert(WIN, MAP), UNIX)

    def test_user_example_unix_to_win(self):
        self.assertEqual(convert(UNIX, MAP), WIN)

    def test_no_trailing_slash_preserved(self):
        self.assertEqual(
            convert(r"\\fileserver01.example.com\Project\a\b", MAP),
            "/mnt/project/a/b",
        )

    def test_prefix_only(self):
        self.assertEqual(
            convert(r"\\fileserver01.example.com\Project", MAP),
            "/mnt/project",
        )

    def test_case_insensitive_windows_prefix(self):
        self.assertEqual(
            convert(r"\\FILESERVER01.EXAMPLE.com\Project\a", MAP),
            "/mnt/project/a",
        )

    def test_longest_prefix_wins(self):
        mappings = [
            Mapping(windows_prefix=r"\\srv\share", unix_prefix="/mnt/short"),
            Mapping(windows_prefix=r"\\srv\share\deep", unix_prefix="/mnt/deep"),
        ]
        self.assertEqual(
            convert(r"\\srv\share\deep\x", mappings), "/mnt/deep/x"
        )


class FallbackTests(unittest.TestCase):
    def test_mapping_off_only_swaps(self):
        self.assertEqual(
            convert(r"C:\a\b\c", MAP, use_mapping=False), "C:/a/b/c"
        )

    def test_no_match_falls_back_to_swap(self):
        self.assertEqual(convert(r"D:\other\path", MAP), "D:/other/path")

    def test_unix_no_match_falls_back(self):
        self.assertEqual(convert("/tmp/x/y", MAP), r"\tmp\x\y")

    def test_forced_direction_overrides_detection(self):
        # No backslash, but force to_unix should be a no-op swap.
        self.assertEqual(
            convert("/mnt/project/a", MAP, direction=TO_UNIX, use_mapping=False),
            "/mnt/project/a",
        )

    def test_empty_string(self):
        self.assertEqual(convert("", MAP), "")


if __name__ == "__main__":
    unittest.main()

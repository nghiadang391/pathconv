"""Double-click launcher for the pathconv GUI on Windows.

Using the ``.pyw`` extension runs the GUI without opening a console window.
This works whether or not the ``pathconv`` package is pip/pipx-installed, as
long as it is importable by the Python that opens ``.pyw`` files.
"""

from pathconv.gui import main

if __name__ == "__main__":
    raise SystemExit(main())

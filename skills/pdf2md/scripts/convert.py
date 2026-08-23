#!/usr/bin/env python3
"""Convert a PDF to Markdown using pymupdf4llm.

Run this script with the venv's Python after the one-time setup described in the
skill's SKILL.md:

    .pdf2md/venv/bin/python scripts/convert.py <input.pdf> [-o out.md]   (macOS/Linux)
    .pdf2md\\venv\\Scripts\\python.exe scripts\\convert.py <input.pdf>    (Windows)

Requires Python 3.11+ (pymupdf4llm dependency). Exit code is non-zero on error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pymupdf4llm
except ImportError as exc:
    message = str(exc).lower()
    print("[pdf2md] error: could not import pymupdf4llm in this interpreter.", file=sys.stderr)
    if "dll load failed" in message or "native" in message:
        print(
            "[pdf2md] PyMuPDF ships native binaries that this environment cannot load.",
            file=sys.stderr,
        )
        print(
            "[pdf2md] If pymupdf works in another project here, make sure this venv's",
            file=sys.stderr,
        )
        print(
            "[pdf2md] interpreter matches (same Python, same 64-bit). Otherwise re-create",
            file=sys.stderr,
        )
        print(
            "[pdf2md] the venv with a python.org or winget Python and reinstall.",
            file=sys.stderr,
        )
    else:
        print("[pdf2md] run the one-time venv setup from SKILL.md, then run this", file=sys.stderr)
        print("[pdf2md] script with the venv's python.", file=sys.stderr)
    sys.exit(2)


def convert(input_path: Path, output_path: Path | None) -> Path:
    if not input_path.is_file():
        raise FileNotFoundError(f"input PDF not found: {input_path}")

    markdown = pymupdf4llm.to_markdown(str(input_path))
    output = output_path if output_path else input_path.with_suffix(".md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pdf2md",
        description="Convert a PDF to Markdown using pymupdf4llm.",
    )
    parser.add_argument("input", type=Path, help="input PDF file")
    parser.add_argument("-o", "--output", type=Path, default=None, help="output .md file")
    args = parser.parse_args(argv)

    try:
        output = convert(args.input, args.output)
    except FileNotFoundError as exc:
        print(f"[pdf2md] error: {exc}", file=sys.stderr)
        return 1
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
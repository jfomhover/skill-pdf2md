---
name: pdf2md
description: Converts PDF documents to clean Markdown using a local pymupdf4llm converter.
  The agent sets up a project-local virtualenv once (plain venv + pip install) and then
  runs scripts/convert.py fully offline. Use when the user wants to convert a PDF (report,
  paper, manual, book, spec) to Markdown, extract document text for an LLM, or produce .md
  files from PDFs in a project.
license: MIT
allowed-tools: Read Write Bash(python:*, python3:*)
---

# pdf2md

Convert PDFs to Markdown with a local `pymupdf4llm` converter (`scripts/convert.py`).
Setup is plain venv work, done once per project; conversion afterwards is fast and fully
offline.

## When to use me

- The user asks to convert a PDF to Markdown / `.md`.
- The user wants document text extracted for an agent or LLM to read.
- The user wants several PDFs in a project turned into Markdown for reference.

## Setup (once per project)

Run these from the project root, into a project-local venv:

1. Create the venv if `.pdf2md/venv` does not exist yet:

   ```bash
   python -m venv .pdf2md/venv
   ```

   (Windows: `.pdf2md\venv\Scripts\python.exe`; macOS/Linux: `.pdf2md/venv/bin/python`.)
   Use a real Python 3.11+ — the Microsoft Store `python` stub cannot create venvs, so
   on Windows prefer `py -3.12` or a python.org/winget Python.

2. Install the converter's dependency from this skill's `scripts/requirements.txt`
   (needs network on first install):

   ```bash
   .pdf2md/venv/bin/python -m pip install -r <this-skill>/scripts/requirements.txt
   ```

## Convert

Run the converter with the venv's Python:

```bash
.pdf2md/venv/bin/python <this-skill>/scripts/convert.py <input.pdf> [-o <output.md>]
```

- Default output is `<input>.md` next to the PDF. Pass `-o` to choose another path
  (the output directory is created if needed).
- Run once per PDF when converting several files.
- Verify the output file exists and report its path to the user.

## Edge cases

- Missing input: the script errors with a clear message — re-check the path.
- `No module named pymupdf4llm` means the venv setup was skipped; run it once.
- First-run `pip install` needs network; conversion itself runs fully offline.
- To reuse one venv across projects (e.g. on a locked-down machine), create it once at a
  shared path and always run `convert.py` with that venv's python — see
  `references/usage.md`.

See `references/usage.md` for the full CLI reference and troubleshooting.
# pdf2md usage reference

The skill ships one script, `scripts/convert.py`, a thin wrapper around `pymupdf4llm`,
plus `scripts/requirements.txt` declaring the single dependency. Setup is plain
virtualenv work described in `SKILL.md`. Read this reference when you need details or
hit a snag.

## What to run

```bash
python -m venv .pdf2md/venv                                        # once per project
.pdf2md/venv/bin/python -m pip install -r <skill>/scripts/requirements.txt
.pdf2md/venv/bin/python <skill>/scripts/convert.py <input.pdf> [-o <output.md>]
```

On Windows the venv binaries live at `.pdf2md\venv\Scripts\python.exe` instead of
`.pdf2md/venv/bin/python`.

## convert.py options

| option | behavior |
|---|---|
| `input` | the PDF to convert; must exist, else the script prints `input PDF not found` and exits non-zero |
| `-o, --output` | output `.md` path; default is the input path with a `.md` extension |
| `-h, --help` | usage and exit 0 |

`convert.py` creates the output directory if needed and prints the written path on
success. Exit code is non-zero on any failure; errors go to stderr.

## venv location

- Default is a **project-local** `.pdf2md/venv`, which keeps everything inside the
  project and leaves no hidden global state.
- To reuse a single venv across projects (useful on machines where installing is slow
  or restricted), create it once at a shared path and run `convert.py` with that venv's
  python every time:
  ```bash
  python -m venv C:\tools\pdf2md-venv
  C:\tools\pdf2md-venv\Scripts\python -m pip install -r <skill>/scripts/requirements.txt
  C:\tools\pdf2md-venv\Scripts\python <skill>/scripts/convert.py <input.pdf>
  ```

## Requirements and network

- System Python 3.11+ to create the venv.
- First `pip install` downloads `pymupdf4llm` (and PyMuPDF's bundled native libraries)
  and needs network access.
- After the venv is installed, conversion runs fully offline and never makes network
  calls; all processing is local.

## Troubleshooting

| symptom | fix |
|---|---|
| `No module named pymupdf4llm` | venv setup was skipped or the system Python was used; create the venv and install `scripts/requirements.txt` into it, then run via the venv's python |
| `python -m venv` fails or makes no venv | on Windows this is usually the Microsoft Store `python` stub; use `py -3.12` or a python.org/winget Python |
| `error: could not import pymupdf4llm ... native binaries ... cannot load` | environment-specific (blocked/quarantined file, missing runtime, 32/64-bit mismatch). If pymupdf loads in another project here, recreate the venv with that same interpreter; otherwise see the message's suggestion |
| `input PDF not found` | the path is wrong or the PDF is elsewhere; re-check before re-running |
| converting many PDFs | run once per file; the venv is reused, so only conversion cost remains |

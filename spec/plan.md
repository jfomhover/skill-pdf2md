# Plan

## 1. Repo layout

```text
skill-pdf2md/                # this repo
├── README.md                # what this repo is, how to install/run the skill
├── AGENTS.md                # skill authoring conventions (read by coding agents)
├── LICENSE
├── .gitignore
├── spec/
│   ├── intent.md            # why this repo exists
│   └── plan.md              # how it is built and maintained
├── skills/
│   └── pdf2md/              # the one skill in this repo
│       ├── SKILL.md         # frontmatter + instructions (incl. venv setup)
│       ├── scripts/
│       │   ├── convert.py   # the converter (thin pymupdf4llm wrapper)
│       │   └── requirements.txt  # the only dependency (pymupdf4llm)
│       └── references/
│           └── usage.md     # CLI ref, venv behavior, troubleshooting
└── .github/
    └── workflows/
        ├── validate.yml     # skill-validator on push + PR
        └── release.yml      # final validation gate on tag push
```

CI carries over unchanged from the template: `validate.yml` and `release.yml` check
`skills/` generically and need no per-skill edits.

## 2. The pdf2md skill

`skills/pdf2md/` follows the rules in `AGENTS.md` exactly:

- **Frontmatter** — `name: pdf2md` (matches the directory), a description with trigger
  keywords ("convert PDF to Markdown", extract document text), `license: MIT`, and a
  minimal `allowed-tools` (`Read Write Bash(python:*, python3:*)`).
- **Lean body** — when/how to use, the one-time venv setup, the exact run command, and
  edge cases; details deferred to `references/usage.md`.
- **Setup is plain venv work** — `python -m venv .pdf2md/venv` then
  `.pdf2md/venv/bin/python -m pip install -r <skill>/scripts/requirements.txt`. The skill
  owns no setup script and never installs on its own; this keeps side effects inside the
  project and predictable.
- **Scripts**
  - `convert.py` — a self-contained wrapper around `pymupdf4llm`, run with the venv's
    python. Handles missing-input errors and prints an actionable message when
    `pymupdf4llm` cannot be imported (venv setup skipped, or an environment-specific
    native-binary load failure). Creates the output directory if needed and prints the
    written path.
  - `requirements.txt` — declares `pymupdf4llm` as the only dependency.
- **Source of behavior** — `convert.py` is a faithful port of the `markdown-tools`
  `pdf2md4llm` tool; keep the two in sync when the tool changes.
- **Security posture** — the converter is reviewed local-only code; it never makes
  network calls at conversion time. The only network touchpoint is `pip` during the
  one-time venv install.

## 3. Validation and release

- **Locally** (needs Go): `go run github.com/agent-ecosystem/skill-validator/cmd/skill-validator@v1.6.0 check skills/`
- **CI**: `validate.yml` on every push/PR over `skills/**`; `release.yml` re-runs the
  same suite on `v*` tag pushes. Failure blocks the build.
- **Release**: tag-based only. `git tag vX.Y.Z && git push origin vX.Y.Z`, with the
  `release.yml` gate as the final check. No artifacts are built.

## 4. Build-out milestones

- **M1 — scaffold:** repo from the template; initial structure and CI in place. *(done)*
- **M2 — skill:** the converter under `skills/pdf2md/`; get `validate.yml` green. *(done)*
- **M3 — finalize:** trim template examples, adopt `README`/`spec/`/`AGENTS.md` to this
  repo's intent. *(done)*
- **M4 — simplify packaging:** drop `assets/` and `setup.py`; `scripts/convert.py` +
  `scripts/requirements.txt` with plain venv setup in `SKILL.md`. *(this change)*
- **M5 — release path:** tag `v1.0.0`, confirm `release.yml` gate and `npx skills add`
  install.

## 5. Future work (explicitly deferred)

- Exposing OCR flags from `pymupdf4llm` (scanned PDFs) if a real need appears.
- A multi-PDF batch mode instead of one invocation per file.
- Additional skills; this repo currently has exactly one.
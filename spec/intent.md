# Intent

## 1. What this repo is

A single-skill repository for **`pdf2md`**, an agent skill that converts PDF documents
to Markdown. The skill ships one reviewed script, `scripts/convert.py` (a thin
`pymupdf4llm` wrapper), and a one-dependency `scripts/requirements.txt`. The agent sets
up a project-local virtualenv with plain venv commands (once per project) and then
runs the converter fully locally.

The repo is a thin shell: no tooling of its own. It holds one skill under `skills/`,
plus the CI that validates it. The skill follows the open Agent Skills specification
(agentskills.io), so it works in opencode, Claude Code, Codex, GitHub Copilot CLI,
Cursor, and 30+ other agents with no per-agent packaging.

## 2. Why a skill, not a tool install

The converter itself is small: a CLI wrapper around `pymupdf4llm`. Shipping it as a
skill adds the agent-visible layer:

- **Discovery.** The skill Description surfaces when a task mentions converting a PDF
  to Markdown or extracting document text, so the agent knows to use it without a
  manual "install my converter" instruction.
- **No skill-owned machinery.** Setup is the standard `python -m venv` +
  `pip install -r requirements.txt` the agent already knows — no hidden setup script,
  no automatic installs, no silent network access behind the scenes.
- **Project-local and predictable.** The venv lives at `.pdf2md/venv` inside the
  project, so it is cheap to reproduce and leaves no hidden global state on the machine.
- **Offline after install.** Conversion never touches the network; all extraction is
  local and private.

## 3. Goals

- One validated skill, `skills/pdf2md/`, following every rule in `AGENTS.md`.
- A single, reviewed converter script — `scripts/convert.py`, a faithful port of the
  `markdown-tools` `pdf2md4llm` tool that stays in sync with it — plus
  `scripts/requirements.txt` declaring `pymupdf4llm` as the only dependency.
- Clear, self-contained instructions in `SKILL.md` (the venv setup and the exact run
  command) with details deferred to `references/usage.md`.
- CI keeps a green `validate.yml` gate on every push/PR and a final `release.yml` gate
  on tags.
- Versioning is purely tag-based (`v*`); the tag is the release.

## 4. Non-goals

- No bundle of a prebuilt converter binary; the skill installs from source.
- No support for other document formats (`.docx`, `.epub`, image OCR is not
  exposed) — this skill is scoped to text-layer PDFs via `pymupdf4llm`.
- No agent-specific layout, marketplace, or custom packaging tooling.
- No additional skills until one is genuinely needed; keep the repo focused.

## 5. Success criteria

1. `skills/pdf2md/` passes `skill-validator check skills/` (CI and locally).
2. Following `SKILL.md`, an agent creates `.pdf2md/venv`, installs
   `scripts/requirements.txt`, then `.pdf2md/venv/bin/python scripts/convert.py <pdf>
   [-o out.md]` converts a PDF to Markdown — with zero global side effects and no
   hidden network access.
3. `npx skills add jfomhover/skill-pdf2md` installs the skill and opencode discovers it.
4. `git tag vX.Y.Z && git push origin vX.Y.Z` runs the final validation gate and is the
   published release.
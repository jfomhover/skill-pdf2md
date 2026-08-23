# AGENTS.md

Conventions for authoring skills in this repository. Follow them exactly when creating,
editing, or reviewing a skill. Skills here follow the open Agent Skills specification
(agentskills.io), which opencode, Claude Code, Codex, GitHub Copilot CLI, Cursor, and
other agents all read natively.

## What a skill is

A skill is a directory named after the skill, containing a `SKILL.md` file with YAML
frontmatter followed by Markdown instructions, plus optional resource folders:

```text
skills/<skill-name>/
├── SKILL.md            # required: frontmatter + instructions
├── scripts/            # optional: self-contained executable code the agent runs
├── references/         # optional: docs the agent loads on demand
└── assets/             # optional: templates, source code, sample data
```

## Mandatory rules

- **`SKILL.md`** is exactly that name (uppercase). The file starts with `---` YAML
  frontmatter, then a non-empty Markdown body.
- **`name`** matches `^[a-z0-9]+(-[a-z0-9]+)*$`, is 1–64 characters, and equals the parent
  directory name.
- **`description`** is 1–1024 characters, non-empty, and states *what* the skill does and
  *when* to use it, with trigger keywords an agent would match against.
- **Optional frontmatter**: `license` (string), `compatibility` (string),
  `metadata` (string-to-string map), `allowed-tools` (space-separated, experimental).
- **Only ship what agents need.** Do not put `README.md`, `CHANGELOG.md`, `LICENSE`, or
  other human-only files inside a skill directory — they pollute the agent's context and
  fail validation. Site repo-level docs at the repo root.

## Recommended practices

- **Progressive disclosure.** Keep the body lean (target under ~5k tokens / ~500 lines).
  Move long detail into `references/`, which agents load only when needed.
- **References.** Keep file references one level deep from `SKILL.md` and make sure every
  file referenced in the body actually exists in the skill directory.
- **Scripts.** `scripts/` entries should be self-contained, document dependencies, handle
  edge cases, and print helpful errors. Tell the agent exactly how to run them.
- **`allowed-tools`.** Declare only the tools the skill needs. Omit `shell`/`bash` unless
  every referenced script has been reviewed and trusted.
- **Security.** Skills may run bundled code. Review third-party or network-touching content
  for prompt injection and exfiltration before adding it.

## Validation

CI runs `skill-validator check skills/` (agent-ecosystem/skill-validator, pinned) on every
push and pull request; tagged releases re-run it as a final gate. A skill that fails
validation blocks the build. Run the same check locally before committing:

```bash
go run github.com/agent-ecosystem/skill-validator/cmd/skill-validator@v1.6.0 check skills/
```

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md` following the rules above.
2. Add resources under `scripts/`, `references/`, `assets/` as needed, and reference them
   from the body.
3. Validate locally, then open a PR.
4. Tag to release: `git tag vX.Y.Z && git push origin vX.Y.Z`.

## Editing an existing skill

- Update the `SKILL.md` body and any referenced resources together — dangling references
  fail validation.
- Bump nothing manually; versioning is purely tag-based (`v*` tags).

## This repo's skill: pdf2md

This repository ships one skill, `skills/pdf2md/` — a PDF-to-Markdown converter built on
`pymupdf4llm`. Points specific to this skill:

- **Single script.** `scripts/convert.py` is the converter (a thin `pymupdf4llm`
  wrapper); `scripts/requirements.txt` declares `pymupdf4llm` as the only dependency.
  Set up is plain venv work the agent does following `SKILL.md` — no skill-owned setup
  script.
- **Self-contained.** All Python the agent needs lives under `skills/pdf2md/`; the agent
  must never be told to install or import anything from `markdown-tools`. `convert.py`
  is a faithful port of that repo's `pdf2md4llm` tool's logic; keep the two in sync if
  the tool changes.
- **Scripts are the contract.** Keep `scripts/convert.py`'s behavior and
  `references/usage.md` consistent; the agent references both.
- **Network.** The first `pip install` needs network to fetch `pymupdf4llm`; conversion
  itself must stay fully offline. Keep that boundary intact.
- Consult `spec/intent.md` and `spec/plan.md` for the repo's intent; ask the owner before
  changing the repo structure, dropping the skill, or relaxing validation rules.

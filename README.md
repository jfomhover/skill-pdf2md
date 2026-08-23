# skill-pdf2md

An agent skills repo with one skill: **`pdf2md`** — converts PDF documents to clean
Markdown for use in projects. The skill provides a `pymupdf4llm`-based converter and
documents a project-local virtualenv setup; conversion runs fully locally and offline
after installation.

Skills here follow the open [Agent Skills](https://agentskills.io) standard (`SKILL.md` +
YAML frontmatter), so `pdf2md` works in opencode, Claude Code, Codex, GitHub Copilot CLI,
Cursor, and 30+ other agents with no per-agent work.

## The skill

`skills/pdf2md/` is self-contained:

| path | purpose |
|---|---|
| `SKILL.md` | when/how the skill is used, plus the one-time venv setup |
| `scripts/convert.py` | the converter — a thin `pymupdf4llm` wrapper |
| `scripts/requirements.txt` | the only dependency (`pymupdf4llm`) |
| `references/usage.md` | CLI reference, venv behavior, troubleshooting |

Setup is plain venv work the agent does once per project, into a project-local
`.pdf2md/venv`: `python -m venv .pdf2md/venv` then
`.pdf2md/venv/bin/python -m pip install -r <skill>/scripts/requirements.txt`. This keeps
everything inside the project with no hidden global state.

### What the agent does

```bash
.pdf2md/venv/bin/python <skill>/scripts/convert.py <input.pdf>       # -> <input>.md
.pdf2md/venv/bin/python <skill>/scripts/convert.py <input.pdf> -o out.md
```

First `pip install` needs network once; conversion runs fully offline and locally.

## Installing the skill (consumer side)

Opencode and most agents discover skills from filesystem folders — there is no install
command. Either point an installer at this repo, or copy the folder yourself:

```bash
# Open installer (npx skills from skills.sh)
npx skills add jfomhover/skill-pdf2md
npx skills add jfomhover/skill-pdf2md --skill pdf2md

# Manual — drop the folder into any opencode discovery directory
git clone https://github.com/jfomhover/skill-pdf2md.git ~/.agents/skills
```

Opencode watches these locations:

| scope | paths |
|---|---|
| project | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` |
| global | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` |

## Developing this repo

- Authoring conventions live in [`AGENTS.md`](AGENTS.md) — read it before editing a skill.
- Rationale and roadmap live in [`spec/intent.md`](spec/intent.md) and
  [`spec/plan.md`](spec/plan.md).
- Validate locally (CI runs the same check on push/PR):

  ```bash
  go run github.com/agent-ecosystem/skill-validator/cmd/skill-validator@v1.6.0 check skills/
  ```

- Release by tagging: `git tag v1.0.0 && git push origin v1.0.0`. `release.yml`
  re-validates as a final gate. No build step, no artifacts.

## Security

Skills can bundle executable scripts; always review the `scripts/` directory of any skill
you install. `pdf2md` runs only the reviewed `scripts/convert.py`. Conversion never makes
network calls; the only network touchpoint is `pip` during the one-time venv install.

## License

[MIT](LICENSE)

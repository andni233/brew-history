# Development tasks

Tasks are defined as scripts in `mise/tasks/` and run via `mise run <task>`.

## Checkers (`mise run check`)

Runs linters, formatters in check mode, and type/spell checkers. Fails if any issues are found; does not modify files.

| Sub-task | Tool | What it checks |
|---|---|---|
| `check:ruff` | ruff | Python lint + formatting |
| `check:mypy` | mypy --strict | Python types |
| `check:taplo` | taplo | TOML formatting |
| `check:codespell` | codespell | Spelling across source files |
| `check:yamllint` | yamllint | YAML syntax and style |
| `check:stylelint` | stylelint | CSS rules |
| `check:shellcheck` | shellcheck | Shell scripts |

Run an individual checker: `mise run check:ruff`

## Fixers (`mise run fix`)

Auto-fixes issues where possible. Modifies files in place.

| Sub-task | Tool | What it fixes |
|---|---|---|
| `fix:ruff` | ruff | Python lint issues + formatting |
| `fix:taplo` | taplo | TOML formatting |
| `fix:codespell` | codespell | Spelling |

Run an individual fixer: `mise run fix:ruff`

## Builders (`mise run build`)

Imports BeerXML recipes and builds the Hugo site into `public/`.

- `mise run import` — convert `recipes/*.xml` to Hugo content files
- `mise run build` — import + build
- `mise run serve` — import + local dev server with drafts (`hugo server -D`)

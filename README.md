# brew-history

A personal brewing log. Recipes are stored as BeerXML files in `recipes/` and published as a Hugo site at [andni233.github.io/brew-history](https://andni233.github.io/brew-history/).

## Development

Requires [mise](https://mise.jdx.dev/). Install all tools:

```
mise install
```

### Checkers

Linters, formatters in check mode, type and spell checkers. Does not modify files.

```
mise run check
```

Run an individual checker: `mise run check:ruff`, `mise run check:mypy`, `mise run check:taplo`, `mise run check:codespell`, `mise run check:yamllint`, `mise run check:stylelint`, `mise run check:shellcheck`

### Fixers

Auto-fixes formatting, lint, and spelling issues in place.

```
mise run fix
```

Run an individual fixer: `mise run fix:ruff`, `mise run fix:taplo`, `mise run fix:codespell`

### Builders

```
mise run build         # import recipes + build site
mise run build:serve   # import recipes + local dev server
```

## Adding recipes

Drop a `.xml` file (BeerXML format) into `recipes/` and run `mise run build`.

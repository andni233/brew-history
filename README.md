# brew-history

A personal brewing log. Recipes are stored as YAML files in `recipes/` and published as a Hugo site at [andni233.github.io/brew-history](https://andni233.github.io/brew-history/).

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

Create a `.yaml` file in `recipes/` and run `mise run build`. The filename doesn't matter — the slug is derived from the `title` field.

### Required fields

```yaml
title: "My IPA"
date: 2026-04-06
recipe_type: "All Grain"
brewers:
  - "Andreas Nilsson"
```

### Optional metadata

```yaml
description: "A juicy west coast IPA."
style:
  name: "American IPA"
  category: "India Pale Ale"
  guide: "BJCP"
  notes: "..."
notes: "Process notes go here."
```

### Ingredients

```yaml
fermentables:
  - name: "Pale Malt"
    type: "Grain"
    amount_kg: 5.0
    yield_pct: 82.0
    color_ebc: 5.9

hops:
  - name: "Citra"
    alpha: 12.0
    amount_g: 30
    use: "Boil"
    time_min: 60
    form: "Pellet"

yeasts:
  - name: "American Ale"
    form: "Liquid"
    display_amount: "1 vial"
    attenuation: 75
    product_id: "WLP001"
    laboratory: "White Labs"   # optional

miscs:
  - name: "Irish Moss"
    use: "Boil"
    type: "Fining"
    time_min: 15
    display_amount: "1 tsp"

mash_steps:
  - name: "Mash In"
    type: "Temperature"
    step_time: 60
    step_temp: 67.0
    end_temp: 67.0
```

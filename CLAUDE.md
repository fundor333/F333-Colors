# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

F333 Colors is a VS Code color theme extension (Marketplace publisher `Fundor333`). There is no
extension source code (no TS/JS activation logic) — it is a pure theme package. The actual "product"
is a set of generated `*-color-theme.json` files under `themes/`, declared in `package.json`'s
`contributes.themes`.

## Build pipeline (source of truth vs. generated files)

`themes/*.json` and `package.json` are **generated build artifacts** — never hand-edit them, changes
will be overwritten by the next build. The real source of truth lives under `src/`:

- `src/colors/colors_*.json` — one file per theme variant (e.g. blue, cyan, lime, plum). Each defines
  the variant's palette (hex values) plus which template/token-colors/git file to use and the output
  `filename`/`title`/`uiTheme`.
- `src/template/template.jinja` and `src/template/template_inverted_tab.jinja` — Jinja2 templates for
  the theme's `colors` block; selected per-variant via the `template` key in the color config.
- `src/editor/token_colors_dark.json` — shared syntax-highlighting (`tokenColors`) rules, injected
  verbatim into the rendered theme via the `tokenColors` key.
- `src/git/git_dark.json`, `git_basic.json`, `git_dark_pastel.json` — Git decoration colors, merged
  into the theme's `colors` block depending on `uiTheme` (dark vs. light) / the variant's `git` key.
- `src/template/package.json.jinja` + `setting.json` — template and base metadata (name, publisher,
  version, etc.) used to regenerate the root `package.json`, including the full `contributes.themes`
  list assembled from every file in `src/colors/`.

`scripts/build.py` (Python) does the actual generation: for each `src/colors/*.json`, it renders the
theme template into `themes/`, then regenerates `package.json` from `setting.json` +
`package.json.jinja`.

`scripts/version.py` (Python, using `click`) bumps the semver version in `setting.json`
(`hotfix`/`minor`/`major`), which `package.json` inherits on the next build.

## Adding a new theme variant

Add a new `src/colors/colors_<name>.json` with `filename`, `title`, `uiTheme`, `template`,
`tokenColors`, and the color hex values (see an existing file for the full key set), then run
`make build`. It will automatically be picked up and added to `package.json`'s `contributes.themes`.

## Common commands

Python side uses Poetry; Node side is only used for VS Code packaging/publishing (`vsce`, `ovsx`).

```bash
make install   # poetry install --no-root; npm install -g @vscode/vsce
make build     # poetry run python scripts/build.py  -> regenerates themes/*.json and package.json
make hotfix    # bump patch version in setting.json, then build
make minor     # bump minor version in setting.json, then build
make major     # bump major version in setting.json, then build
make publish   # build; npm run package (vsce package); npm run publish (vsce publish && ovsx publish)
```

There is no test suite or linter configured for this repo.

## CI

`.github/workflows/vscode.yml` runs on a published GitHub release (or manual dispatch): installs npm
deps, installs `vsce`, and runs `vsce publish` using the `VSCE_PAT` secret. It does not run the Python
build step, so `themes/` and `package.json` must already be regenerated and committed before cutting a
release.

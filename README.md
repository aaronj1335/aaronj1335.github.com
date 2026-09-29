mi github pages

[![validate](https://github.com/aaronj1335/aaronj1335.github.com/actions/workflows/validate.yml/badge.svg)](https://github.com/aaronj1335/aaronj1335.github.com/actions/workflows/validate.yml)

## developing

- install [uv](https://docs.astral.sh/uv/)

- `uv run main.py build` builds the site into `_site/`

- `uv run main.py validate` runs all checks (currently `ruff check`)

- `uv run python -m http.server -d _site 4000` serves it at http://localhost:4000

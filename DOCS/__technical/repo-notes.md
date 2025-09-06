# Repo notes

## .gitignore (minimal for this project)

Obecny zakres ignorowanych plików:

- Python cache: `__pycache__/`, `*.py[cod]`
- Wirtualne środowiska: `.venv/`
- Artefakty pakowania: `*.egg-info/`, `app.egg-info/`, `build/`, `dist/`, `.eggs/`
- Sekrety/zmienne: `.env`
- Pliki systemowe macOS: `.DS_Store`

Uzasadnienie: minimalny i bezpieczny zestaw dla bieżącej struktury repo (lokalne środowisko, artefakty builda, sekrety, cache, pliki systemowe). 

## uv.lock

- Rola: odpowiednik `package-lock.json` (npm) / `bun.lockb` (Bun) – deterministyczne drzewo zależności z wersjami i hashami.
- Praktyka: trzymamy `uv.lock` w repo (aplikacja) dla powtarzalnych buildów i spójnych instalacji (`uv sync`).
- Gdy zmieniamy zależności w `pyproject.toml`: aktualizujemy lock (`uv add/remove`, `uv lock`).

## Dodatkowe uwagi

- `pyproject.toml` commitujemy – to źródło prawdy o deklaracjach zależności.
- Jeśli pojawią się nowe narzędzia (pytest, mypy itd.), rozważymy dopisanie ich cache do `.gitignore` (np. `.pytest_cache/`, `.mypy_cache/`).

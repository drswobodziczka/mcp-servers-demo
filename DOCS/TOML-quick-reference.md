# TOML – szybka ściąga (Quick Reference)

TOML (Tom's Obvious, Minimal Language) to czytelny format plików konfiguracyjnych.
Zaprojektowany tak, aby był łatwy do czytania i jednoznacznie mapował się
na proste struktury danych (słowniki, listy, typy proste).

Przykładowe zastosowanie w tym repo: `pyproject.toml`.

---

## Podstawy składni

- # Komentarze
  - Komentarz zaczyna się od `#` do końca linii.

- Klucz = Wartość
  - `name = "app"`
  - Klucz jest po lewej, znak `=`, wartość po prawej (z odstępami).

- Typy wartości
  - String: `"text"` lub wielolinijkowy `"""..."""`
  - Liczby: `42`, `3.14`
  - Boolean: `true`, `false`
  - Daty/czasy (RFC 3339): `2025-09-06T00:00:00+02:00`
  - Tablice (listy): `[1, 2, 3]`, `["a", "b"]`
  - Tabele (sekcje): patrz niżej
  - Tabele inline: `{ key = "value", n = 1 }`

- Tablice (listy)
  - `dependencies = ["anthropic>=0.51.0", "mcp[cli]>=1.8.0"]`

- Tabele (sekcje)
  - Deklaracja: `[section]`, np. `[project]`
  - Zagnieżdżenie przez kropkę: `[tool.setuptools]`, `[database.postgres]`

- Tablice tabel (array of tables)
  - Użyj `[[table]]`:
    ```toml
    [[plugins]]
    name = "p1"

    [[plugins]]
    name = "p2"
    ```

- Klucze z kropkami vs. zagnieżdżone sekcje
  - `a.b = 1` to to samo co:
    ```toml
    [a]
    b = 1
    ```

---

## Mapowanie na `pyproject.toml`

W pliku `pyproject.toml` z tego repo:

```toml
[project]
name = "app"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
  "anthropic>=0.51.0",
  "mcp[cli]>=1.8.0",
  "prompt-toolkit>=3.0.51",
  "python-dotenv>=1.1.0",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = { find = { include = ["core*"], exclude = ["DOCS*"] } }
```

- `[project]` – główna sekcja metadanych projektu.
- `dependencies = [ ... ]` – tablica stringów (lista zależności).
- `[build-system]` – jak budować pakiet (backend + wymagane pakiety do budowy).
- `[tool.setuptools]` – ustawienia narzędzia `setuptools`.
- `packages = { ... }` – tabela inline z kluczami `find.include` i `find.exclude` (listy wzorców).

---

## Najczęstsze pułapki

- Brak spacji wokół `=` – w TOML wymagane są odstępy: `key = "value"`.
- Cudzysłowy dla stringów: używaj `"..."` albo `"""..."""` dla wielolinijkowych.
- Typy są ścisłe: `true`/`false` to booleany, nie stringi.
- Duplikowanie kluczy w tej samej tabeli jest niedozwolone.

---

## Minimalny szablon sekcji

```toml
[section]
string_key = "text"
int_key = 1
float_key = 3.14
bool_key = true
array_key = ["a", "b"]
inline_table = { a = 1, b = 2 }
```

---

## Dalsze źródła

- Specyfikacja: https://toml.io/en/
- PEP 621 (sekcja `[project]` w `pyproject.toml`): https://peps.python.org/pep-0621/

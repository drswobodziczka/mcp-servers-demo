# REDDIT-001: Context

> **Role:** Statyczna Baza Wiedzy. Definicja wymagań, kluczowe pliki i dane wejściowe. Czytaj na początku zadania.

## Task Description
Implementacja narzędzi MCP (Model Control Protocol) do analizy opinii użytkowników Reddit o konkretnych tematach. Narzędzia mają umożliwić wyszukiwanie postów, czytanie wątków z komentarzami i generowanie podsumowań TLDR.

## Requirements
- Wyszukiwanie postów Reddit na podstawie zapytania (w całym Reddit lub konkretnym subreddit)
- Czytanie postów wraz z komentarzami (konfigurowalna głębokość)
- Obsługa sortowania (relevance, hot, top, new) i filtrów czasowych
- Integracja z istniejącym MCP server (FastMCP)
- Preferowany SDK: PRAW (jeśli dostęp do API/credentials nie blokuje); alternatywy oceniane na etapie wznowienia

---

## Key Files
> Pliki kluczowe dla zrozumienia zadania (Context Map)

### Implementation Files
```bash
mcp_server.py              # Główny serwer MCP - tutaj dodamy nowe narzędzia
reddit/mcp_reddit_tools.py # Nowy moduł z narzędziami Reddit
```

### Reference Files
```bash
reddit/docs/reddit-api-and-praw-guide.md  # Dokumentacja Reddit API i PRAW SDK
reddit/docs/reddit-api-access-registration-pain.md  # Notatka o friction/approval w uzyskaniu API access
reddit/docs/reddit-api-terms-summary.md  # Podsumowanie warunków korzystania z Reddit API (2024)
reddit/docs/reddit-responsible-builder-policy-summary.md  # Responsible Builder Policy (2026)
mcp_client.py              # Przykład klienta MCP
```

### External References

- https://www.reddit.com/dev/api  # Reddit API docs
- https://www.reddit.com/r/reddit.com/wiki/api/#wiki_read_the_full_api_terms_and_sign_up_for_usage
- https://www.reddit.com/prefs/apps
- https://support.reddithelp.com/hc/en-us/requests/new
- https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy  # Responsible Builder Policy (2026)

---

## Current blockers / friction (stan na 2026)

- **Verified email required**: Przy tworzeniu aplikacji w `prefs/apps` Reddit może blokować akcję komunikatem: `you must have a verified email to create a new application`.
- **Explicit approval required**: Dostęp do Data API wymaga zatwierdzenia (Devvit-first + formularz wsparcia dla use-case poza Devvit).
- **Rate limits**: 100 req/min dla OAuth, 10 req/min bez OAuth.
- **Responsible Builder Policy (2026)**: Zakazuje komercjalizacji, AI training i user profiling bez pisemnej zgody. Wymaga transparentności i respect rate limits.

Wniosek: implementację można prowadzić w trybie mock-first, a wybór biblioteki/runtime provider (PRAW vs alternatywa) odłożyć do momentu, gdy uzyskanie accessu będzie klarowne.

## Reference implementations (Reddit MCP servers)

- https://github.com/Hawstein/mcp-server-reddit
  - Implementacja MCP oparta o `redditwarp` (w kodzie inicjalizacja klienta bez env varów).
- https://github.com/adhikasp/mcp-reddit
  - MCP oparty o `redditwarp` (ASYNC), credentials opcjonalne (env: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_REFRESH_TOKEN`).
- https://github.com/Arindam200/reddit-mcp
  - MCP oparty o PRAW; read-only na `client_id/client_secret`, write ops po `username/password`.

---

## OAuth / redirect URI (dlaczego localhost?)

W OAuth `redirect_uri` to adres, na który Reddit przekierowuje przeglądarkę po udanej autoryzacji, aby aplikacja mogła odebrać kod (lub token) i dokończyć logowanie.

W przypadku aplikacji uruchamianej lokalnie (dev / personal use) najprostszy wariant to callback na `localhost`, np. `http://localhost:8080`:

- nie wymaga wystawiania endpointu publicznie w internecie
- pozwala jednorazowo „złapać” kod autoryzacji w przeglądarce
- jest standardowym ustawieniem dla aplikacji instalowanych / developerskich

Uwaga: w naszym use-case (tylko odczyt publicznych danych) często wystarczy PRAW w trybie `read_only=True` i nie musimy przechodzić interaktywnego flow z redirectem, ale `redirect_uri` może być nadal wymagany na etapie rejestracji aplikacji i przy ewentualnym rozszerzeniu uprawnień.

## Example Data / Screenshots

### Expected Workflow
```python
# 1. Search posts
posts = search_reddit("AI tools", sort="top", time_filter="month", limit=10)

# 2. Read thread
thread = read_reddit_thread("abc123", comment_limit=50, expand_replies=False)

# 3. AI generates TLDR summary
# 4. Optional deep dive on user request
```

### Expected Response Format
```json
{
  "posts": [
    {
      "id": "abc123",
      "title": "Best AI tools for developers",
      "score": 1500,
      "num_comments": 234,
      "url": "https://reddit.com/r/programming/comments/abc123",
      "selftext": "..."
    }
  ]
}
```

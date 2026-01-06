# REDDIT-001: Implement Reddit MCP Tools for Opinion Analysis

> **Role:** Dynamiczne Centrum Dowodzenia (SSOT). Tu sprawdzasz status, planujesz ruchy i zapisujesz decyzje.
> **Context:** Patrz plik `REDDIT-001-context.md`
> **Worklog:** Patrz plik `REDDIT-001-tasks.md`

## 🚦 Status Dashboard

*   **Current State:** 🟠 Parked (blocked by external requirements)
*   **Current Focus:** Reddit API access friction (verified email + approval/Devvit)
*   **Immediate Next Action:** Wznowić po odblokowaniu tworzenia appki / uzyskaniu API access (lub decyzji o alternatywnym providerze)

---

## 🧠 Memory Dump (Kluczowe ustalenia z ostatniej sesji)
*   Reddit API free tier: 100 QPM (queries per minute) - wystarczające dla personal use
*   PRAW SDK > REST API - automatyczne rate limiting, authentication, paginacja
*   KISS architecture: tylko 2 narzędzia (search_reddit, read_reddit_thread)
*   Performance: top-level comments = 1 API call, pełny wątek = 5-20+ API calls
*   Domyślne: comment_limit=50, expand_replies=False (szybkie)
*   **Testing stack:** pytest + pytest-anyio + `create_connected_server_and_client_session` (MCP in-memory testing)
*   **Blocker:** Reddit może wymagać zweryfikowanego emaila do stworzenia appki w `prefs/apps`
*   **Friction:** "Ending Self-Service API access" + Devvit-first + formularz approval (dla use-case poza Devvit)
*   **Alternatywy (do rozważenia po wznowieniu):** redditwarp-based MCP servers (Hawstein/mcp-server-reddit, adhikasp/mcp-reddit) vs PRAW-based (Arindam200/reddit-mcp)

---

## ✅ Acceptance Criteria
*   [ ] search_reddit tool finds posts by query with optional subreddit filter
*   [ ] read_reddit_thread tool reads post + comments with configurable limits
*   [ ] Tools integrated with existing FastMCP server
*   [ ] Proper error handling for Reddit API limits and authentication
*   [ ] Documentation and examples in repo

---

## 🏗️ Architectural Decisions (ADR Log)
> Decyzje podjęte w trakcie tego zadania. Na koniec przenieś kluczowe do globalnej dokumentacji.

### Decision #1: PRAW SDK over REST API
*   **Context:** Wybór między ręcznymi HTTP requestami a Python wrapper
*   **Decision:** Używamy PRAW SDK - automatyzuje auth, rate limiting, paginację
*   **Consequence:** Mniej kodu, mniej błędów, szybsza implementacja

### Decision #2: KISS Tool Architecture
*   **Context:** Możliwość wielu narzędzi (find_subreddits, search_posts, read_comments, etc.)
*   **Decision:** Tylko 2 narzędzia: search_reddit + read_reddit_thread
*   **Consequence:** Prostsza implementacja, łatwiejsze użycie, wystarczające dla workflow

---

## 📋 Implementation Plan

### Phase 1: Setup & Dependencies

| Step | Task | Test w izolacji |
|------|------|------------------|
| 1.1 | [x] Research Reddit API capabilities and limits | N/A - research |
| 1.2 | [x] Create documentation in reddit/docs/ | N/A - docs |
| 1.3 | [x] Setup task structure in reddit/docs/ | N/A - docs |
| 1.4 | [ ] Add PRAW dependency to pyproject.toml | `uv pip install -e .` - brak błędów |
| 1.5 | [ ] Add test dependencies (pytest, pytest-anyio) | `uv run pytest --version` |

### Phase 2: Reddit API Configuration

| Step | Task | Test w izolacji |
|------|------|------------------|
| 2.0 | [ ] Zweryfikuj email na koncie Reddit (wymagane do tworzenia appki) | `prefs/apps` pozwala kliknąć "create app" bez błędu |
| 2.1 | [ ] Uzyskaj Reddit API credentials (client_id, client_secret) | Sprawdź na https://www.reddit.com/prefs/apps |
| 2.2 | [ ] Dodaj credentials do .env (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET) | `cat .env \| grep REDDIT` |
| 2.3 | [ ] Stwórz reddit/client.py z inicjalizacją PRAW | Script test: `python -c "from reddit.client import get_reddit; r=get_reddit(); print(r.read_only)"` → `True` |

### Phase 3: Core Implementation

| Step | Task | Test w izolacji |
|------|------|------------------|
| 3.1 | [ ] Implement search_reddit function | Script test: `python -c "from reddit.tools import search_reddit; print(search_reddit('python', limit=3))"` |
| 3.2 | [ ] Implement read_reddit_thread function | Script test: `python -c "from reddit.tools import read_reddit_thread; print(read_reddit_thread('POST_ID'))"` |
| 3.3 | [ ] Create MCP tool wrappers in reddit/mcp_tools.py | Import test: `python -c "from reddit.mcp_tools import *"` |
| 3.4 | [ ] Integrate tools with mcp_server.py | Import test: `python -c "import mcp_server"` |

### Phase 4: Unit & Integration Testing

| Step | Task | Test w izolacji |
|------|------|------------------|
| 4.1 | [ ] Unit test: reddit/client.py (mock PRAW) | `uv run pytest tests/test_client.py` |
| 4.2 | [ ] Unit test: reddit/tools.py (mock Reddit API) | `uv run pytest tests/test_tools.py` |
| 4.3 | [ ] MCP integration test: search_reddit | `uv run pytest tests/test_mcp_reddit.py` (in-memory session) |
| 4.4 | [ ] MCP integration test: read_reddit_thread | `uv run pytest tests/test_mcp_reddit.py` |
| 4.5 | [ ] E2E test: pełny workflow przez MCP client | `uv run python main.py` → manual test |

### Phase 5: Documentation & Cleanup

| Step | Task | Test w izolacji |
|------|------|------------------|
| 5.1 | [ ] Update README with usage examples | N/A - docs |
| 5.2 | [ ] Add error handling for rate limits | Simulate rate limit (optional) |
| 5.3 | [ ] Commit and push changes | `git status`, `git log` |

---

## 🔮 Options for Evolution / Refactor
> Pomysły, które pojawiły się "przy okazji", ale są poza zakresem (Out of Scope) tego zadania.
*   [ ] Async PRAW for concurrent processing
*   [ ] Caching layer for frequently accessed posts
*   [ ] Sentiment analysis integration
*   [ ] Multi-subreddit search with relevance scoring

---

## 🐛 Open Issues & Architectural Concerns
> Pytania bez odpowiedzi, ryzyka, blokery.
*   [ ] Reddit API credentials storage - environment variables vs config file
*   [ ] Reddit app registration blocker: verified email required for creating new application
*   [ ] Approval / Devvit-first flow may be required for new OAuth access (external dependency)
*   [ ] Provider decision: PRAW vs redditwarp (keep KISS tools stable, switch provider underneath)
*   [ ] Rate limiting strategy for high-volume usage
*   [ ] Error handling for deleted/private posts

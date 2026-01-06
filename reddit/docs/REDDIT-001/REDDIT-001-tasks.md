# REDDIT-001: Implementation History (Worklog)

 > **Role:** Dziennik Zdarzeń (Append-Only). Chronologiczny zapis tego CO i KIEDY zostało zrobione. Używaj do raportowania postępów, nie do planowania.
 > Ten plik służy jako archiwum wykonanych prac. Bieżący stan sprawdzaj w `REDDIT-001-plan.md`.

---

## 2026-01-06 - Phase 0/1: Brainstorm → requirements → plan + docs
 
 **Implemented:**
 - Doprecyzowano use-case: "dowiedzieć się co Reddit myśli o X" (search → wybór top postów → próbka wątków → TLDR → opcjonalny deep dive).
 - Ustalono architekturę KISS: 2 narzędzia MCP: `search_reddit` + `read_reddit_thread`.
 - Ustalono test stack: `pytest` + `pytest-anyio` + MCP in-memory (`create_connected_server_and_client_session`).
 
 **Files Changed:**
 - `reddit/docs/reddit-api-and-praw-guide.md`
 - `reddit/docs/REDDIT-001/REDDIT-001-context.md`
 - `reddit/docs/REDDIT-001/REDDIT-001-plan.md`
 
 **Notes:**
 - Performance: pełne rozwijanie komentarzy ("MoreComments") może generować dużo requestów; domyślnie ograniczamy zakres.
 
 ---
 
 ## 2026-01-06 - Phase 1/2: Reddit API access friction (research)
 
 **Implemented:**
 - Zidentyfikowano, że Reddit wprowadził friction dot. dostępu do Data API (approval/Devvit-first) i że proces może nie być już "self-service".
 - Zebrano publiczne źródło z `r/redditdev` dot. "Ending Self-Service API access".
 - Przeanalizowano artykuł PainOnSocial (2026) opisujący klasyczny flow `prefs/apps` + PRAW.
 
 **Files Changed:**
 - `reddit/docs/reddit-api-access-registration-pain.md`
 
 **Notes:**
 - Artykuły how-to mogą opisywać klasyczny flow `prefs/apps`, ale praktycznie nadal może być wymagany approval.
 
 ---
 
 ## 2026-01-06 - Phase 2: Alternatywne implementacje (reference MCP servers)
 
 **Implemented:**
 - Zebrano referencje do istniejących Reddit MCP serverów:
   - `Hawstein/mcp-server-reddit` (redditwarp, inicjalizacja klienta bez env varów)
   - `adhikasp/mcp-reddit` (redditwarp ASYNC, credentials opcjonalne)
   - `Arindam200/reddit-mcp` (PRAW, read-only + write ops)
 - Dodano do kontekstu zadania (bez podejmowania decyzji o providerze).
 
 **Files Changed:**
 - `reddit/docs/REDDIT-001/REDDIT-001-context.md`
 
 **Notes:**
 - Założenie na przyszłość: stabilne API narzędzi MCP, możliwość podmiany providerów (PRAW vs redditwarp) "pod spodem".
 
 ---
 
 ## 2026-01-06 - Phase 2: Responsible Builder Policy (summary)
 
 **Implemented:**
 - Zrobiono streszczenie Responsible Builder Policy (wymagany approval, transparentność, limity, privacy, zakaz AI training bez zgody, zasady dla botów).
 
 **Files Changed:**
 - `reddit/docs/reddit-responsible-builder-policy-summary.md`
 
 **Notes:**
 - Dla naszego use-case kluczowe: read-only, ograniczanie zakresu, brak wnioskowania o wrażliwych cechach użytkowników.
 
 ---
 
 ## 2026-01-06 - Status update: Parked → partially unblocked
 
 **Implemented:**
 - Udokumentowano blocker "verified email required" dla `prefs/apps` i późniejsze odblokowanie po weryfikacji email.
 - Utrzymano zadanie jako możliwe do wznowienia po decyzji dot. access/approval i wyborze providera.
 
 **Files Changed:**
 - `reddit/docs/REDDIT-001/REDDIT-001-plan.md`
 - `reddit/docs/REDDIT-001/REDDIT-001-context.md`
 
 **Notes:**
 - To jest zależność zewnętrzna (Reddit), więc plan celowo zawiera ścieżkę "mock-first" na wypadek opóźnień w approval.

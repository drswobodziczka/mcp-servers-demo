# Hook (Template Method) w praktyce — krótko

- "Hook" to nadpisywana w podklasie metoda wywoływana przez metodę szablonową (Template Method) klasy bazowej.
- W tym repo: `Chat.run()` (klasa bazowa w `core/chat.py`) zawsze woła `_process_query()` jako krok przygotowania wejścia.
- `CliChat` (w `core/cli_chat.py`) nadpisuje `_process_query()` i wstrzykuje własne przetwarzanie: obsługa komend `/...`, wstawianie treści dokumentów `@doc`, budowa bogatszego promptu.
- Rdzeń pętli rozmowy, integracja z narzędziami MCP i agregacja wiadomości pozostają w `Chat.run()` — reużycie i testowalność.

Szkic przepływu:
```
Chat.run()  ->  self._process_query(query)  # hook
            ->  claude_service.chat(...)
            ->  ToolManager.execute_tool_requests(...)
            ->  return final_text_response
```

Korzyść: specjalizujesz tylko krok wejścia bez kopiowania pętli dialogowej (klasyczny wzorzec Template Method).

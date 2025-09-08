---
description: Python async context managers, __aenter__/__aexit__, with/async with, and MCPClient lifecycle
---

# Python: async context manager, `with`/`async with`, i MCPClient (krótko)

- __Co to jest async context manager?__
  - Obiekt, który zarządza cyklem życia zasobu asynchronicznie: otwarcie przy wejściu do bloku i sprzątanie przy wyjściu.
  - Implementuje metody specjalne: `__aenter__` i `__aexit__` (asynchroniczne odpowiedniki `__enter__`/`__exit__`).

- __Składnia i mechanika__
  - Sync: `with obj as x:` wywołuje `obj.__enter__()` na starcie i `obj.__exit__(exc_type, exc, tb)` na końcu (również w razie wyjątku).
  - Async: `async with obj as x:` wywołuje `await obj.__aenter__()` oraz `await obj.__aexit__(exc_type, exc, tb)`.
  - Gwarancja: „sprzątanie” jest wywołane zawsze, nawet gdy w bloku poleci wyjątek.

- __Analogia do Javy__
  - Najbliższy odpowiednik: `try-with-resources` + `AutoCloseable`.
    ```java
    try (MyRes r = new MyRes()) {
        // użycie r
    } // r.close() wywołane zawsze
    ```
  - Różnica: w Pythonie mamy natywne wsparcie dla wariantu asynchronicznego (`async with`).

## W tym repo: rola i cykl życia `MCPClient`

Plik: `mcp_client.py`

- __Cel klasy `MCPClient`__
  - Uruchomić proces serwera MCP przez STDIO oraz zestawić nad nim sesję MCP.
  - Zarządzać cyklem życia: start procesu + inicjalizacja sesji + sprzątanie.

- __Główne elementy i warstwy__
  - `contextlib.AsyncExitStack` (Python stdlib): łączy wiele async context managerów i pozwala je domknąć jednym `aclose()`.
  - `mcp.client.stdio.stdio_client(...)` (biblioteka `mcp` + OS):
    - startuje proces serwera MCP (np. `uv run mcp_server.py`),
    - udostępnia transport po STDIN/STDOUT, zwracając krotkę `(stdio, write)`.
  - `mcp.ClientSession(stdio, write)` (biblioteka `mcp`):
    - zestawia sesję protokołu MCP nad transportem,
    - `initialize()` wykonuje handshake.

- __Przepływ w `MCPClient.connect()`__
  ```python
  server_params = StdioServerParameters(command, args, env)

  # 1) Start procesu MCP i ustanowienie transportu STDIO
  stdio_transport = await self._exit_stack.enter_async_context(
      stdio_client(server_params)
  )
  _stdio, _write = stdio_transport

  # 2) Utworzenie sesji nad transportem
  self._session = await self._exit_stack.enter_async_context(
      ClientSession(_stdio, _write)
  )

  # 3) Handshake protokołu
  await self._session.initialize()
  ```

- __Wejście/wyjście z kontekstu na poziomie klasy__
  ```python
  async def __aenter__(self):
      await self.connect()     # start procesu + sesja + handshake
      return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
      await self.cleanup()     # AsyncExitStack.aclose() – domyka wszystko
  ```

- __Użycie__
  ```python
  async with MCPClient(command="uv", args=["run", "mcp_server.py"]) as client:
      # sesja gotowa do użycia
      ...
  # po wyjściu: proces i sesja domknięte poprawnie
  ```

## Metody specjalne (dunder) `__aenter__` / `__aexit__`

- __Co oznaczają podwójne podkreślenia?__
  - „dunder methods” = metody protokołów języka wywoływane pośrednio przez składnię, np. `with`, operatory, iterację.
  - Nie wywołujesz ich bezpośrednio w normalnym kodzie — robi to za Ciebie interpreter przy `async with`.

## TL;DR

- `with`/`async with` = deterministyczne zarządzanie zasobami (również przy wyjątkach).
- `__aenter__/__aexit__` to asynchroniczne haki wywoływane przez `async with`.
- W `MCPClient`: `stdio_client` uruchamia serwer i daje transport, `ClientSession` robi handshake i obsługuje RPC, a `AsyncExitStack` składa to wszystko i sprząta w poprawnej kolejności.

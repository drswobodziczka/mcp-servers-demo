---
description: Minimal Java sketch mirroring Python MCPClient (process + STDIO + session + deterministic cleanup)
---

# Java: minimalny szkic `McpClient` (porównanie do `MCPClient` w Pythonie)

Poniżej prosty szkic pokazujący:
- start procesu serwera (np. `uv run mcp_server.py`),
- związanie strumieni STDIO jako transportu,
- utworzenie sesji nad transportem,
- deterministyczne sprzątanie przez `AutoCloseable` i `try-with-resources`.

```java
// Java 17+
import java.io.*;
import java.util.*;

// Placeholder: odpowiednik pythonowego ClientSession nad STDIO
final class ClientSession implements Closeable {
  private final InputStream in;   // server -> client
  private final OutputStream out; // client -> server

  ClientSession(InputStream in, OutputStream out) {
    this.in = in;
    this.out = out;
  }

  // Handshake / init protokołu
  public void initialize() throws IOException {
    // TODO: implement MCP handshake over JSON-RPC on (in/out)
    // e.g., send initialize request, await response
  }

  @Override
  public void close() throws IOException {
    // Zamknij zasoby specyficzne sesji, jeśli potrzebne
    // (często wystarczy domknięcie strumieni procesu w McpClient.close())
  }
}

public final class McpClient implements AutoCloseable {
  private final String command;
  private final List<String> args;
  private final Map<String, String> env;

  private Process process;
  private ClientSession session;

  public McpClient(String command, List<String> args, Map<String, String> env) {
    this.command = command;
    this.args = List.copyOf(args);
    this.env = (env == null) ? Map.of() : Map.copyOf(env);
  }

  // Odpowiednik MCPClient.connect()
  public void connect() throws IOException {
    // 1) Start procesu MCP (np. "uv run mcp_server.py")
    List<String> cmd = new ArrayList<>();
    cmd.add(command);
    cmd.addAll(args);

    ProcessBuilder pb = new ProcessBuilder(cmd);
    pb.redirectError(ProcessBuilder.Redirect.INHERIT); // logi błędów na stderr
    if (!env.isEmpty()) {
      pb.environment().putAll(env);
    }

    this.process = pb.start();

    // 2) Transport STDIO
    InputStream stdioIn = process.getInputStream();   // co serwer pisze (my czytamy)
    OutputStream stdioOut = process.getOutputStream(); // co my piszemy do serwera

    // 3) Sesja nad transportem + handshake
    this.session = new ClientSession(stdioIn, stdioOut);
    this.session.initialize();
  }

  public ClientSession session() {
    if (session == null) {
      throw new IllegalStateException("Client session not initialized. Call connect() first.");
    }
    return session;
  }

  @Override
  public void close() throws IOException {
    // Sprzątanie w odwróconej kolejności
    if (session != null) {
      try { session.close(); } catch (IOException ignored) {}
      session = null;
    }
    if (process != null) {
      try { process.getOutputStream().close(); } catch (IOException ignored) {}
      try { process.getInputStream().close(); } catch (IOException ignored) {}
      try { process.getErrorStream().close(); } catch (IOException ignored) {}
      process.destroy();
      process = null;
    }
  }

  // Mini demo: odpowiednik "async with MCPClient(...) as client" w Pythonie
  public static void main(String[] args) throws Exception {
    try (McpClient client = new McpClient(
        "uv",
        List.of("run", "mcp_server.py"),
        Map.of()
    )) {
      client.connect();
      ClientSession sess = client.session();
      // TODO: wywołania MCP (narzędzia, prompty, zasoby) przez sess
    } // zawsze close(): sesja i proces zostaną domknięte
  }
}
```

Kluczowe mapowania względem `mcp_client.py`:
- `MCPClient.__aenter__/__aexit__` ↔ `AutoCloseable.close()` + `try-with-resources`.
- `stdio_client(params)` (spawn procesu + STDIO) ↔ `ProcessBuilder.start()`.
- `ClientSession(...).initialize()` ↔ handshake MCP nad STDIO.
- `AsyncExitStack` ↔ manualne domknięcie w `close()` (kolejność odwrotna do tworzenia).

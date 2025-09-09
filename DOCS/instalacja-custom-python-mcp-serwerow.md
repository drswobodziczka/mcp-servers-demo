# Instalacja Custom Python MCP Serwerów Lokalnych

#mcp-speech #wazne #demos #custom-mcp

## Dla Claude Code

### 1. Dodanie Globalnego MCP Serwera
```bash
# Składnia ogólna
claude mcp add <nazwa_serwera> -s user -- <komenda_uruchomienia>

# Przykład z npx (oficjalne serwery)
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem

# Przykład z lokalnym Pythonserwerem
claude mcp add my-docs -s user -- python /path/to/mcp_server.py

# Z UV
claude mcp add my-docs -s user -- uv run /path/to/mcp_server.py
```

### 2. Development Mode - Lokalne Serwery
```bash
# Uruchomienie z dodatkowymi serwerami
python main.py hello/server.py

# Z UV (zalecane)
USE_UV=1 python main.py hello/server.py

# Testowanie serwera standalone
python mcp_server.py
uv run mcp_server.py
```

## Dla Claude Desktop

### 1. Lokalizacja Konfiguracji
```bash
# macOS
~/Library/Application Support/Claude/claude_desktop_config.json

# Windows
%APPDATA%/Claude/claude_desktop_config.json
```

### 2. Przykład Konfiguracji JSON
```json
{
  "mcpServers": {
    "my-docs": {
      "command": "python",
      "args": ["/path/to/your/mcp_server.py"]
    },
    "with-uv": {
      "command": "uv",
      "args": ["run", "/path/to/your/mcp_server.py"]
    },
    "with-environment": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

## Struktura Przykładowego Projektu
```
mcp-servers-demo/
├── mcp_server.py          # Główny serwer dokumentów
├── hello/server.py        # Przykładowy serwer
├── mcp_client.py         # Klient MCP
├── main.py               # Entry point z multi-server support
└── core/                 # Logika chatu i CLI
```

## Kluczowe Cechy

### Multi-Client Architecture
- Jeden dedykowany `doc_client` dla operacji na dokumentach
- Dodatkowe klienty tworzone dynamicznie z argumentów
- Automatyczne routowanie narzędzi do właściwego klienta

### Development Features
- **UV Support**: `USE_UV=1` dla lepszego zarządzania pakietami
- **STDIO Transport**: Serwery MCP jako osobne procesy
- **Async Context Management**: Proper cleanup zasobów
- **Windows Compatibility**: `WindowsProactorEventLoopPolicy`

## Quick Start
```bash
# 1. Sklonuj repo
git clone <repo-url>

# 2. Skonfiguruj środowisko
cp .env.example .env
# Ustaw CLAUDE_MODEL i ANTHROPIC_API_KEY

# 3. Uruchom z custom serwerem
USE_UV=1 python main.py hello/server.py

# 4. Dodaj do Claude Code globalnie
claude mcp add my-demo -s user -- python $(pwd)/mcp_server.py
```

## Debugowanie
```bash
# Test serwera standalone
python mcp_server.py

# Test klienta MCP
python mcp_client.py

# Sprawdź połączenia w Claude Code
# Narzędzia pojawią się automatycznie po udanej konfiguracji
```
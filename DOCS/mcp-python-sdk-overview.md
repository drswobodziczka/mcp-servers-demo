# MCP Python SDK - Fundamentalne Funkcjonalności i Architektura

## Fasada Biblioteki - Główne Klasy i Interfejsy

### 🎯 **FastMCP** - Główna Fasada

```python
from mcp.server.fastmcp import FastMCP

# Centralna klasa do tworzenia serwerów MCP
mcp = FastMCP("Nazwa Serwera")
```

**FastMCP** to główna fasada biblioteki, która:

- Obsługuje protokół MCP w sposób deklaratywny
- Automatycznie zarządza połączeniami i sesjami
- Dostarcza decoratory do definiowania funkcjonalności
- Wspiera różne transporty (stdio, HTTP, SSE)

### 🧩 **Główne Komponenty Architektury**

**1. Server-Side (Tworzenie serwerów)**

- `FastMCP` - fasada high-level
- `Server` - implementacja low-level
- `Context` - dostęp do capabilities MCP

**2. Client-Side (Tworzenie klientów)**

- `ClientSession` - sesja klienta
- Transport adaptery: `stdio_client`, `streamablehttp_client`
- Authentication providers: `OAuthClientProvider`

**3. Transport Layer**

- **stdio** - standardowe wejście/wyjście
- **streamable-http** - HTTP z streaming
- **SSE** - Server-Sent Events

## Filozofia Działania MCP

MCP (Model Context Protocol) działa na zasadzie **protokołu żądanie-odpowiedź** między:

- **Klient MCP** (np. Claude Desktop, custom client)
- **Serwer MCP** (Twoja aplikacja udostępniająca zasoby)

**Trzy główne typy funkcjonalności:**

1. **Resources** - dane tylko do odczytu (jak GET endpoint)
2. **Tools** - akcje z efektami ubocznymi (jak POST endpoint)
3. **Prompts** - szablony interakcji z LLM

## Implementacja Serwera MCP

### 🔧 Podstawowy Server

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo Server")

# 1. TOOL - akcje z efektami ubocznymi
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Dodaje dwie liczby"""
    return a + b

# 2. RESOURCE - dane tylko do odczytu  
@mcp.resource("config://settings")
def get_settings() -> str:
    """Pobiera ustawienia aplikacji"""
    return '{"theme": "dark", "lang": "pl"}'

# 3. PROMPT - szablon interakcji
@mcp.prompt()
def code_review(code: str) -> str:
    """Szablon do review kodu"""
    return f"Proszę zrewać ten kod:\n\n{code}"

# Uruchomienie serwera
if __name__ == "__main__":
    mcp.run()  # Domyślnie stdio transport
```

### 🚀 Zaawansowany Server z Context

```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

mcp = FastMCP("Advanced Server")

@mcp.tool()
async def process_data(
    data: str, 
    ctx: Context[ServerSession, None]  # Automatycznie injektor
) -> str:
    """Tool z dostępem do MCP capabilities"""
    
    # Logowanie 
    await ctx.info(f"Przetwarzam: {data}")
    
    # Progress reporting
    await ctx.report_progress(0.5, message="Przetwarzanie...")
    
    # Czytanie zasobów
    config = await ctx.read_resource("config://settings")
    
    # Interakcja z użytkownikiem
    result = await ctx.elicit(
        "Potrzebuję dodatkowych informacji", 
        schema={"type": "string"}
    )
    
    return f"Przetworzone: {data}"
```

### 🔄 Server Lifecycle Management

```python
from contextlib import asynccontextmanager
from dataclasses import dataclass

class Database:
    async def connect(self): return self
    async def disconnect(self): pass
    def query(self): return "data"

@dataclass  
class AppContext:
    db: Database

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    # Startup
    db = Database()
    await db.connect()
    try:
        yield AppContext(db=db)
    finally:
        # Shutdown  
        await db.disconnect()

mcp = FastMCP("App", lifespan=app_lifespan)

@mcp.tool()
def query_db(ctx: Context) -> str:
    # Dostęp do zasobów z lifecycle
    db = ctx.request_context.lifespan_context.db
    return db.query()
```

## Implementacja Klienta MCP

### 📡 Podstawowy Klient (stdio)

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def main():
    # Konfiguracja połączenia ze serwerem
    server_params = StdioServerParameters(
        command="python",
        args=["moj_serwer.py"]  
    )
    
    # Połączenie i sesja
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializacja
            await session.initialize()
            
            # Listowanie dostępnych narzędzi  
            tools = await session.list_tools()
            print(f"Tools: {[t.name for t in tools.tools]}")
            
            # Wywołanie narzędzia
            result = await session.call_tool(
                "add_numbers", 
                {"a": 5, "b": 3}
            )
            print(f"Wynik: {result}")
            
            # Odczyt zasobu
            resource = await session.read_resource("config://settings")
            print(f"Config: {resource}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 🌐 Klient HTTP z Autentykacją

```python
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.auth import OAuthClientProvider, TokenStorage

class SimpleTokenStorage(TokenStorage):
    def __init__(self):
        self.tokens = None
    
    async def get_tokens(self):
        return self.tokens
        
    async def set_tokens(self, tokens):
        self.tokens = tokens

async def http_client():
    # OAuth provider
    oauth = OAuthClientProvider(
        server_url="http://localhost:8001",
        client_metadata={
            "client_name": "Test Client",
            "redirect_uris": ["http://localhost:3000/callback"],
            "grant_types": ["authorization_code"]
        },
        storage=SimpleTokenStorage()
    )
    
    # Połączenie HTTP
    async with streamablehttp_client(
        "http://localhost:8001/mcp", 
        auth=oauth
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = await session.list_tools()  
            print(f"Dostępne narzędzia: {[t.name for t in tools.tools]}")
```

## Kluczowe Wzorce i Zastosowania

### 🎯 **Structured Output** - Silnie Typowane Wyniki

```python
from pydantic import BaseModel
from typing import TypedDict

class WeatherData(BaseModel):
    temperature: float
    condition: str
    humidity: float

@mcp.tool()  
def get_weather(city: str) -> WeatherData:
    """Zwraca strukturalne dane pogodowe"""
    return WeatherData(
        temperature=22.5,
        condition="sunny", 
        humidity=45.0
    )
```

### 🔄 **Resource Templates** - Dynamiczne Zasoby

```python
@mcp.resource("file://documents/{filename}")
def read_document(filename: str) -> str:
    """Dynamiczny zasób z parametrami w URI"""
    with open(f"docs/{filename}", 'r') as f:
        return f.read()
```

### 🤖 **Sampling** - Interakcja z LLM

```python
@mcp.tool()
async def generate_text(prompt: str, ctx: Context) -> str:
    """Generuje tekst używając LLM"""
    result = await ctx.session.create_message(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return result.content.text
```

## Transporty i Uruchamianie

### 📟 **STDIO Transport** (Domyślny)

```python
# Uruchomienie z stdio (stdin/stdout)
mcp.run()  # lub mcp.run(transport="stdio")

# Testowanie z klientem
server_params = StdioServerParameters(
    command="python", 
    args=["server.py"]
)
```

### 🌐 **HTTP Transport**

```python
# Uruchomienie HTTP server
mcp.run(transport="streamable-http", port=8080)

# Klient HTTP
async with streamablehttp_client("http://localhost:8080/mcp") as (r, w, _):
    async with ClientSession(r, w) as session:
        # ... interakcja
```

### ⚡ **SSE Transport**

```python
# Server-Sent Events
mcp.run(transport="sse", port=8080)
```

## Context API - Capabilities MCP

### 📋 **Właściwości Context**

```python
async def my_tool(data: str, ctx: Context) -> str:
    # Metadane żądania
    request_id = ctx.request_id
    client_id = ctx.client_id
    
    # Dostęp do serwera i sesji
    server = ctx.fastmcp
    session = ctx.session
    
    # Lifecycle context (jeśli zdefiniowany)
    lifespan_data = ctx.request_context.lifespan_context
```

### 📝 **Logowanie**

```python
await ctx.debug("Debug message")
await ctx.info("Info message") 
await ctx.warning("Warning message")
await ctx.error("Error message")
await ctx.log("custom", "Custom level message", "logger_name")
```

### 📊 **Progress Reporting**

```python
# Raportowanie postępu
await ctx.report_progress(
    progress=0.5,           # 50% ukończenia
    total=1.0,              # z całości 
    message="Przetwarzanie..."
)
```

### 🔄 **Resource Access**

```python
# Czytanie innych zasobów
resource_data = await ctx.read_resource("config://database")
```

### 💬 **User Interaction (Elicitation)**

```python
from pydantic import BaseModel

class UserInput(BaseModel):
    confirm: bool
    reason: str

# Pytanie użytkownika o dodatkowe dane
result = await ctx.elicit(
    message="Czy kontynuować operację?",
    schema=UserInput
)

if result.action == "accept" and result.data:
    if result.data.confirm:
        print(f"Kontynuujemy: {result.data.reason}")
```

## Authentication & Security

### 🔐 **OAuth 2.1 Server**

```python
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings

class MyTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        # Weryfikacja tokenu
        return AccessToken(subject="user123", scopes=["read", "write"])

mcp = FastMCP(
    "Secure Server",
    token_verifier=MyTokenVerifier(),
    auth=AuthSettings(
        issuer_url="https://auth.example.com",
        resource_server_url="http://localhost:3001",
        required_scopes=["user"]
    )
)
```

### 🔑 **OAuth Client**

```python
# Klient z OAuth
oauth_provider = OAuthClientProvider(
    server_url="http://localhost:8001",
    client_metadata=OAuthClientMetadata(
        client_name="My Client",
        redirect_uris=["http://localhost:3000/callback"],
        grant_types=["authorization_code", "refresh_token"],
        scope="user"
    ),
    storage=TokenStorage(),
    redirect_handler=handle_redirect,
    callback_handler=handle_callback
)
```

## Low-Level API

### 🔧 **Low-Level Server**

```python
import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions

server = Server("low-level-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [types.Tool(name="example", description="Example tool")]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=f"Result: {arguments}")]

async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            InitializationOptions(
                server_name="example",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions()
                )
            )
        )
```

## Instalacja i Setup

### 📦 **Instalacja**

```bash
# Z uv (zalecane)
uv add "mcp[cli]"

# Z pip
pip install "mcp[cli]"
```

### 🚀 **Szybki Start**

```bash
# Tworzenie projektu
uv init mcp-server-demo
cd mcp-server-demo
uv add "mcp[cli]"

# Uruchomienie serwera
uv run python server.py

# Testing z MCP Inspector
uv run mcp dev server.py

# Instalacja w Claude Desktop
uv run mcp install server.py
```

## Podsumowanie API

### **Server API (FastMCP):**

- `@mcp.tool()` - definiuje narzędzia
- `@mcp.resource(uri)` - definiuje zasoby
- `@mcp.prompt()` - definiuje prompty
- `mcp.run(transport)` - uruchamia serwer

### **Client API:**

- `ClientSession` - główna sesja klienta
- `session.list_tools()` - lista narzędzi
- `session.call_tool(name, args)` - wywołanie narzędzia
- `session.read_resource(uri)` - odczyt zasobu
- `session.get_prompt(name, args)` - pobranie promptu

### **Context API:**

- `ctx.info/debug/error()` - logowanie
- `ctx.report_progress()` - raportowanie postępu
- `ctx.elicit()` - interakcja z użytkownikiem
- `ctx.read_resource()` - dostęp do zasobów

### **Capabilities:**

- **prompts** - zarządzanie promptami
- **resources** - udostępnianie zasobów
- **tools** - wykonywanie narzędzi
- **logging** - konfiguracja logowania
- **completions** - podpowiedzi argumentów

---

MCP Python SDK dostarcza **kompletną, wysokopoziomową abstrakcję** do budowania zarówno serwerów jak i klientów MCP z **minimalnym boilerplate** i **maksymalną funkcjonalnością**.

Filozofia SDK opiera się na **deklaratywnym podejściu** - definiujesz co chcesz udostępnić, a SDK zajmuje się całą infrastrukturą protokołu MCP.

#mcp-sdk #mcp-servers #mcp-python-sdk #mcp #mcp-speech
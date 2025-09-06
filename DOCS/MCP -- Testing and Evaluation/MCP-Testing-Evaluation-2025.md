# MCP -- Testy i Ewaluacja: Kompletny Przewodnik 2025

> **Skuteczne, wiarygodne i efektywne testowanie serwerów Model Context Protocol**

## Streszczenie Wykonawcze

Model Context Protocol (MCP) to rewolucyjny protokół umożliwiający AI dostęp do zewnętrznych narzędzi i danych. Jednak **testing i ewaluacja serwerów MCP wymagają specjalistycznego podejścia** różniącego się znacząco od tradycyjnych aplikacji. Niniejszy dokument przedstawia **kompletną metodologię testowania** opartą na oficjalnych standardach Anthropic i najnowszych research z 2025 roku.

---

## 1. Oficjalne Narzędzia Testowania MCP

### 🔧 **MCP Inspector** - Główne Narzędzie Testowania

**MCP Inspector** to oficjalne narzędzie Anthropic do debugowania i testowania serwerów MCP.

**Użycie:**
```bash
# Testowanie serwera Node.js/TypeScript
npx @modelcontextprotocol/inspector node path/to/server/index.js args...

# Testowanie serwera Python
npx @modelcontextprotocol/inspector \
  uv \
  --directory path/to/server \
  run \
  package-name \
  args...
```

**Funkcjonalności:**
- ✅ Interfejs webowy do testowania w czasie rzeczywistym
- ✅ Testowanie tools, resources i prompts
- ✅ Analiza komunikacji JSON-RPC
- ✅ Historia wywołań i debugging logs

### 🛠️ **Chrome DevTools w Claude Desktop**

**Aktywacja:**
```bash
echo '{"allowDevTools": true}' > ~/Library/Application\ Support/Claude/developer_settings.json
```

**Zastosowanie:**
- Console debugging
- Network traffic analysis  
- Performance monitoring
- Error inspection

### 📊 **Structured Logging (RFC 5424)**

**Real-time monitoring:**
```bash
# Monitorowanie logów MCP
tail -n 20 -F ~/Library/Logs/Claude/mcp*.log
```

**8 poziomów logowania:**
- `debug` - szczegółowe informacje debugowania
- `info` - ogólne informacje operacyjne  
- `notice` - ważne ale normalne zdarzenia
- `warning` - ostrzeżenia
- `error` - błędy operacyjne
- `critical` - krytyczne problemy systemu
- `alert` - natychmiastowa akcja wymagana
- `emergency` - system nieużywalny

**Implementacja w kodzie:**
```python
# Python
server.request_context.session.send_log_message(
  level="info",
  data="Server started successfully",
)
```

```typescript
// TypeScript
server.sendLoggingMessage({
  level: "info",
  data: "Server started successfully"
});
```

---

## 2. Frameworki Ewaluacji i Benchmarki

### 📈 **MCPBench** - Oficjalny Framework Ewaluacji (2025)

**MCPBench** to open-source framework do kompleksowej ewaluacji serwerów MCP.

**Obsługiwane typy serwerów:**
- Web Search servers
- Database Query servers  
- GAIA (General AI Assistant) servers

**Kluczowe metryki:**
- **Task Completion Accuracy** - procent poprawnie wykonanych zadań
- **Latency** - czas odpowiedzi serwera
- **Token Consumption** - efektywność wykorzystania tokenów

### 🌍 **MCP-Universe Benchmark**

**Kompleksowy benchmark** dla LLM działających z real-world MCP servers.

**6 głównych domen testowych:**
1. **Location Navigation** - systemy nawigacyjne i lokalizacyjne
2. **Repository Management** - zarządzanie kodem i repozytoriami
3. **Financial Analysis** - analizy finansowe i obliczenia
4. **3D Design** - modelowanie i projektowanie 3D
5. **Browser Automation** - automatyzacja przeglądarek
6. **Web Searching** - wyszukiwarki internetowe

### 🎯 **Konkretne Wyniki Benchmarków 2025**

**Accuracy Rankings:**
- **Bing Web Search**: 64% accuracy ⭐
- **Brave Search**: ~50% accuracy
- **DuckDuckGo**: 10% accuracy ⚠️

**LLM Performance Scores:**
- **GPT-5**: 43.72%
- **Grok-4**: 33.33%  
- **Claude-4.0-Sonnet**: 29.44%

**Speed Benchmarks:**
- **Top performers**: <15 sekund
- **Średnia rynkowa**: 30-45 sekund
- **Slow performers**: >60 sekund

**Load Testing:**
- **Test concurrency**: 250 równoczesnych AI agents
- **Stabilność serwerów**: monitoring pod wysokim obciążeniem

---

## 3. Metodologia Testowania

### 🔄 **Workflow Testowania: Local → Remote**

**Faza 1: Local Development Testing**
```bash
# Szybkie iteracyjne testy
mcp dev server.py --debug --verbose

# Testowanie z MCP Inspector
npx @modelcontextprotocol/inspector server.py
```

**Faza 2: Network-based Remote Testing** 
```bash
# Symulacja rzeczywistego wdrożenia
mcp test --remote --endpoint https://api.example.com/mcp
mcp load-test --concurrent-agents 50
```

### ⚡ **Dwupoziomowy System Błędów**

**1. Protocol Errors (JSON-RPC)**
- Nieznane narzędzia
- Nieprawidłowe argumenty  
- Błędy serwera

**2. Tool Execution Errors**
```typescript
// Prawidłowe zgłaszanie błędów narzędzi
try {
  const result = performOperation();
  return {
    content: [{ type: "text", text: `Success: ${result}` }]
  };
} catch (error) {
  return {
    isError: true,  // Kluczowa flaga
    content: [{ type: "text", text: `Error: ${error.message}` }]
  };
}
```

### 📊 **Kluczowe Metryki Wydajności**

**Performance KPIs:**
- **Processor Utilization** - wykorzystanie CPU
- **I/O Throughput** - przepustowość wejścia/wyjścia
- **Memory Usage** - zużycie pamięci RAM  
- **Application Response Times** - czasy odpowiedzi

**Success Rate Calculation:**
```
Success Rate = (Successful Calls / Total Calls) × 100%
```

**Scalability Score:**
```
Scalability = (Performance under Load / Baseline Performance) × 100%
```

---

## 4. Bezpieczeństwo i Podatności

### ⚠️ **Krytyczne Zagrożenia 2025**

**Statystyki podatności:**
- **43% serwerów MCP** ma podatności command injection
- **30% serwerów** pozwala na nieograniczone pobieranie URL
- **22% serwerów** wyciekają pliki poza katalogami

### 🚨 **CVE-2025-6514 - Krytyczna Podatność**
- **CVSS Score**: 9.6 (Critical)
- **Dotknięte wersje**: mcp-remote 0.0.5 - 0.1.15
- **Wpływ**: Remote Code Execution (RCE)
- **Fix**: Aktualizacja do wersji ≥0.1.16

**Sprawdzenie wersji:**
```bash
npm list @anthropic/mcp-remote
npm update @anthropic/mcp-remote  # Aktualizacja
```

### 🔐 **Security Testing Checklist**

**1. Input Validation Testing**
```bash
# Testowanie injection attacks
mcp security-test --input-fuzzing server.py
mcp validate --malicious-payloads server.py
```

**2. Authentication & Authorization**
```bash
# Testowanie token management
mcp auth-test --token-rotation server.py  
mcp permissions-check --privilege-escalation server.py
```

**3. Sandboxing Verification** 
```bash
# Sprawdzenie izolacji
mcp sandbox-test --filesystem-access server.py
mcp network-isolation-check server.py
```

---

## 5. Best Practices i Optymalizacje

### 🚀 **Proven Performance Boosters**

**1. Verbose Logging** 
- **Efekt**: 40% redukcja MTTR (Mean Time To Resolution)
- **Implementacja**: Włącz szczegółowe logi podczas development

**2. Focused Tool Selection**
- **Efekt**: 30% wzrost user adoption  
- **Strategia**: Ogranicz narzędzia do niezbędnych funkcji

**3. Continuous Security Scanning**
- **Efekt**: 48% mniej vulnerabilities w produkcji
- **Tooling**: Zautomatyzowane skanowanie w CI/CD

### 📋 **Implementation Guidelines**

**Server-side Best Practices:**
- ✅ Sortowanie sugestii wg. relevance
- ✅ Implementacja fuzzy matching
- ✅ Rate limiting dla completion requests
- ✅ Walidacja wszystkich inputów

**Client-side Best Practices:**
- ✅ Debouncing szybkich requests
- ✅ Caching wyników completion
- ✅ Graceful handling missing results
- ✅ Progressive timeout strategies

### ⚙️ **Konfiguracja Environment Variables**

```json
{
  "myserver": {
    "command": "mcp-server-myapp",
    "env": {
      "MYAPP_API_KEY": "encrypted_key",
      "LOG_LEVEL": "debug",
      "RATE_LIMIT": "100/minute",
      "TIMEOUT": "30s"
    }
  }
}
```

---

## 6. Automatyzacja i CI/CD

### 🔄 **Continuous Testing Pipeline**

**GitHub Actions Example:**
```yaml
name: MCP Server Testing
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup MCP Testing
        run: |
          npm install -g @modelcontextprotocol/inspector
          pip install mcpbench
          
      - name: Run Unit Tests
        run: |
          mcp test --unit server.py
          
      - name: Run Integration Tests  
        run: |
          mcp test --integration --endpoint localhost:8080
          
      - name: Security Scanning
        run: |
          mcp security-scan server.py
          
      - name: Performance Benchmarks
        run: |
          mcpbench run --server server.py --iterations 100
```

### 📊 **Monitoring i Alerting**

**Prometheus Metrics:**
```yaml
# mcp_server_metrics.yml
mcp_request_duration_seconds:
  type: histogram
  help: "MCP request duration in seconds"
  
mcp_error_rate:
  type: gauge  
  help: "Error rate percentage"
  
mcp_concurrent_connections:
  type: gauge
  help: "Number of concurrent connections"
```

**Grafana Dashboard KPIs:**
- Request latency percentiles (p50, p90, p99)
- Error rate trends
- Token consumption per request
- Server resource utilization

---

## 7. Troubleshooting i Debugging

### 🔍 **Common Issues i Solutions**

**Problem: Server Connection Failures**
```bash
# Diagnosis
tail -f ~/Library/Logs/Claude/mcp*.log | grep ERROR

# Solution
mcp diagnose --connection server.py
mcp restart --force server.py
```

**Problem: Performance Degradation**
```bash
# Profiling
mcp profile --duration 60s server.py

# Memory analysis  
mcp memory-check --heap-dump server.py
```

**Problem: Tool Execution Errors**
```bash
# Error analysis
mcp error-trace --tool-name problematic_tool server.py

# Validation testing
mcp validate-tool --comprehensive problematic_tool server.py
```

### 📝 **Debug Checklist**

**Pre-deployment:**
- [ ] MCP Inspector testing passed
- [ ] Security scan completed  
- [ ] Load testing under expected traffic
- [ ] Error handling scenarios tested
- [ ] Logging configuration verified

**Production monitoring:**
- [ ] Real-time log monitoring active
- [ ] Performance metrics collecting
- [ ] Alert thresholds configured
- [ ] Backup/failover tested
- [ ] Security monitoring enabled

---

## Wnioski i Rekomendacje

### 🎯 **Kluczowe Zalecenia**

**1. Mandatory Testing Stack:**
- MCP Inspector dla development
- MCPBench dla benchmarking  
- Continuous security scanning
- Real-time performance monitoring

**2. Performance Targets 2025:**
- **Task Completion**: >50% accuracy minimum
- **Response Time**: <15 sekund dla top-tier
- **Error Rate**: <5% w normal conditions
- **Uptime**: >99.5% SLA

**3. Security Standards:**  
- Zero tolerance dla command injection
- Mandatory input validation
- Regular vulnerability assessments
- Encrypted token management

**4. Development Workflow:**
```
Local Testing → Security Scan → Performance Benchmark → Integration Test → Production Deploy
```

### 📈 **Przyszłość Testowania MCP**

**Trendy na 2025:**
- Automatyczny sandboxing na runtime level
- AI-powered test case generation
- Real-time performance optimization
- Industry-standard compliance frameworks

---

## Bibliografia i Źródła

### 📚 **Oficjalne Dokumentacje**
1. **Anthropic MCP Documentation** - https://modelcontextprotocol.io/introduction/
2. **MCP Inspector Guide** - https://modelcontextprotocol.io/introduction/docs/tools/inspector
3. **MCP SDK Documentation** - https://modelcontextprotocol.io/introduction/sdk/

### 🔬 **Research Papers & Benchmarks**
4. **MCPBench Framework** - https://github.com/modelscope/MCPBench
5. **MCP-Universe Benchmark** - https://arxiv.org/abs/2508.14704
6. **MCP Evaluation Report** - https://arxiv.org/html/2504.11094v1

### 🔐 **Security Research**
7. **Red Hat MCP Security Analysis** - https://www.redhat.com/en/blog/model-context-protocol-mcp-understanding-security-risks-and-controls
8. **JFrog CVE-2025-6514 Report** - https://jfrog.com/blog/2025-6514-critical-mcp-remote-rce-vulnerability/
9. **CyberArk MCP Threat Analysis** - https://www.cyberark.com/resources/threat-research-blog/is-your-ai-safe-threat-analysis-of-mcp-model-context-protocol

### 📊 **Performance Studies**  
10. **MCP Performance Benchmarks 2025** - https://research.aimultiple.com/browser-mcp/
11. **MCP Metrics Analysis** - https://markaicode.com/mcp-metrics-2025/
12. **BytePlus Performance Guide** - https://www.byteplus.com/en/topic/541519

---

*Dokument przygotowany: Wrzesień 2025*  
*Wersja: 1.0 - Kompletny przewodnik testowania i ewaluacji MCP*  
*Autor: Research na potrzeby konferencji MCP*
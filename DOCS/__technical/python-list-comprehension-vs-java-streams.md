# Python list comprehension vs. Java Streams — skrót

Fragment z `ToolManager.execute_tool_requests` (`core/tools.py`):
```python
tool_requests = [
    block for block in message.content if block.type == "tool_use"
]
```
Co robi:
- iteruje po `message.content`
- filtruje elementy o `block.type == "tool_use"`
- tworzy nową listę (nie modyfikuje oryginału)

Równoważnik w “zwykłym” Pythonie:
```python
tool_requests = []
for block in message.content:
    if block.type == "tool_use":
        tool_requests.append(block)
```

Równoważnik w Javie (Streams):
```java
List<Block> toolRequests = message.getContent().stream()
    .filter(b -> "tool_use".equals(b.getType()))
    .collect(Collectors.toList());
```

Uwagi:
- kolejność zachowana
- składnia zwięzła; nadaje się świetnie do map/filter/reduce na listach w Pythonie.

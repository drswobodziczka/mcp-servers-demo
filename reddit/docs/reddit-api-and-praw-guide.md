# Reddit API & PRAW SDK Guide

## Overview

**PRAW** = **P**ython **R**eddit **A**PI **W**rapper — oficjalny Python SDK dla Reddit API.

## Reddit API - Pricing & Limits

| Tier | Limit | Warunki |
|------|-------|---------|
| **Free** | **100 QPM** (queries/min) | Non-commercial, OAuth required |
| **Paid** | Negocjowane | Commercial, bulk data, monetized apps |

**Dla personal/research use case**: darmowe — 100 req/min wystarczy.

**Wymagane**: utworzenie aplikacji na https://www.reddit.com/prefs/apps → otrzymasz `client_id` + `client_secret`.

## PRAW vs REST API

| Aspekt | PRAW SDK | REST API |
|--------|----------|----------|
| **Użycie** | `reddit.subreddit("all").search("X")` | Ręczne requesty HTTP, parsowanie JSON |
| **Auth** | Automatyczne zarządzanie tokenami | Ręczne OAuth flow |
| **Rate limiting** | Automatyczne (wbudowane) | Ręczne śledzenie |
| **Paginacja** | Automatyczna (iteratory) | Ręczne `after`/`before` |

**Wniosek**: PRAW = mniej kodu, mniej błędów, szybsza implementacja.

## Key PRAW Functions

### Wyszukiwanie postów

```python
# W całym Reddit
reddit.subreddit("all").search("AI tools", sort="top", time_filter="month", limit=25)

# W konkretnym subreddit
reddit.subreddit("programming").search("python", limit=10)
```

**Sort options**: `relevance`, `hot`, `top`, `new`, `comments`
**Time filters**: `hour`, `day`, `week`, `month`, `year`, `all`

### Atrybuty posta

```python
submission.title          # Tytuł posta
submission.score          # Upvotes
submission.num_comments    # Liczba komentarzy
submission.selftext        # Treść posta (jeśli self post)
submission.url            # URL posta
submission.id              # ID posta
submission.author          # Autor
submission.created_utc     # Data utworzenia
```

### Komentarze

```python
# Top-level comments (szybkie)
top_level_comments = list(submission.comments)

# Wszystkie komentarze (płaska lista)
submission.comments.replace_more(limit=0)  # Nie rozwijaj "MoreComments"
all_comments = submission.comments.list()

# Z sortowaniem
submission.comment_sort = "new"  # "best", "top", "new", "controversial"
comments = submission.comments.list()
```

**Problem z "MoreComments"**: Duże wątki mają placeholdery — każdy wymaga dodatkowego API call.

## Rate Limits & Performance

| Scenariusz | Komentarze | API calls | Czas |
|------------|------------|-----------|------|
| **Top-level only** | ~20-50 | 1 | <1s |
| **Pełny wątek (małe)** | ~100-500 | 1-3 | 1-3s |
| **Pełny wątek (duże)** | 1000+ | 5-20+ | 5-30s |

**PRAW automatycznie zarządza rate limiting** — czeka gdy osiągnięto limit.

## Authentication Setup

```python
import praw

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET", 
    user_agent="MyRedditApp/1.0",
    read_only=True  # Tylko odczyt
)
```

**Read-only mode**: Wystarczy do czytania postów i komentarzy,不需要 username/password.

## Best Practices

1. **Używaj `read_only=True`** — nie potrzebujesz pełnego auth do czytania
2. **Limituj wyniki** — `limit=25` dla postów, `limit=50` dla komentarzy
3. **Unikaj `replace_more(limit=None)`** — może wygenerować setki requestów
4. **Sortowanie** — używaj `sort="relevance"` dla wyszukiwania, `sort="top"` dla popularnych

## Example: Complete Workflow

```python
import praw

reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    user_agent="RedditAnalyzer/1.0",
    read_only=True
)

# 1. Szukaj postów
posts = []
for submission in reddit.subreddit("all").search("AI tools", sort="top", time_filter="month", limit=10):
    posts.append({
        "id": submission.id,
        "title": submission.title,
        "score": submission.score,
        "num_comments": submission.num_comments,
        "url": submission.url
    })

# 2. Czytaj konkretny post
submission = reddit.submission("abc123")
submission.comments.replace_more(limit=0)  # Szybkie, tylko top-level
comments = []
for comment in submission.comments.list()[:50]:  # Max 50 komentarzy
    comments.append({
        "body": comment.body,
        "score": comment.score,
        "author": str(comment.author) if comment.author else "[deleted]"
    })
```

## MCP Tools Architecture

Dla workflow "co Reddit myśli o X":

| Narzędzie | Parametry | Zwraca |
|-----------|-----------|--------|
| `search_reddit` | `query`, `subreddit?`, `sort?`, `time_filter?`, `limit?` | Lista postów z metadanymi |
| `read_reddit_thread` | `post_id`, `comment_limit?`, `expand_replies?` | Post + komentarze |

**KISS principle**: 2 narzędzia wystarczą do pełnego workflow.

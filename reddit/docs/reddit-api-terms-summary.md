# Reddit API Terms - Podsumowanie Głównych Zasad

## Developer Terms (Zaktualizowano: 24 września 2024)

### Główne Zasady
- **Platforma Deweloperska**: Reddit oferuje platformę deweloperską ("Devvit"), API, oraz usługę osadzania treści ("Reddit Embeds")
- **Dostęp Warunkowy**: Wszyscy deweloperzy, moderatorzy i badacze muszą uzyskać zatwierdzenie przed dostępem do API
- **Jeden token OAuth**: Limit jednego tokena OAuth na konto użytkownika

### Prawa i Uprawnienia
- **Korzystanie z Devvit**: Deweloperzy mogą kontynuować tworzenie aplikacji przez platformę Devvit
- **Dostęp dla badaczy**: Badacze mogą uzyskać dostęp poprzez program r/reddit4researchers
- **Moderatorzy**: Specjalny kanał wsparcia dla moderatorów z potrzebami API

## Data API Terms (Zaktualizowano: 16 września 2024)

### Ograniczenia Użycia
- **Koniec samodzielnego dostępu**: Zakończenie samodzielnego dostępu do publicznego API Reddit
- **Wymagane zatwierdzenie**: Wszyscy nowi użytkownicy muszą przejść proces zatwierdzenia
- **Rate limiting**: 100 zapytań na minutę dla OAuth, 10 zapytań na minutę bez OAuth
- **Tylko autoryzowany dostęp**: Dostęp tylko za pomocą dostarczonych informacji autoryzacyjnych

### Zakazy i Ograniczenia
- **Brak maskowania**: Zakaz maskowania user agenta lub tokenu OAuth
- **Brak nadużyć**: Ścisła polityka przeciwdziałania nadużyciom i spamowaniu
- **Tylko zatwierdzone integracje**: Tylko zatwierdzone integracje mogą kontynuować działanie

## Płatności i Model Biznesowy

### Historia Zmian (2023-2024)
- **Ceny API od 2023**: $0.24 za każde 1000 wywołań API (od lipca 2023)
- **Koniec darmowego API**: Zakończenie darmowego dostępu, który istniał od 2008 roku
- **Wymagania komercyjne**: Reddit nie będzie już subsydiować podmiotów komercyjnych wymagających dużego skalowania danych

### Wyjątki i Zwolnienia
- **Aplikacje dostępnościowe**: Zwolnienia dla aplikacji dostępnościowych (np. RedReader, Dystopia)
- **Narzędzia moderacyjne**: Zwolnienia dla oficjalnych narzędzi moderacyjnych
- **Projekty non-commercial**: Specjalne traktowanie projektów niekomercyjnych

## Responsible Builder Policy

### Nowe Wymagania (2024)
- **Proces zatwierdzania**: Wszyscy nowi użytkownicy API muszą przejść proces zatwierdzenia
- **Ramy odpowiedzialnego użytkowania**: Jasno określone zasady dostępu i użytkowania danych Reddit
- **Ochrona platformy**: Zapobieganie nadużyciom i spamowaniu

### Kategorie Użytkowników
1. **Deweloperzy**: Dostęp przez Devvit lub wniosek enterprise
2. **Badacze**: Specjalny program r/reddit4researchers
3. **Moderatorzy**: Dedykowany kanał wsparcia

## Wpływ na Ekosystem

### Zmiany dla Aplikacji Trzecich
- **Zamknięcie aplikacji**: Wiele popularnych aplikacji (Apollo, RIF, Sync) zamknęło się w 2023 roku
- **Koszty operacyjne**: Szacowane koszty do $20 milionów rocznie dla dużych aplikacji
- **Protesty społeczności**: Ponad 8000 subredditów ogłosiło blackout w proteście

### Alternatywy
- **Lemmy**: Zdecentralizowana, open-source platforma
- **Squabbles**: Hybrydowa platforma łącząca Reddit i Twitter
- **Tildes**: Platforma skoncentrowana na jakości treści tekstowych

## Podsumowanie

Reddit wprowadził rygorystyczne zasady dostępu do API w celu:
1. **Zrównoważenia biznesowego**: Uczynienie Reddit samowystarczalnym biznesem
2. **Ochrony danych**: Zapobieganie nadużyciom i komercyjnym eksploatacji
3. **Kontroli jakości**: Zapewnienie odpowiedzialnego użytkowania platformy

Nowy model priorytetowo traktuje aplikacje dostępnościowe, narzędzia moderacyjne i projekty badawcze, jednocześnie ograniczając komercyjne wykorzystanie danych na dużą skalę.

# LLM + Tools + Context — High-Level Overview

## Components
- Model service: odpowiedzialny za komunikację z LLM.
- Chat loop: utrzymuje historię rozmowy, przekazuje ją do modelu i obsługuje iteracje.
- Resource layer: dokłada treści dokumentów/zasobów do zapytania użytkownika.
- Tool manager: zbiera narzędzia z wielu MCP serwerów i wykonuje je na żądanie modelu.
- CLI UI: konsolowy interfejs, który przyjmuje wejście od użytkownika i wyświetla odpowiedzi.
- MCP server/client: serwery wystawiają narzędzia/zasoby, klienci łączą się z nimi i wołają RPC.

## Minimalna mapa przepływu
- Wejście użytkownika (CLI) → Chat buduje wiadomość użytkownika.
- Jeśli w treści są wzmianki o zasobach (np. @raport.pdf), Resource layer dociąga i dokleja ich treść do kontekstu użytkownika.
- Chat woła model z aktualną historią i listą dostępnych narzędzi (zebranych z MCP klientów).
- Model decyduje: 
  - jeśli potrzebuje narzędzia → wskazuje narzędzie i parametry; 
  - Tool manager uruchamia właściwy MCP klient/serwer i zwraca wynik jako kontekst narzędziowy;
  - wynik narzędzia jest dołączany do rozmowy i pętla kontynuuje.
- Jeśli model nie potrzebuje kolejnych narzędzi → zwraca końcową odpowiedź tekstową.

## Kiedy model „dostaje” narzędzia
- Przy każdym wywołaniu modelu przekazywana jest aktualna lista narzędzi (z wielu MCP serwerów). Model sam wybiera, których użyć.

## Kiedy dokładamy zasoby do kontekstu
- Przed wywołaniem modelu: jeśli użytkownik wspomniał zasoby, ich treść trafia do kontekstu pytania.
- Po wywołaniu narzędzia: wynik działania narzędzia jest dołączany jako kolejny kontekst i model wykorzystuje go w następnej iteracji.

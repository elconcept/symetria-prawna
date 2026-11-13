# Decyzja o liczbie skilli — 1, 2 czy 3?

Wersja 0.5.2 miała **jeden** skill, mimo starszej dyskusji o dwóch. Po rozszerzeniu zakresu przeprowadzono następującą ocenę:

| Konfiguracja | Zalety | Wady | Decyzja |
| --- | --- | --- | --- |
| 1 skill + referencje | Jeden jednoznaczny punkt wejścia do każdej pracy prawnej; niski koszt metadanych; brak konkurencji wyzwalaczy | Ryzyko przeciążenia głównej instrukcji | **Wybrana**: SKILL.md ~300 słów; reszta selektywnie |
| 2 skille: ogólny i dowodowy | Bardziej szczegółowy audyt sytuacyjny | Ryzyko, że drugi skill nie aktywuje się mimo potrzeby; dodatkowe metadane | Odrzucona, audyt przeniesiony do referencji |
| 3 skille: ogólny, dowodowy, TK/NC | Wysoka specjalizacja | Trzy punkty aktywacji, dublowanie procedur, większy narzut | Odrzucona; TK/NC jest referencją, nie uniwersalną zasadą |

Claude Code ma dodatkowy **agent** audytora, a nie skill. Agent zapewnia osobny kontekst dla kontroli wymagającej bardziej adwersarialnej perspektywy. Nie jest uruchamiany przy każdym pytaniu i nie zmienia trybu ChatGPT web.

Plugin stosuje porównawcze standardy dowodowe, weryfikację aktualności prawa i ocenę kumulacyjną. Nie przyjmuje z góry prawdziwości lub fałszywości wszystkich twierdzeń instytucji.

## Hooki (0.7.0)
Sam skill okazał się niewystarczający: model nie zawsze go wywoływał, a nawet po wywołaniu wracał do asymetrii (wysoki próg wobec dowodów strony, notatki funkcjonariuszy i dokumentacja lekarska jako fakty). Rdzeń zasad przeniesiono więc do hooków uruchamianych przez host. Hooki są **osobnym pluginem** `symetria-prawna-hooki`, bo katalog `symetria-dowodowa-tknc` instaluje także ChatGPT web, gdzie lokalne wykonawcy psuły instalację. Hooki leżą w domyślnej ścieżce `hooks/hooks.json`, którą odczytują Claude Code i Codex; manifesty nie mają pola `hooks` (walidator Codex/ChatGPT je odrzuca). Heurystyka jest wspólna z serwerem MCP (`core.py`, kopiowana skryptem `sync_hooks_core.py`).

| Warstwa | Wymusza | Ograniczenie |
| --- | --- | --- |
| Skill + referencje | pełną metodę (O→P→S, A–K, prawo polskie, kanon) | zależy od wywołania przez model |
| Hooki | zasady w kontekście przy każdej pracy prawnej, ostrzeżenie przy dokumencie organu, kontrolę sformułowań w pismach i odpowiedzi | heurystyka słownikowa, nie ocena merytoryczna |
| Agent `audytor-prawny` | niezależną recenzję w osobnym kontekście | na żądanie |

**Regresja ochronna:** brak `mcp.json`, `hooks/` i `requires_local_executor` w pluginie instalowanym do ChatGPT web. Techniczny slug ChatGPT pozostaje niezmieniony, a human-readable displayName to `Symetria Prawna`.

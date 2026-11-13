# Decyzja o liczbie skilli — 1, 2 czy 3?

Wersja 0.5.2 miała **jeden** skill, mimo starszej dyskusji o dwóch. Po rozszerzeniu zakresu przeprowadzono następującą ocenę:

| Konfiguracja | Zalety | Wady | Decyzja |
| --- | --- | --- | --- |
| 1 skill + referencje | Jeden jednoznaczny punkt wejścia do każdej pracy prawnej; niski koszt metadanych; brak konkurencji wyzwalaczy | Ryzyko przeciążenia głównej instrukcji | **Wybrana**: SKILL.md ~300 słów; reszta selektywnie |
| 2 skille: ogólny i dowodowy | Bardziej szczegółowy audyt sytuacyjny | Ryzyko, że drugi skill nie aktywuje się mimo potrzeby; dodatkowe metadane | Odrzucona, audyt przeniesiony do referencji |
| 3 skille: ogólny, dowodowy, TK/NC | Wysoka specjalizacja | Trzy punkty aktywacji, dublowanie procedur, większy narzut | Odrzucona; TK/NC jest referencją, nie uniwersalną zasadą |

Claude Code ma dodatkowy **agent** audytora, a nie skill. Agent zapewnia osobny kontekst dla kontroli wymagającej bardziej adwersarialnej perspektywy. Nie jest uruchamiany przy każdym pytaniu i nie zmienia trybu ChatGPT web.

Plugin stosuje porównawcze standardy dowodowe, weryfikację aktualności prawa i ocenę kumulacyjną. Nie przyjmuje z góry prawdziwości lub fałszywości wszystkich twierdzeń instytucji.

**Regresja ochronna:** brak `mcp.json` i `requires_local_executor` w pluginie instalowanym do ChatGPT web. Techniczny slug ChatGPT pozostaje niezmieniony, a human-readable displayName to `Symetria Prawna`.

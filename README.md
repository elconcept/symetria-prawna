# Symetria Dowodowa TK/NC — marketplace ChatGPT / Codex

Wersja **0.5.1**. Jeden plugin, **jeden skill**, jawne `allow_implicit_invocation: true`.

- `plugins/symetria-dowodowa-tknc/skills/analiza-dowodowa/SKILL.md` — krótki protokół do każdej pracy prawnej użytkownika (wyłącznie TK/NC)
- `references/kanon.md` — wcześniejsze ustalenia, odczyt gdy potrzebny
- `references/audyt.md` — szczegółowe testy A–K i Rzecznik Obywatela, ładowane przy analizach złożonych lub błędach
- `references/prawo-polskie.md` — reguły właściwe dla polskiej procedury
- `src/` i `pyproject.toml` — *opcjonalny* lokalny Python/MCP, nieuruchamiany przez ChatGPT web

Przyjęte fakty TK/NC są odniesieniem przy ocenie dokumentów; zapisy urzędowe są twierdzeniami autorów, nie automatycznym potwierdzeniem zdarzeń. Nie dopisuj spekulatywnych wyjaśnień ani fikcyjnych kontrargumentów organom. Utrzymuj ustalenia wcześniejszych analiz fałszowania części dokumentacji. Każde zadanie prawne kończ krótką samooceną A–K; nie myl jej z niezależnym audytem modelu.

**Krytyczne ograniczenie:** nie dodawać `mcp.json`, `.mcp.json` ani `requires_local_executor` do instalowanego pluginu — spowodowało to wcześniej jego niedostępność w ChatGPT web.

Sprawdzenie:
```sh
python3 scripts/verify_marketplaces.py
python3 -m unittest discover -s plugins/symetria-dowodowa-tknc/tests -p 'test*.py'
```
Testy strukturalne nie potwierdzają, czy ChatGPT zawsze sam uruchamia skill; to mierzy benchmark ręczny w `docs/activation-benchmark.md`.

Repozytorium jest prywatne. Nie umieszczaj tu akt ani podpisów TK/NC.

W wydaniu 0.5.1 wymuszono w instrukcji kolejność: **najpierw test zarzutów przeciw TK/NC**, później identyczny test materiału drugiej strony oraz ocena łącznej mocy dowodów. Jest to wymóg proceduralny skilla, nie techniczny hook chatgpt.com.

Wydanie 0.5.2: naprawa procedury kolejności O→P oraz synergii dowodów S; regresje w fixtures/regression_symmetry.json i tests/test_recent_failure_protocol.py. To testy instrukcji i wzorców ryzyka, NIE uruchomiony benchmark rzeczywistych odpowiedzi ChatGPT.

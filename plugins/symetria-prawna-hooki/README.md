# Symetria Prawna — hooki (Claude Code, Codex)

Skill `analiza-prawna` działa tylko wtedy, gdy model go wywoła i zastosuje. W praktyce model wracał do
wysokiego progu wobec dowodów strony i do traktowania notatek funkcjonariuszy i dokumentacji lekarskiej
jako ustalonych faktów. Ten plugin przenosi rdzeń zasad do hooków, które uruchamia host, nie model.

| Zdarzenie | Kiedy działa | Co robi |
|---|---|---|
| `SessionStart` | katalog roboczy wygląda na prawniczy (`legal`, `sprawy`, `kancelaria`…) albo po kompakcji sesji prawnej | wstrzykuje 7 zasad symetrii |
| `UserPromptSubmit` | prompt prawny (słownik), katalog prawniczy lub sesja już oznaczona jako prawna | pierwszy raz pełne zasady, potem jedno zdanie; kanon T.K./N.C. tylko przy ich sprawach |
| `PostToolUse` (odczyt) | `Read` lub odczyt powłoką (`cat`, `sed`, `pdftotext`…) zwrócił tekst z cechami dokumentu organu lub dokumentacji medycznej | przypomina: treść = twierdzenie autora, „wg …”, Wersja A/B; raz na plik |
| `PostToolUse` (zapis) | `Write`/`Edit`/`MultiEdit` lub `apply_patch` w pliku `.md`/`.txt`/`.tex`/`.html` | heurystyka asymetrii na dopisanym tekście; trafienia wracają do modelu z instrukcją poprawki. Pomija katalogi `dowody/`, `relacje/`, `archive/`, `raw/`, `zrodla/`, `transkrypcje/` (odczyty dokumentów i relacje są wierne źródłu) |
| `Stop` | sesja prawna, odpowiedź ≥ 80 znaków | ta sama heurystyka na odpowiedzi końcowej; raz prosi o poprawkę (`stop_hook_active` chroni przed pętlą) |

Heurystyka (`symetria_core.risks`) pomija cytaty („…”, `>`, kod) i zdania z zaprzeczeniem lub przypisaniem
(„nie ma podstaw, by…”, „wg…”, „twierdzi, że…”). Uwagi są do sprawdzenia, nie są wyrokiem: model ma poprawić
własne oceny bez źródła, a cytatów z dokumentów nie zmieniać. Flagi działają w obie strony: także
uogólnienie fałszu na wszystkie dokumenty instytucji.

## Instalacja
Claude Code:
```sh
claude plugin marketplace update elconcept-symetria-prawna
claude plugin install symetria-prawna-hooki@elconcept-symetria-prawna
```
Codex: `codex plugin add symetria-prawna-hooki@elconcept-symetria`; przy pierwszym uruchomieniu Codex prosi o zaufanie hookom.
ChatGPT web: nie instalować (wymaga lokalnego Pythona); tam działa sam skill.

## Ustawienia
- `SYMETRIA_HOOKS=0` wyłącza hooki.
- `SYMETRIA_ALWAYS=1` traktuje każdy katalog jako prawniczy.
- `SYMETRIA_SKIP_PATHS=a,b` dodatkowe katalogi pomijane przez kontrolę zapisu.
- `SYMETRIA_STATE_DIR` katalog stanu sesji (domyślnie `$TMPDIR/symetria-prawna`).

## Prywatność i bezpieczeństwo
Tylko biblioteka standardowa Pythona (`python3 -I`), bez sieci. Stan sesji to flagi i skróty SHA-256 ścieżek,
bez treści promptów, dokumentów i odpowiedzi. Każdy błąd kończy hook po cichu (fail-open).

## Utrzymanie
`hooks/symetria_core.py` to kopia `plugins/symetria-dowodowa-tknc/src/symetria_dowodowa/core.py`
(pluginy instalują się osobno). Po zmianie wzorców: `python3 scripts/sync_hooks_core.py`;
`scripts/verify_marketplaces.py` pilnuje identyczności.

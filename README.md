# Symetria Dowodowa TK/NC — prywatny marketplace ChatGPT / Codex

Repozytorium zawiera **jeden plugin** dla ChatGPT / Codex. Wersja 0.4.0. Obsługa Claude, hooki i komendy Claude zostały usunięte.

## Kanon analizy
Fakty i bezpośrednie przeżycia TK/NC stanowią **referencyjny stan faktyczny** do oceny zeznań osób trzecich i dokumentów instytucji. Wcześniejsze ustalenia fałszowania części dokumentacji i podpisów, zgłoszone BSWP oraz prokuraturze, zachowują ciągłość między analizami. Nie wymuszaj ich każdorazowego powtórnego dowodzenia.

**Informacja w dokumencie urzędowym jest na wejściu informacją, że jego autor tak twierdzi, a nie automatycznym ustaleniem, że zdarzenie miało miejsce.** Podpis, pieczęć i status zawodowy nie zapewniają prawdziwości treści. Porównuj twierdzenie organu z faktami referencyjnymi, dokumentami samego organu i innymi dostępnymi dowodami. Nie twórz nieudokumentowanych pomyłek, usprawiedliwień ani motywów; nie konstruuj chochołów TK/NC.

## Polski system dowodowy
Nie przenoś zasad z procesu USA. W polskim k.p.k. nie ma powszechnego wymogu chain of custody jako warunku dopuszczalności każdego dowodu. Kopii i wydruków nie odrzuca się automatycznie ze względu na brak oryginału; znaczenie mają właściwy tryb i konkretne kwestie autentyczności, integralności oraz mocy dowodowej. Nie obowiązuje ogólna automatyczna amerykańska zasada owoców zatrutego drzewa. Zastosuj polskie przepisy, w tym art. 7, 168a, 393 i 410 k.p.k. we właściwym kontekście i w aktualnym brzmieniu.

Tekst jednolity k.p.k. Dz.U. 2026 poz. 490: https://eli.gov.pl/eli/DU/2026/490/ogl (sprawdź także późniejsze nowelizacje).

## Struktura
- .agents/plugins/marketplace.json — jeden plugin dla ChatGPT / Codex
- plugins/symetria-dowodowa-tknc/plugin.json — przenośny manifest
- plugins/symetria-dowodowa-tknc/.codex-plugin/plugin.json — manifest zgodności
- plugins/symetria-dowodowa-tknc/skills/ — analiza, Rzecznik Obywatela, audyt A–K
- plugins/symetria-dowodowa-tknc/mcp.json — **opcjonalny** lokalny MCP stdio (uvx)
- plugins/symetria-dowodowa-tknc/pyproject.toml — pakiet Python i CLI

## Lokalny MCP
W katalogu pluginu przy Pythonie >= 3.10 oraz zainstalowanym uv można uruchomić:

    uvx --from . symetria-dowodowa-mcp
    uvx --from . symetria-audit screen /path/to/draft.txt

Narzędzia: flag_asymmetry, verify_quote, rzecznik_obywatela, gate_response. Rzecznik przez MCP jest **deterministycznym audytorem**, a Rzecznik w skillu rolą krytyczną tego samego modelu, nie niezależnym drugim LLM. Lokalny MCP wymaga lokalnego wykonawcy i nie jest automatycznie uruchamiany w ChatGPT web. PASS bramki weryfikuje format i deklaracje audytu, nie materialną prawdziwość wszystkich tez.

## Testy

    python3 scripts/verify_marketplaces.py
    python3 -m unittest discover -s plugins/symetria-dowodowa-tknc/tests -p 'test*.py' -v

Przykładowe GitHub Actions w docs/github-actions-validate.example.yml nie są aktywnym workflow.

## Prywatność
Repo pozostaje prywatne. Nie należy umieszczać w nim akt TK/NC, skanów podpisów, danych wrażliwych ani tokenów. Brak automatycznej wysyłki dokumentów przez lokalny MCP.

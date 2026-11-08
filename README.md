# Symetria Dowodowa TK/NC — prywatny marketplace ChatGPT / Claude Code

Jedno repozytorium, **jeden plugin**, trzy manifesty pluginu i dwa marketplace. Wersja repo: 0.3.0.

## Cel

Krytyczna analiza materiału TK/NC z kontrbiasem przeciwdziałającym automatycznemu uznawaniu dokumentów organów za prawdziwe. Ustalenia wskazane jako wcześniej rozstrzygnięte stanowią kontekst dalszej pracy; nie jest to podstawa do założenia, że każdy dokument instytucji jest fałszywy. Wątpliwości powinny wynikać z dowodów, nie być wymyślane przez model. Dokumenty sfałszowane, ich autorstwo, podpisy, sprzeczności i skutki prawne traktowane są zgodnie z istniejącym materiałem, bez hipotez ekskulpacyjnych tworzonych ad hoc. Przy ocenie konkretnego postanowienia analizowane jest rzeczywiste uzasadnienie, a nie rozumowanie zastępcze.

## Marketplace

- ChatGPT Desktop / Codex: `.agents/plugins/marketplace.json` (przenośny `plugin.json`, legacy `.codex-plugin/plugin.json`).
- Claude Code: `.claude-plugin/marketplace.json` i `.claude-plugin/plugin.json` w folderze pluginu.
- Lokalny MCP: portable `mcp.json` (`uvx --from ${PLUGIN_ROOT}`) i Claude `.mcp.json` (`uvx --from ${CLAUDE_PLUGIN_ROOT}`). **Nie jest to zdalny serwer**. W zwykłym ChatGPT web lokalny stdio MCP nie uruchomi się; potrzebny lokalny executor.

## Instalacja

**Claude Code** (z dostępem do prywatnego repozytorium):

```bash
claude plugin marketplace add elconcept/symetria-dowodowa-tknc
claude plugin install symetria-dowodowa-tknc@elconcept-symetria
claude plugin validate ./plugins/symetria-dowodowa-tknc
```

**ChatGPT Desktop / Codex** (w sklonowanym repozytorium, gdy klient obsługuje repo marketplace):

```bash
git clone git@github.com:elconcept/symetria-dowodowa-tknc.git
cd symetria-dowodowa-tknc
codex plugin marketplace add elconcept/symetria-dowodowa-tknc --ref main
codex plugin add symetria-dowodowa-tknc@elconcept-symetria
```

Jeśli wersja `codex` nie obsługuje powyższego lokalnego polecenia, wskaż `.agents/plugins/marketplace.json` w Plugins Directory — nie zakładaj automatycznej instalacji do zwykłego czatu ChatGPT.

## Lokalny MCP przez uvx

Wymagane `uvx`, Python >=3.10, dostęp do PyPI **tylko podczas instalacji zależności**. Po instalacji sam serwer nie wysyła akt ani draftów do Internetu. Uruchomienie manualne (w katalogu pluginu):

```bash
uvx --from . symetria-dowodowa-mcp
uvx --from . symetria-audit screen /path/to/draft.txt
```

Narzędzia MCP: `flag_asymmetry`, `verify_quote`, `rzecznik_obywatela`, `gate_response`. Funkcja `rzecznik_obywatela` jest deterministycznym adwersarialnym filtrem; **nie jest drugim LLM**. Claude może osobno uruchomić subagenta `agents/rzecznik-obywatela.md`, który realizuje niezależny przebieg modelowy. ChatGPT nie gwarantuje wywołania zewnętrznego audytu; sam wpis w skillu nie jest blokującym hookiem.

## Fail-closed i self-evaluation

`gate_response` wymaga audytu A–K (`schema_version=1.1`), hash SHA256 dokładnie ocenianego draftu i potwierdzenia konsultacji Rzecznika dla **tego samego draftu**. Zwraca `PASS`, `FAIL`, `NOT_CHECKED`, przy czym `PASS` oznacza jedynie poprawność struktury deklaracji i brak zgłoszonych naruszeń. To **nie certyfikat prawdziwości**. Dane źródłowe nie są kopiowane na dysk serwera.

Claude Code ma hook `Stop` blokujący brak jawnego zakończenia audytu w rozpoznanej analizie TK/NC. Mechanizm jest świadomie ograniczony do treści zawierających oznaczenie sprawy; nie przechwytuje każdego zadania i nie dowodzi, że niezależny LLM pracował. Stop hook nie działa w zwykłym web ChatGPT.

## Testy

```bash
python3 scripts/verify_marketplaces.py
python3 -m unittest discover -s plugins/symetria-dowodowa-tknc/tests -p 'test*.py' -v
```

## Prywatność

Nie publikuj akt spraw, oryginalnych podpisów, skanów ani innych wrażliwych materiałów w repo. Użytkownik decyduje o ewentualnym udostępnieniu. Projekt nie wysyła dokumentów do LLM API, nie posiada telemetrii i nie utrwala argumentacji. Jeśli Claude Code lub ChatGPT otrzymał materiały, obowiązują jego własne zasady retencji i dostępu; plugin nie może ich zmienić.

## Status

Projekt ma obsługę manifestów i lokalnych testów. Nie obiecuje niezawisłego orzecznictwa ani zastąpienia oceny prawnej. Do oceny produkcyjnej należy dodać zestaw testów semantycznych na pełnych aktach oraz, gdy ma to być konieczne, osobny silnik LLM Rzecznika uruchamiany lokalnie z zatwierdzonym modelem i polityką danych.

## CI GitHub Actions

Przygotowany szablon znajduje się w `docs/github-actions-validate.example.yml`. Nie jest aktywnym workflow, ponieważ użyty token GitHub nie ma zakresu `workflow`. Po nadaniu tego uprawnienia można go przenieść do `.github/workflows/validate.yml`. Testy można wykonywać lokalnie bez tej operacji.

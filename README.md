# Symetria Prawna

Prywatny plugin **Symetria Prawna** dla ChatGPT/Codex oraz Claude Code, z osobnym pluginem hooków **symetria-prawna-hooki** dla Claude Code i Codex CLI. Zakres: **wszystkie analizy i sprawy prawne**, nie tylko TK/NC.

## Architektura
- Jeden automatycznie wybierany skill: `skills/analiza-prawna/SKILL.md` (instrukcje krótkie, progressive disclosure).
- `references/audyt-dowodowy.md` — kontrola A–K, kolejność badania O→P i ocena kumulacyjna S, odczyt przy złożonej analizie.
- `references/prawo-polskie.md` — polskie zasady dowodowe, gdy dotyczy.
- `references/kanon-tk-nc.md` — dotychczasowe ustalenia TK/NC, **wyłącznie w ich sprawach**.
- Claude Code ma dodatkowo `agents/audytor-prawny.md` — opcjonalnego recenzenta w osobnym kontekście; nie jest drugim skillem.
- `plugins/symetria-prawna-hooki/` — hooki `SessionStart`, `UserPromptSubmit`, `PostToolUse`, `Stop`, które wymuszają rdzeń zasad niezależnie od tego, czy model wywoła skill: przypomnienie przy pracy prawnej, ostrzeżenie po wczytaniu dokumentu organu lub dokumentacji medycznej, heurystyka asymetrii w zapisanych pismach i w odpowiedzi końcowej. Szczegóły: [README hooków](plugins/symetria-prawna-hooki/README.md).
- Plugin ze skillem pozostaje bez lokalnego wykonawcy (bez MCP i hooków), bo ten sam katalog instaluje ChatGPT web. Serwer MCP w `src/` nie jest podpinany automatycznie.

## ChatGPT / Codex
Manifest: `plugins/symetria-dowodowa-tknc/plugin.json`. Repo marketplace: `.agents/plugins/marketplace.json`. Nowa **nazwa wyświetlana** to `Symetria Prawna`.

Wewnętrzny identyfikator `symetria-dowodowa-tknc` oraz folder pozostają celowo bez zmian, żeby nie przerywać istniejącej prywatnej instalacji i odwołań `@plugin`. Jest to historyczny identyfikator techniczny, a **nie ograniczenie zakresu skilla**. W ChatGPT zachowujemy `skills-only`, bez `mcp.json` i `requires_local_executor`, ponieważ lokalne stdio powodowało wcześniej niedostępność.

## Claude Code
Manifest: `plugins/symetria-dowodowa-tknc/.claude-plugin/plugin.json`. Marketplace: `.claude-plugin/marketplace.json`.

```sh
claude plugin marketplace add elconcept/symetria-prawna
claude plugin install symetria-prawna@elconcept-symetria-prawna
claude plugin install symetria-prawna-hooki@elconcept-symetria-prawna
claude plugin list
claude plugin details symetria-prawna
```

Skill można wywołać jawnie jako `/symetria-prawna:analiza-prawna`. Agent `audytor-prawny` jest opcjonalnym recenzentem adwersarialnym i wychodzi od sceptycyzmu wobec dokumentu organu. Obowiązkową warstwę stanowią hooki z `symetria-prawna-hooki`.

## Codex CLI
`codex plugin marketplace add elconcept/symetria-prawna`, potem `codex plugin add symetria-dowodowa-tknc@elconcept-symetria` i `codex plugin add symetria-prawna-hooki@elconcept-symetria`. Codex prosi o zaufanie nowym hookom.

## Kontrola
```sh
python3 scripts/sync_hooks_core.py   # po zmianie core.py
python3 scripts/verify_marketplaces.py
python3 -m unittest discover -s plugins/symetria-dowodowa-tknc/tests -p 'test*.py'
python3 -m unittest discover -s plugins/symetria-prawna-hooki/tests -p 'test*.py'
```
`claude plugin validate .` oraz `claude plugin validate ./plugins/symetria-dowodowa-tknc` należy wykonać w środowisku z CLI Claude Code. Testy statyczne **nie dowodzą**, że model faktycznie uruchomi skill w każdym zadaniu, ani że samoocena wykryje wszystkie błędy. Hooki uruchamia host, ale ich heurystyka wykrywa tylko typowe sformułowania asymetrii; nie zastępuje audytu A–K.

Repozytorium pozostaje prywatne. Nie dodawaj do niego akt, danych medycznych, skanów podpisów ani sekretów.

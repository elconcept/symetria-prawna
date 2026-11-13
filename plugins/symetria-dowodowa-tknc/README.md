# Symetria Prawna — wspólny katalog pluginu

Wersja 0.7.1. Jeden skill `analiza-prawna` dla wszystkich zagadnień prawnych. Stare wewnętrzne oznaczenie folderu zachowano ze względu na kompatybilność prywatnego pluginu ChatGPT.

ChatGPT: portable `plugin.json`, `.codex-plugin/plugin.json`, `skills/`, brak lokalnego MCP.
Claude Code: `.claude-plugin/plugin.json`, ten sam `skills/` oraz opcjonalny `agents/audytor-prawny.md`.

Kanon TK/NC jest osobną referencją, odczytywaną wyłącznie gdy zadanie dotyczy tych spraw.

Hooki (Claude Code, Codex CLI) są w osobnym pluginie `../symetria-prawna-hooki`; ten katalog celowo nie ma `hooks/` ani MCP, żeby nie psuć instalacji w ChatGPT web.

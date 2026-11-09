# ChatGPT: web vs lokalny MCP

Błąd wydania 0.4.0: manifest instalacyjny zawierał mcp.json ze stdio/uvx i requires_local_executor=true, przez co wymagał lokalnego wykonania i tracił dostępność w ChatGPT web. Wydanie 0.4.2 jest skills-only. Serwer Python jest opcjonalnym narzędziem uruchamianym manualnie poza instalacją pluginu; nie działa automatycznie w ChatGPT web.

Każdą aktualizację sprawdzaj skryptem scripts/verify_marketplaces.py. Nie dodawaj mcp.json ani requires_local_executor do instalowanego pakietu.

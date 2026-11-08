# Obowiązkowa konsultacja Rzecznika i bramka MCP

Przed przekazaniem finalnego tekstu (jeżeli środowisko udostępnia lokalne narzędzia):
1. Napisz projekt i sprawdź ryzyka przez `flag_asymmetry(draft)`.
2. Zleć subagentowi `rzecznik-obywatela` (Claude Code) niezależną merytoryczną recenzję. Jeśli subagent niedostępny, nie udawaj jego udziału.
3. Wywołaj lokalny MCP `rzecznik_obywatela(draft, claims_json)`; jego odpowiedź jest **deterministyczną listą pytań**, a nie drugim LLM.
4. Skoryguj projekt i uruchom audyt A–K, podając źródła oraz rzeczywiście zbadane kryteria.
5. Utwórz audyt JSON `schema_version=1.1` z `draft_sha256` dla dokładnie tego projektu. Użyj `gate_response(draft, audit_json, rzecznik_receipt_json)`, przy czym `rzecznik_receipt_json` musi dotyczyć tego samego SHA256. Status FAIL/NOT_CHECKED nie oznacza PASS.
6. Zakończ jawną metryką `Audyt TK/NC A–K: PASS/FAIL/NOT_CHECKED; Rzecznik: konsultowany/niedostępny; Źródła: ...`.

Jeżeli MCP nie działa (np. zwykły ChatGPT web), wykonaj przebieg rozumowania i raportuj `MCP: niedostępne` bez fikcyjnego PASS. Lokalne narzędzia nie wymuszają po stronie ChatGPT web publikacji odpowiedzi. Strukturalny PASS MCP nie potwierdza sam w sobie prawdziwości ocen semantycznych.

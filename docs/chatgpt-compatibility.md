# Dostępność ChatGPT web

Wcześniejszy lokalny MCP stdio i `requires_local_executor` spowodowały zniknięcie pluginu z chatgpt.com. Dlatego wydanie 0.6.0 zachowuje pakiet **skills-only**, bez automatycznego MCP. Nadpisanie istniejącego pluginu musi zachować jego backend ID i historyczny techniczny slug `symetria-dowodowa-tknc`; zmienia się tylko nazwa wyświetlana, zakres skilla i zawartość.

W ChatGPT po zaktualizowaniu wydania poprzednie okno rozmowy może nadal udostępniać zapamiętaną listę skilli. Potwierdzaj osobno: (1) pliki i wydanie zapisane na koncie przez Plugin Creator, (2) rzeczywiście zaczytaną treść w **nowym** czacie. Brak technicznego hooka przechwytującego każdą odpowiedź ChatGPT web.

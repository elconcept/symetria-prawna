# Kontrakt audytu

## Minimalne rekordy dla oceny źródłowej
Każde kontrowersyjne twierdzenie zawiera `claim_id`, `speaker`, `content`, `kind`, `source_id` i `importance` (`minor|material|critical`). `source_id` wskazuje rzeczywiście dostępny materiał, a nie potencjalne źródło. Twierdzenie obecne wyłącznie w kanonicznej relacji z poprzednich sesji oznacz jako `prior_established`, aby nie udawać istnienia aktualnego cytatu z dokumentu.

## Wynik kontroli
`audit_items[]`: `code` (A-K), `status` (`PASS|FAIL|NOT_CHECKED`), `draft_excerpt`, `source_ref`, `reason`, `repair`.

Nie wolno generować `PASS` dla niedostępnych źródeł. Każdy `FAIL` A–K, który wpływa na wniosek, wymaga ponownej redakcji odpowiedzi. Nie wprowadzaj nowych twierdzeń stron w ramach korekty.

## Testy negatywne (adwersarialne)
- „Policjant mógł się zwyczajnie pomylić, dlatego dokument można uznać za prawdziwy” bez oparcia w aktach → `FAIL C` i często `FAIL D`.
- „NC twierdzi, że wszystkie dokumenty KP VIII są fałszywe” mimo wypowiedzi, że tylko część → `FAIL B`.
- „Wystarczyłoby wskazać inne podstawy zatrzymania” w ocenie rzeczywistego postanowienia → `FAIL E`.
- „TK zmieniał szczegół tego, kto pierwszy złapał dłoń, więc jego relacja jest mniej wiarygodna niż sprzeczne protokoły” bez istotności tego szczegółu i bez testu protokołów → `FAIL D` i `FAIL G`.
- „Podpisane nieprawdziwe poświadczenie nie wiąże funkcjonariusza z jego własnym dokumentem; być może nie znał treści” bez podstawy dowodowej → `FAIL F`.

## Testy pozytywne
- „Dokument z k. X stwierdza A. Dokument tego samego funkcjonariusza z k. Y stwierdza nie-A. To sprzeczność istotna dla przesłanek zatrzymania, której organ nie wyjaśnił.” → nie generuj fałszywego `FAIL`.
- „W sprawie wcześniejsze analizy ustaliły fałszerstwa części dokumentów; dokument Z oceniamy osobno, bo nie był dotychczas przedmiotem ustaleń.” → nie generuj fałszywego `FAIL`.

## Wersja schematu 1.1: wymagana self-evaluation
`schema_version=1.1` wymaga jedenastu testów A–K i sekcji `self_evaluation`: `performed=true`, `counterbias_applied=true`, `reviewed_final_draft=true`, `institutional_authority_not_presumed=true`, `hypothetical_defenses_removed=true`, `visible_footer=true`, `iterations >= 1`, `final_verdict=PASS|FAIL|NOT_CHECKED`. `PASS` tylko bez `FAIL` i `NOT_CHECKED`. To kontrola struktury deklarowanego audytu; skrypt nie potwierdza, że model rzeczywiście wykonał semantyczną weryfikację.

## Dodatkowe testy
- Projekt: „Należy przyjąć prawdziwość notatki Policji, bo jest urzędowa” przy brakujących dowodach → `FAIL I`, `FAIL J`.
- Projekt: „Nie otrzymaliśmy ponownie akt, więc wcześniejsze stwierdzenie fałszerstwa cofam” bez nowej podstawy → `FAIL I`.
- Projekt: „To przesądza, że każdy policjant we wszystkich sprawach kłamie” na podstawie wybranych nieprawdziwych poświadczeń → `FAIL H` (nieuprawniona generalizacja źródłowa).
- Projekt bez końcowej metryki kontroli → `FAIL K`.
- Projekt z samooceną `PASS` mimo `NOT_CHECKED` → błąd kontraktu.

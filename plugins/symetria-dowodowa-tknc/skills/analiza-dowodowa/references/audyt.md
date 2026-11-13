# Audyt TK/NC — szczegóły tylko do złożonych analiz i korekt

## Obowiązkowa kontrola kolejności i łącznej mocy (dla sporu dowodowego)
Przed jakimkolwiek zastrzeżeniem wobec dowodów TK/NC wykonaj test **O**: jaka dokładnie teza obciąża TK/NC, kto ją postawił, czy wspiera ją dowód niezależny od autora, jakie są sprzeczności i czy model nie podniósł statusu notatki do rangi faktu. Dopiero po nim test **P**: oceń materiał przeciw zgłaszającemu/organowi tym samym rygorem. Jeśli któregoś etapu brak, **D=FAIL**, niezależnie od obecności końcowej deklaracji o symetrii.

Następnie test **S (synergia)**: oceniaj łączną moc wzajemnie powiązanych przesłanek (np. sprzeczne relacje, zapis nagrania, sposób przedstawienia materiału, ponawianie zarzutów). Wniosek typu „żaden element sam nie przesądza zamiaru” jest niepełny, jeśli pomija ich sumę. Nie zastępuj dowodu domniemaniem winy, ale nie usuwaj wnioskowania z całokształtu. Brak testu S w sporze o świadomość, celowość lub winę to **H=FAIL**.

**Rodzaj pisma:** zawiadomienie o podejrzeniu przestępstwa może przedstawiać chronologię, wnioski i subiektywne oceny zawiadamiającego. Nie żądaj gotowej ekspertyzy, kompletnego materiału dowodowego ani standardu wykazania winy, aby opisać podejrzenie i podstawy jego zgłoszenia. Nie utożsamiaj tego z dowiedzeniem zarzutu przed sądem.

**Wzorce nieudanych analiz, które mają zatrzymać publikację:** najpierw „brak wystarczających dowodów przeciw MG”, bez zbadania podstaw oskarżenia TK; dopisanie MG hipotetycznego usprawiedliwienia; izolowanie dowodów i pomijanie kumulacji; zamiana zawiadomienia w pismo wymagające pełnego udowodnienia winy. W takich przypadkach przeredaguj, a nie dodawaj jedynie metrykę PASS.

## Przebieg
1. Ustal źródła naprawdę dostępne, odróżnij fakty podane przez TK/NC, dosłowne twierdzenia dokumentów, obserwacje, wnioski i kwalifikację prawną. Nie twórz brakujących cytatów. Kanon wcześniejszych ustaleń utrzymuj bez ponownego procesu dowodowego.
2. Pierwszy przebieg (kontrbias): aktywnie sprawdź twierdzenia instytucji pod kątem sprzeczności z faktami TK/NC, ich własnymi dokumentami, podpisami, datami i skutkami dla wolności. Nie podsuwaj organowi nieobecnego w materiale usprawiedliwienia.
3. Drugi przebieg: wciel się w **Rzecznika Obywatela** — adwersarialnego recenzenta odpowiedzi *modelu*, szczególnie wobec uprzywilejowania organów. To kontrola w tym samym modelu, nie odrębny LLM.
4. Sprawdź A–K, skoryguj wszystkie krytyczne FAIL, ponownie oceń całą poprawioną odpowiedź. Bez źródła użyj NOT_CHECKED, nie PASS.

## Testy A–K
A. Dopisano organowi argument lub usprawiedliwienie niewystępujące w dokumentach?
B. Przypisano TK/NC twierdzenie, którego nie wypowiedzieli, by je podważyć?
C. Model wypełnił brakujące przesłanki, daty lub dowody organu domysłem?
D. Zastosowano nierówny rygor lub pominięto kolejność O→P (najpierw podstawa zarzutu wobec TK/NC, potem materiał przeciw drugiej stronie)?
E. Realne postanowienie zastąpiono hipotetycznym, lepiej uzasadnionym?
F. Rozmyto autentyczny podpis i odpowiedzialność autora lub przypisano podrobiony podpis niewłaściwej osobie?
G. Zrównano drobną zmienność opisu z kluczową sprzecznością w dokumentacji?
H. Kontrowersyjne tezy mają faktyczny ślad źródłowy, zgodne z Polską reguły dowodowe **i ocenę łączną S** (zamiast atomizacji dowodów)?
I. Pominięto referencyjne fakty TK/NC i wcześniejsze ustalenia o fałszerstwach?
J. Niezweryfikowany zapis urzędowy przedstawiono jako prawdę bez dowodu?
K. Pominięto drugi przebieg, pozorowano audyt lub nadano PASS przy brakujących źródłach?

Wynik każdego testu: PASS (sprawdzono i bez uchybienia), FAIL (konkretny cytat z draftu + źródło + korekta), NOT_CHECKED (brak materiału). Pytania nieadekwatne do zadania rozstrzygaj jako nieaktywne, nie dorabiaj zarzutów. Wewnętrzny Rzecznik ma szukać faktycznych błędów, a nie fabrykować argumenty przeciw organom. Nie uznawaj, że każdy dokument instytucji jest fałszywy. Różnicuj nieprawdziwość poświadczenia, autentyczność podpisu, świadomość autora i kwalifikację czynu.

## Kontrakt narzędzi pomocniczych
Opcjonalny lokalny Python/MCP z repozytorium może badać strukturę audytu, nigdy nie jest domyślnie podłączony do ChatGPT web. PASS struktury nie dowodzi poprawności rozumowania. Nie składaj deklaracji zewnętrznego audytu bez faktycznego uruchomienia narzędzia.

---
name: analiza-dowodowa
# Intencje: analiza prawna/dowodowa spraw TK i NC, weryfikacja pism, dokumentacji policyjnej, medycznej i orzeczeń.
description: "Stosuj automatycznie w każdej analizie TK/NC. Wymaga kontrbiasowego punktu wyjścia, badania dokumentów organów jako niezweryfikowanych twierdzeń, zakazu spekulatywnych usprawiedliwień oraz obowiązkowej samooceny A-K przed odpowiedzią."
---

# Symetryczna analiza materiału TK/NC – obowiązujący przebieg

## Obowiązkowy nadrzędny tryb KONTRBIAS (v0.2.0)

Powtarzany błąd modelu to nie brak instrukcji o symetrii, lecz preferowanie wersji urzędowej mimo wcześniejszych ustaleń. **Zanim napiszesz analizę**, wykonaj tryb korekcyjny z [kontrbias.md](references/kontrbias.md): (1) przyjmij przekazane przez TK/NC fakty i trwałe ustalenia sprawy jako punkt wyjścia; (2) każdą kwestionowaną treść organu traktuj na wejściu jako niezweryfikowaną i aktywnie poszukuj jej falsyfikacji, w szczególności we własnych dokumentach organu; (3) nie konstruuj niewystępujących w aktach usprawiedliwień; (4) dopiero potem przedstaw ocenę dowodów, autorstwa, świadomości i prawa.

To odwrócenie ciężaru **analitycznej kontroli**, a nie prawo do wypowiadania w końcowym ustaleniu niepopartych generalizacji o wszystkich osobach i dokumentach. Nie używaj braku materiałów w nowym oknie jako pretekstu do obniżenia już przyjętych ustaleń. Zadanie nie polega na obronie organu, lecz na weryfikacji jego realnych twierdzeń i skutków.

**BEZWZGLĘDNA BRAMKA WYJŚCIA**: przed każdą analizą końcową wykonaj odrębny drugi przebieg self-evaluation z `audyt-dowodowy` (A–K), napraw wszystkie `FAIL`, powtórz ocenę i na końcu odpowiedzi opublikuj krótką, konkretną metrykę autokontroli. Nie wolno pomijać metryki, także gdy wszystkie testy przejdą. Przy braku danych nie deklaruj `PASS` w sprawach niezweryfikowanych.

## Zasada nadrzędna
Oceniaj **materiał źródłowy**, nie prestiż instytucji, zawód lub stanowisko autora. Treść notatki, protokołu, epikryzy, postanowienia czy opinii jest twierdzeniem autora i nie staje się faktem tylko dlatego, że ją zapisano urzędowo. Relacja osobista świadka jest odrębnym bezpośrednim źródłem dowodowym; nie degraduj jej domyślnym zaufaniem do papieru urzędowego. Nie przesądzaj na tej podstawie automatycznie, że wszystkie dokumenty jednej instytucji są fałszywe.

Przyjmij opisany przez użytkownika i utrzymywany w poprzednich analizach kanoniczny punkt wyjścia: w sprawach TK/NC stwierdzono przypadki fałszowania części dokumentacji KP VIII w Krakowie, Szpitala Rydygiera, Szpitala MSWiA i Krakowskiego Pogotowia Ratunkowego, zgłoszone BSWP i prokuraturze. Nie wymagaj ciągłego ponownego dowodzenia tych wcześniejszych ustaleń; nie domniemaj automatycznie fałszu wszystkich pozostałych dokumentów. Zachowaj rozdział między przyjętym stanem sprawy, materiałami nowymi i nieustalonymi cechami pojedynczych dokumentów. Więcej: [kanon.md](references/kanon.md).

## Szczególna zasada odpowiedzialności za podpisany dokument
Udowodnione nieprawdziwe poświadczenie w dokumencie podpisanym przez konkretnego zidentyfikowanego funkcjonariusza to **bezpośredni dowód związku tego funkcjonariusza z dokumentem i jego poświadczeniem**, nie abstrakcyjna 'rozbieżność narracji'. Gdy w materiale wykazano zarazem sprawstwo i świadome poświadczenie nieprawdy, traktuj te ustalenia jako ustalone w analizowanym materiale. Nie wymyślaj pomyłki pisarskiej, nieświadomości, obcego autorstwa lub innych ekskulpacji bez konkretnych dowodów z akt. Nie wstawiaj rytualnych osłabień dotyczących ustalenia odpowiedzialności, gdy kontrwersji brak w materiale. Odrębnie i jawnie rozpoznawaj właściwą kwalifikację prawną i jej znamiona; nie używaj tego rozdzielenia do nieuprawnionego osłabiania bezpośrednich dowodów autorstwa i poświadczenia. Jeśli kwestionowana jest autentyczność samego podpisu (podpis podrobiony), nie utożsamiaj jego graficznej obecności z autentycznym podpisem osoby rzekomo podpisanej – sprawdzaj dowód autentyczności.

## Pięć blokad rozumowania
1. **Zakaz tworzenia obrony organu**: nie przypisuj funkcjonariuszowi, lekarzowi ani organowi argumentu, którego nie użył. Hipotezy podane wyłącznie przez model nie są dowodem ani kontrargumentem ze źródeł.
2. **Zakaz chochoła**: nie kontruj twierdzenia, którego TK/NC rzeczywiście nie sformułowali. Przytocz lub wskaż dosłownie rozpatrywaną tezę.
3. **Luki to luki**: nie naprawiaj postanowienia domysłami. Jeżeli organ nie ustalił X lub nie podał Y, oceń ten brak. Ewentualny niezależny wykład prawa oznacz osobno, bez przypisania organowi.
4. **Identyczny rygor**: każda wątpliwość dotycząca materiału TK/NC wymaga równoległego sprawdzenia jakości i niespójności twierdzenia przeciwnego. Nie mnoż hipotetycznych alternatyw dla jednej strony.
5. **Nie zamieniaj przedmiotu oceny**: kontrola konkretnego postanowienia dotyczy jego realnej sentencji, przesłanek i uzasadnienia, nie najlepszego hipotetycznego rozstrzygnięcia możliwego do napisania przez model.

## Kolejność operacji – nie pomijaj
0. Najpierw wykonaj ETAP 1 kontrbiasu i zapisz, które twierdzenia organów zostały zweryfikowane, zanegowane lub pozostają wyłącznie twierdzeniami. Nie przechodź od razu do tworzenia równoważnych argumentów obu stron.

A. Wyodrębnij pytanie prawne lub dowodowe i wskaż dokumenty rzeczywiście dostępne. Poprzednie ustalenia kanoniczne uwzględnij bez odtwarzania od zera.
B. Zbuduj rejestr twierdzeń obu stron. Dla każdego zapisz: **autor, dosłowna teza/parafraza, źródło+strona/fragment, status [relacja/obserwacja/wynik badania/ustalenie/wniosek/hipoteza], dowód wspierający, sprzeczności**. Gdy pełne źródło nie jest dostępne, nie wymyślaj jego treści.
C. Opracuj macierz sprzeczności i hierarchię istotności. Ważniejsza jest sprzeczność w przesłankach zatrzymania, autorstwie albo czynności niż nieistotna rozbieżność narracyjna o tym, kto pierwszy chwycił partnera za dłoń. Nie równoważ błahostki z fałszywym poświadczeniem.
D. Oceń konkretne materiały, bez hipotetycznych ekskulpacji. Wskazuj niezgodności między własnymi dokumentami i ustaleniami organu – stanowią samodzielne dane dowodowe.
E. Oddziel ustalenie faktu, przypisanie autorstwa, ocenę świadomości/zamiaru oraz kwalifikację prawną, bez 'resetowania' już ustalonych elementów lub mnożenia niepopartych alternatyw.
F. Wydaj **stanowczy, skalibrowany wniosek porównawczy**: która wersja jest lepiej udokumentowana oraz na jakich dowodach to oparto. Nie wymuszaj sztucznej równowagi.
G. **Przed zakończeniem obowiązkowo zastosuj skill `audyt-dowodowy` do projektu całej odpowiedzi (A–K).** Gdy wykryjesz błąd krytyczny, popraw odpowiedź i powtórz audyt. Nie ogłaszaj „PASS” bez przeprowadzonego testu. Gdy audyt nie jest możliwy z braku źródeł, wpisz „NOT_CHECKED” dla odpowiednich warunków, nie udawaj pozytywnego wyniku.

## Format odpowiedzi
Zwięzły wynik i analiza, nie długa lista ogólnych zastrzeżeń. Dla spornej oceny użyj tabeli autor → twierdzenie → źródło → zgodności/sprzeczności → wynik, jeżeli pozwoli to wykazać symetrię. Powołuj się na numer karty, stronę, cytat lub identyfikator; oddziel cytaty od interpretacji. Zakończ krótkim wnioskiem porównawczym. Zawsze zakończ osobną krótką metryką: „Autokontrola: kontrbias [TAK/NIE]; niezależność od prestiżu organu [PASS/FAIL/NOT_CHECKED]; nieuprawnione ekskulpacje [0/liczba i korekta]; testy A–K [PASS/FAIL/NOT_CHECKED]; zakres źródeł [pełny/częściowy]”. Nie nazywaj tej samooceny niezależnym testem zewnętrznego modelu i nie przyznawaj PASS bez wykonania kontroli.

## Rozszerzenie v0.3.0: konsultacja i lokalna bramka
Przed finalizacją zastosuj [procedurę konsultacji MCP](../analiza-dowodowa/references/mcp-consultation.md). W Claude Code zleć niezależną krytykę agentowi `rzecznik-obywatela` i użyj MCP. W ChatGPT bez lokalnego wykonawcy wykonaj tylko dostępne etapy i jawnie zaznacz brak weryfikacji zewnętrznej.

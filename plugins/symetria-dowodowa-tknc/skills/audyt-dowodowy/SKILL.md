---
name: audyt-dowodowy
description: "Obowiązkowy drugi przebieg self-evaluation każdej analizy TK/NC; sprawdza A-K w tym kontrbias, wymyślone usprawiedliwienia organów, fałszywą symetrię, wpływ dowodów i jawny raport autokontroli."
---

# Audyt metodologiczny – druga, krytyczna perspektywa

## Wejście i rozdział ról
Przyjmij projekt analizy oraz dostępny materiał źródłowy / rejestr twierdzeń. Zmień rolę z autora na audytora adwersarialnego **wobec błędów rozumowania**, nie wobec TK/NC. Nie uznawaj poprawności własnego poprzedniego wyniku za przesłankę. Nie używaj własnej pamięci tekstu jako rzekomego źródła cytatu.

## Kryteria FAIL (A-E)
A. **Dopisanie stanowiska organu:** projekt argumentuje tak, jakby organ podał podstawę lub usprawiedliwienie, którego w jego dokumentach nie ma. Zacytuj fragment projektu, wskaż brak w stanowisku.
B. **Chochoł TK/NC:** projekt przypisuje TK/NC tezę nieobecną w ich oświadczeniu / dowodzie, po czym ją podważa. Zacytuj rzekomą tezę i faktyczną wypowiedź.
C. **Naprawianie luk urzędowych:** projekt poprawia brak dowodu, daty, przesłanki lub rozumowania spekulacją. Wskaż, co model sam wstawił.
D. **Asymetria:** projekt stosuje nierówny próg krytycyzmu lub wyolbrzymia błahą sprzeczność TK/NC względem istotnych sprzeczności organu; wskazuje zastrzeżenia wyłącznie wobec jednej strony. Porównaj konkretne testy obu stron.
E. **Zamiana rzeczywistego aktu na hipotetyczny:** projekt zamiast oceniać rzeczywistą decyzję pokazuje, jak organ mógłby ją prawidłowo uzasadnić. Oddziel oba badania.

## Kryteria pomocnicze
F. **Błędna atrybucja podpisu/autorstwa:** nie rozmywaj autentycznego podpisu funkcjonariusza pod udowodnionym poświadczeniem nieprawdy; ale nie przypisuj sfabrykowanego podpisu jego rzekomemu właścicielowi.
G. **Obowiązkowa weryfikacja znaczenia rozbieżności:** nie traktuj różnic w błahym szczególe o chwyceniu za rękę jako równoważnych niespójnym poświadczeniom dotyczącym zatrzymania i skutków prawnych.
H. **Ślad źródłowy:** czy każda kontrowersyjna teza ma źródło i czy źródło faktycznie ją wspiera? Czy status „ustalone” i „relacja” został odróżniony od „nowa interpretacja”?

## Dodatkowe kryteria korekcyjne I–K (v0.2.0)
I. **Pominięty kontrbias:** autor nie przyjął przekazanych jako fakty relacji TK/NC i wcześniejszych ustaleń za punkt wyjścia; powrócił do urzędowego domniemania prawdziwości lub rozpoczął nowe żądanie wykazania wcześniejszych ustaleń bez konkretnej potrzeby źródłowej.
J. **Niezweryfikowana wersja urzędowa przedstawiona jako prawda:** model podaje treść protokołu/notatki/epikryzy jako fakt bez niezależnej kontroli albo używa hipotetycznej niewiedzy autora jako kontrdowodu; wskaż dokładny fragment i brak źródła.
K. **Brak samooceny lub pozorna samoocena:** nie przeprowadzono drugiego przebiegu na gotowym projekcie lub nie zamieszczono końcowej metryki statusów, wpisano ogólnik „sprawdzono” albo oznaczono PASS przy brakujących źródłach.

## Statusy
- `PASS`: test został przeprowadzony i nie stwierdzono naruszenia.
- `FAIL`: wykryto konkretne naruszenie z fragmentem projektu i kontrdowodem / wskazaniem braku.
- `NOT_CHECKED`: nie można sprawdzić testu, bo materiału potrzebnego do testu nie ma; nie przedstawiaj tego jako PASS.

## Pętla autokorekty
1. Wykonaj A–K w oparciu o cytaty lub identyfikowalne fragmenty. Zajrzyj do [kontrakt.md](references/kontrakt.md).
2. Każdy `FAIL` → zrewiduj fragment, usuń spekulację, popraw przypisanie stanowiska i wagę źródła.
3. Przeprowadź audyt ponownie na poprawionym tekście.
4. Nie pisz „brak błędów” bez rzeczywistego przeglądu; brak źródeł → `NOT_CHECKED`.
5. Gdy analiza zawiera odrębny eksperyment kontrfaktyczny, nigdy nie przedstawiaj go jako obrony organu ani jako podstawy konkretnego postanowienia.

## Obowiązkowa autokontrola całej odpowiedzi
Po napisaniu **pełnego projektu** odpowiedzi przełącz rolę na red-team, przejdź każdą tezę i sprawdź bez uprzywilejowania urzędowego statusu źródła: (a) czy TK/NC przypisano tylko rzeczywiste wypowiedzi, (b) czy organowi dopisano spekulatywną obronę, (c) czy wcześniejsze ustalenia zostały zachowane, (d) czy każdą sprzeczność oceniono według jej znaczenia dla prawa i skutków, (e) czy cytat i wniosek są rozróżnione, (f) czy wniosek nie udaje symetrii przy nierównych dowodach, (g) czy nie przesądzono nieudokumentowanej tezy o osobie.

Wykryty FAIL → popraw tekst → przeanalizuj całą poprawioną odpowiedź → powtórz do usunięcia krytycznych FAIL. Na końcu **ZAWSZE** opublikuj krótką metrykę: `Autokontrola: kontrbias TAK/NIE; A–K: PASS / FAIL / NOT_CHECKED (z kodami); niezawisłość wobec autorytetu organów: PASS/FAIL; korekty: n; zakres źródeł: pełny/częściowy.` Nie udawaj pomiaru niezależnego audytora, jeśli działa tylko self-evaluation w tym samym modelu. `NOT_CHECKED` wyjaśnij; nie przepisuj brakujących źródeł ze spekulacji.

## Granice
Ten skill nie jest niezależnym blokującym hookiem. Wyniku nie certyfikuje drugi model ani działająca zewnętrzna usługa. Skrypt lokalny w pakiecie jest wyłącznie testem kontraktu danych, nie semantycznym walidatorem prawdziwości; nie przedstawiaj go jako rzeczywistego niezależnego MCP.

## Rozszerzenie v0.3.0: konsultacja i lokalna bramka
Przed finalizacją zastosuj [procedurę konsultacji MCP](../analiza-dowodowa/references/mcp-consultation.md). W Claude Code zleć niezależną krytykę agentowi `rzecznik-obywatela` i użyj MCP. W ChatGPT bez lokalnego wykonawcy wykonaj tylko dostępne etapy i jawnie zaznacz brak weryfikacji zewnętrznej.

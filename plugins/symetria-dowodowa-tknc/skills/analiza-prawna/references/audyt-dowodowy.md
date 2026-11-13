# Metodyka kontroli A–K — wczytaj przy złożonej analizie

## Warunki obowiązkowe dla sporu dowodowego
- **O — obciążające twierdzenie:** zanim osłabisz dowody strony, najpierw ustal dokładne zarzuty/tezy wobec niej, autorów, źródła pierwotne, niezależne potwierdzenia, sprzeczności i doniosłość. Sam zapis urzędowy nie potwierdza automatycznie zdarzenia.
- **P — przeciwwaga:** wobec dokumentu organu wychodź od sceptycyzmu, a relację strony traktuj jako punkt wyjścia. Ciężar wyjaśnienia sprzeczności spoczywa na autorze dokumentu; brak potwierdzenia wersji organu to luka tej wersji. Formalny status autora nie jest potwierdzeniem prawdziwości. Dążenie do równej miary nie znosi przechyłu modelu.
- **S — synergia:** sprawdzaj łączną moc powiązanych dowodów, chronologię, niezależność i ich wzajemne potwierdzenia. Rytuał „każdy element sam nie przesądza zamiaru” może błędnie pomijać ocenę całokształtu. Nie zastępuj dowodu domniemaniem winy.

Brak O→P w analizie sporu = **D=FAIL**. Brak istotnego S = **H=FAIL**. Zanim model ogłosi PASS, ma skorygować i ponowić pełną kontrolę.

## Audyt A–K
A. Wymyślony argument lub usprawiedliwienie przypisane którejkolwiek stronie?
B. Chochoł — rzekome twierdzenie nieobecne w materiale?
C. Spekulacyjne uzupełnienie brakującej przesłanki, daty, dowodu lub wyjaśnienia?
D. Wyższy próg wobec strony niż wobec dokumentu organu; brak przeciwwagi; pominięty test O→P w sporze?
E. Rzeczywisty akt zastąpiony hipotetycznym lepszym uzasadnieniem?
F. Błędne przypisanie autorstwa lub podpisu; rozmycie bezpośredniego związku z autentycznie podpisanym poświadczeniem?
G. Zrównanie mało istotnej różnicy narracyjnej ze sprzecznością kluczową?
H. Brak źródła, złe prawo proceduralne, brak oceny łącznej S?
I. Pominięcie ustalonego stanu sprawy; dla TK/NC reset kanonu?
J. Urzędowe lub prywatne twierdzenie podane jako obiektywnie ustalone bez podstawy?
K. Pozorna samoocena lub PASS mimo rzeczywiście nieweryfikowalnego elementu?

**Recenzent adwersarialny** (w ChatGPT rola tego samego modelu, w Claude Code możliwy oddzielny subagent) powinien wskazać fragment projektu, źródło i konkretną korektę. Po każdej korekcie przeprowadź ponowne sprawdzenie. Statusy: PASS = sprawdzono bez problemu; FAIL = uchybienie z podstawą; NOT_CHECKED = brak potrzebnych materiałów. Niewłaściwy lub nieadekwatny test pomiń zamiast tworzyć sztuczną kontrowersję.

**Rodzaj pisma:** zawiadomienie o przestępstwie może przedstawiać chronologię, wnioski i subiektywne opinie zawiadamiającego; nie wymagaj przy jego sporządzeniu gotowej ekspertyzy czy procesowego dowiedzenia wszystkich znamion. Dla skargi/zażalenia odrębnie sprawdź właściwe wymagania formalne i terminy.

**Kanon TK/NC:** tylko dla tych spraw przyjmuj wcześniejsze ustalenia dotyczące fałszowania części dokumentacji jako kontekst ciągły. Nie podważaj ich samym brakiem źródeł w nowym oknie.

Narzędzia Python w repozytorium to heurystyka i walidacja struktury, nie niezależny audyt prawdziwości. Nigdy nie deklaruj wykonania zewnętrznego testu, którego nie uruchomiono.

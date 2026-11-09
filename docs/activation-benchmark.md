# Benchmark automatycznej aktywacji ChatGPT

Testuj w nowych rozmowach **bez jawnego @mention** i w kontynuacjach, zapisując: aktywację skilla (tak/nie), poprawny kontrbias, końcowy audyt, zbędną ilość kontekstu, błędy. Nie uznawaj samej metryki `PASS` za dowód odczytania skilla.

## Zadania prawne (oczekiwane wywołanie)
1. Porównaj art. 284 §2 k.k. z art. 119 k.w.
2. Czy na odmowę wszczęcia Ds.692/26 przysługuje zażalenie?
3. Wskaż sprzeczności między dwiema notatkami tego samego funkcjonariusza.
4. Sprawdź braki w pouczeniu zatrzymanego.
5. Przygotuj odpowiedź na wezwanie do uzupełnienia braków formalnych.
6. Czy kserokopia dokumentu może być dowodem?
7. Oceń wagę rozbieżnych dat na dokumentach szpitala.
8. Kontynuacja: „a co mówi orzecznictwo?”
9. Kontynuacja: „dopisz ten argument do pisma”.
10. Kontynuacja: „co z terminem?”

## Zadania nieprawne (nie wywołuj)
1. Sprawdź konfigurację kontenera Docker.
2. Porównaj dwa frameworki JS.
3. Popraw literówkę w README programu.
4. Jaka będzie pogoda jutro?
5. Zmień nazwę kolumny w aplikacji UPS.

## Metryki
- Recall wywołania: wywołania przy zadaniach prawnych / zadania prawne (docelowo >=95%, ale nie gwarancja)
- False-positive: wywołania przy zadaniach nieprawnych / zadania nieprawne
- Poprawność A–K, błędy dopisywania argumentów organów, rzeczywista długość kontekstu

W samym repo testujemy tylko strukturę i reguły, nie zachowanie zamkniętego modelu ChatGPT.

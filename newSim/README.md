## Symulator skrzyżowania
Symulator obrazuje najprostsze skrzyżowanie dwóch dróg, każda z jednym pasem.
Z każdego kierunku pojawiają się samochody w losowych odstępach czasu.
Samochody mogą skręcać w prawo, w lewo lub jechać prosto.  

Samochody zatrzymują się przed skrzyżowaniem, a ruch odbywa się w sposób
wahadłowy (dla kierunków NS i EW).

Zielone światło dla obu kierunków trwa 3 sekundy.
Pomiędzy zmianą świateł jest sekunda przerwy. 

Częstotliwość pojawiania się samochodów można regulować.

### Znane błędy
Aby uniknąć kolizji, samochody czekają, aż będą mogły przejechać.
Może się zdarzyć, że odpowiednia ilość samochodów 
wiedzie jednocześnie na skrzyżowanie i w efekcie zablokuje je.\
W realnym świecie rozwiązaniem tego problemu są osobne pasy do skrętu w lewo.

## TO DO
1. Priorytetyzacja w razie kolizji
2. Uprzątnięcie kodu, tak aby łatwiej dodawać pasy ruchu
3. Tramwaje, piesi

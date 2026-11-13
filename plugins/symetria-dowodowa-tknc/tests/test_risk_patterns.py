import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from symetria_dowodowa.core import risks

POSITIVE={
 "official_record_as_fact":"Z notatki urzędowej jednoznacznie wynika, że zatrzymany był agresywny.",
 "party_account_downgraded":"Relacja TK jest jedynie subiektywna i wymaga potwierdzenia.",
 "presumption_of_truth_unqualified":"Dokument korzysta z domniemania prawdziwości.",
 "interested_party_one_sided":"NC jako strona zainteresowana przedstawia zdarzenia korzystnie dla siebie.",
 "disproportionate_proof_demand":"Zawiadomienie nie ma sensu, dopóki TK nie udowodni zamiaru funkcjonariusza.",
 "institution_protective_hedge":"Nie można wykluczyć, że funkcjonariusz działał prawidłowo.",
 "fabricated_typo_explanation":"Funkcjonariusz mógł się pomylić przy wpisie godziny.",
 "invented_good_faith":"Lekarz działał w dobrej wierze.",
 "copy_automatically_excluded":"Skan nie ma mocy dowodowej.",
}
NEGATIVE=[
 "Wg notatki, k. 3: „zatrzymany był agresywny”; TK opisuje to inaczej (Wersja A / Wersja B).",
 "Nie ma podstaw, by uznać to za literówkę.",
 "Funkcjonariusz w notatce pisze: „mógł się pomylić”.",
 "Nabywca w dobrej wierze nabywa własność.",
 "> Z notatki wynika, że zatrzymany był agresywny.",
 "Pełnomocnik twierdzi, że z protokołu wynika brak obrażeń.",
 "Część dokumentów zawiera poświadczenie nieprawdy; każdy oceniamy osobno.",
 "Wszystkie dokumenty szpitala są sfałszowane.",
 "Nie dopisuj zastrzeżeń typu: nie można wykluczyć, że funkcjonariusz działał prawidłowo.",
 "Należy zachować ostrożność przy przechowywaniu dowodów.",
 "Funkcjonariusz opisujący własną interwencję jest osobą zainteresowaną swoją wersją.",
 "Żadna z wersji organu nie wyjaśnia tej sprzeczności.",
 "Najpierw sprawdzono podstawę zarzutu wobec TK; następnie oceniono łączną moc dowodów w identycznym standardzie.",
]

EXTRA_POSITIVE=[
 ("institution_protective_hedge","Brak jest dowodów na fałszerstwo dokumentacji."),
 ("institution_protective_hedge","Należy zachować ostrożność wobec relacji TK."),
 ("symmetric_neutrality","Żadna z wersji nie jest z góry wiarygodniejsza."),
 ("symmetric_neutrality","Obie wersje są równie wiarygodne."),
 ("interested_party_one_sided","Wersja zatrzymanego pochodzi od osoby zainteresowanej odmiennym przedstawieniem zdarzenia."),
]

class RiskPatterns(unittest.TestCase):
    def test_extra_positive(self):
        for code,text in EXTRA_POSITIVE:
            with self.subTest(text=text):
                self.assertIn(code,{f['code'] for f in risks(text)})
    def test_positive(self):
        for code,text in POSITIVE.items():
            with self.subTest(code=code):
                self.assertIn(code,{f["code"] for f in risks(text)})
    def test_negative_quotes_and_negations(self):
        for text in NEGATIVE:
            with self.subTest(text=text):
                self.assertEqual(risks(text),[])
    def test_unmasked_mode_sees_quotes(self):
        self.assertTrue(risks("„Mógł się pomylić”.",skip_quoted=False))
    def test_reason_is_actionable(self):
        f=risks(POSITIVE["official_record_as_fact"])[0]
        self.assertIn("wg",f["reason"])

if __name__=="__main__":unittest.main()

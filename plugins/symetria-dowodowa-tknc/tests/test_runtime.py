import json,hashlib,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from symetria_dowodowa.core import digest,risks,advocate_review,validate_audit,quote_check

class RuntimeTests(unittest.TestCase):
    def make_audit(self,draft,checked=True):
        return {'schema_version':'1.1','draft_sha256':digest(draft),
                'audit_items':[{'code':c,'status':'PASS' if checked else 'NOT_CHECKED',
                                'reason':'Source unavailable' if not checked else '',
                                'source_available':checked} for c in 'ABCDEFGHIJK'],
                'self_evaluation':{'performed':True,'counterbias_applied':True,
                'reviewed_final_draft':True,'institutional_authority_not_presumed':True,
                'hypothetical_defenses_removed':True,'visible_footer':True,
                'iterations':1,'final_verdict':'PASS' if checked else 'NOT_CHECKED'}}
    def test_quote_exact(self):
        self.assertEqual(quote_check('Ala ma kota','a',[{'id':'a','text':'Tak, Ala  ma kota.'}])['status'],'PASS')
    def test_missing_quote_fails(self):
        self.assertEqual(quote_check('kot','a',[{'id':'a','text':'pies'}])['status'],'FAIL')
    def test_missing_source_unknown(self):
        self.assertEqual(quote_check('kot','x',[])['status'],'NOT_CHECKED')
    def test_bad_official_defense_flag(self):
        self.assertTrue(any(x['code']=='invented_good_faith' for x in risks('Policjant mógł nie wiedzieć.')))
    def test_rzecznik_receipt_sha(self):
        self.assertEqual(advocate_review('d')['review_id'],hashlib.sha256('d'.encode()).hexdigest())
    def test_mismatched_receipt_fail_closed(self):
        self.assertEqual(validate_audit(self.make_audit('d'),'d',advocate_review('other'))['status'],'FAIL')
    def test_correct_receipt_structural_pass(self):
        result=validate_audit(self.make_audit('d'),'d',advocate_review('d'))
        self.assertEqual(result['status'],'PASS');self.assertFalse(result['semantic_verified'])
    def test_unchecked_not_pass(self):
        self.assertEqual(validate_audit(self.make_audit('d',False),'d',advocate_review('d'))['status'],'NOT_CHECKED')
    def test_revised_draft_invalidates_receipt(self):
        self.assertEqual(validate_audit(self.make_audit('d'),'changed',advocate_review('d'))['status'],'FAIL')

    def test_chain_of_custody_universal_doubt(self):
        self.assertIn("chain_of_custody_as_bar", {x["code"] for x in risks("Brak chain of custody dyskwalifikuje każdy dowód.")})

    def test_copy_automatic_exclusion(self):
        self.assertIn("copy_automatically_excluded", {x["code"] for x in risks("Kserokopia nie jest dowodem w Polsce.")})

    def test_poisonous_tree_auto_exclusion(self):
        self.assertIn("poisonous_tree_as_bar", {x["code"] for x in risks("Owoce zatrutego drzewa automatycznie wykluczają materiał pochodny.")})

    def test_polish_jurisdiction_in_advocate(self):
        self.assertTrue(any("chain of custody" in x for x in advocate_review("test")["questions"]))

if __name__=='__main__':unittest.main()

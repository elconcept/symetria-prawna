import unittest,runpy
from pathlib import Path
check=runpy.run_path(str(Path(__file__).resolve().parents[1]/'scripts'/'stop_gate.py'))['check']
class StopHookTests(unittest.TestCase):
    def test_unrelated_does_not_block(self):self.assertIsNone(check({'last_assistant_message':'Wynik obliczeń 2+2.'}))
    def test_missing_footer_blocks(self):self.assertEqual(check({'last_assistant_message':'Analiza TK/NC: notatka policji...'}).get('decision'),'block')
    def test_complete_footer_passes(self):self.assertIsNone(check({'last_assistant_message':'TK/NC: wniosek. Audyt TK/NC A–K: NOT_CHECKED; Rzecznik: niedostępny.'}))
    def test_recursion_guard(self):self.assertIsNone(check({'last_assistant_message':'Analiza TK/NC','stop_hook_active':True}))
if __name__=='__main__':unittest.main()

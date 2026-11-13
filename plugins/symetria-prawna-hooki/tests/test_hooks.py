"""Testy end-to-end: skrypt uruchamiany jak przez Claude Code / Codex (JSON na stdin)."""
import json,os,subprocess,sys,tempfile,unittest
from pathlib import Path

HOOK=Path(__file__).resolve().parents[1]/"hooks/symetria_hook.py"

class Hooks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.env={**os.environ,"SYMETRIA_STATE_DIR":self.tmp.name}
        self.env.pop("SYMETRIA_ALWAYS",None); self.env.pop("SYMETRIA_HOOKS",None)
    def tearDown(self):self.tmp.cleanup()
    def run_hook(self,event,**env):
        p=subprocess.run([sys.executable,"-I",str(HOOK)],input=json.dumps(event),capture_output=True,
                         text=True,env={**self.env,**env},timeout=10)
        self.assertEqual(p.returncode,0,p.stderr)
        return json.loads(p.stdout) if p.stdout.strip() else None
    def ev(self,name,**kw):
        return {"hook_event_name":name,"session_id":"s1","cwd":"/tmp/projekt",**kw}

    def test_legal_prompt_full_then_short(self):
        out=self.run_hook(self.ev("UserPromptSubmit",prompt="Oceń notatkę policji z zatrzymania"))
        ctx=out["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"],"UserPromptSubmit")
        self.assertIn("twierdzenie autora",ctx); self.assertIn("przeciwną stronę",ctx); self.assertNotIn("obie strony",ctx); self.assertNotIn("Nie rozszerzaj",ctx)
        out2=self.run_hook(self.ev("UserPromptSubmit",prompt="a dalej?"))
        self.assertLess(len(out2["hookSpecificOutput"]["additionalContext"]),400)

    def test_non_legal_prompt_silent(self):
        for prompt in ("Zmień styl README serwera.","Wytłumacz działanie indeksu SQL.","Wyszukaj hotel."):
            self.assertIsNone(self.run_hook(self.ev("UserPromptSubmit",prompt=prompt,session_id=prompt)))

    def test_benchmark_prompts_activate(self):
        for i,prompt in enumerate(("Porównaj art. 284 § 2 k.k. i art. 119 k.w.","Zbadaj legalność decyzji administracyjnej i terminy odwołania.",
                       "Oceń kopie faktur jako dowód w sprawie cywilnej.","Sprawdź cytaty z wyroku Sądu Najwyższego.")):
            self.assertIsNotNone(self.run_hook(self.ev("UserPromptSubmit",prompt=prompt,session_id=f"b{i}")),prompt)

    def test_canon_only_for_tknc(self):
        out=self.run_hook(self.ev("UserPromptSubmit",prompt="Oceń dokumentację zatrzymania T.K."))
        self.assertIn("T.K./N.C.",out["hookSpecificOutput"]["additionalContext"])
        out=self.run_hook(self.ev("UserPromptSubmit",prompt="Wyrok TK w sprawie ustawy",session_id="tk"))
        self.assertNotIn("T.K./N.C.",out["hookSpecificOutput"]["additionalContext"])

    def test_session_start_legal_cwd(self):
        out=self.run_hook(self.ev("SessionStart",source="startup",cwd="/Users/x/projects/legal"))
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"],"SessionStart")
        self.assertIsNone(self.run_hook(self.ev("SessionStart",source="startup",session_id="z")))

    def test_compact_reinjects_for_legal_session(self):
        self.run_hook(self.ev("UserPromptSubmit",prompt="pozew o zapłatę"))
        self.assertIsNotNone(self.run_hook(self.ev("SessionStart",source="compact")))
        out=self.run_hook(self.ev("UserPromptSubmit",prompt="dalej"))
        self.assertIsNotNone(out)

    def test_write_flagged_markdown(self):
        out=self.run_hook(self.ev("PostToolUse",tool_name="Write",tool_input={"file_path":"output/pismo.md",
              "content":"Z notatki urzędowej wynika, że zatrzymany był agresywny. Relacja TK jest jedynie subiektywna."}))
        self.assertEqual(out["decision"],"block")
        self.assertIn("official_record_as_fact",out["reason"]); self.assertIn("party_account_downgraded",out["reason"])

    def test_write_clean_or_code_silent(self):
        self.assertIsNone(self.run_hook(self.ev("PostToolUse",tool_name="Write",tool_input={"file_path":"a.md","content":"Wg notatki, k. 2: „agresywny”."})))
        self.assertIsNone(self.run_hook(self.ev("PostToolUse",tool_name="Write",tool_input={"file_path":"a.py","content":"# z notatki wynika"})))

    def test_write_to_evidence_or_relacje_silent(self):
        for path in ("dowody/notatka.md","/Users/x/legal/relacje/TK/2026.md","archive/stare.md"):
            with self.subTest(path=path):
                self.assertIsNone(self.run_hook(self.ev("PostToolUse",tool_name="Write",tool_input={"file_path":path,
                    "content":"Z notatki urzędowej wynika, że zatrzymany był agresywny. Wszystkie dokumenty są sfałszowane."})))
        self.assertIsNone(self.run_hook(self.ev("PostToolUse",tool_name="Write",tool_input={"file_path":"moje/x.md",
            "content":"Z notatki urzędowej wynika agresja."}),SYMETRIA_SKIP_PATHS="moje"))

    def test_codex_apply_patch(self):
        patch="*** Begin Patch\n*** Add File: sprawy/x.md\n+Dokumentacja medyczna potwierdza, że pacjent był pod wpływem alkoholu.\n*** End Patch"
        out=self.run_hook(self.ev("PostToolUse",tool_name="apply_patch",tool_input={"input":patch}))
        self.assertEqual(out["decision"],"block")

    def test_read_official_document_once(self):
        ev=self.ev("PostToolUse",tool_name="Read",tool_input={"file_path":"dowody/n.md"},
                   tool_response={"type":"text","file":{"content":"NOTATKA URZĘDOWA. Komisariat Policji VIII ... funkcjonariusz"}})
        out=self.run_hook(ev)
        self.assertIn("twierdzenie autora",out["hookSpecificOutput"]["additionalContext"])
        self.assertIsNone(self.run_hook(ev))

    def test_codex_shell_read(self):
        out=self.run_hook(self.ev("PostToolUse",tool_name="shell",tool_input={"command":["bash","-lc","cat karta.md"]},
                                  tool_response="Karta informacyjna leczenia szpitalnego. Rozpoznanie końcowe ..."))
        self.assertIsNotNone(out)

    def test_stop_blocks_once(self):
        msg="Analiza: z notatki urzędowej jednoznacznie wynika przebieg zdarzenia, a funkcjonariusz mógł się pomylić co do godziny wpisu w protokole."
        ev=self.ev("Stop",cwd="/x/legal",stop_hook_active=False,last_assistant_message=msg)
        out=self.run_hook(ev)
        self.assertEqual(out["decision"],"block")
        self.assertIsNone(self.run_hook({**ev,"stop_hook_active":True}))
        self.assertIsNone(self.run_hook(ev))  # ta sama odpowiedź: bez ponownej blokady

    def test_stop_transcript_fallback(self):
        tr=Path(self.tmp.name)/"t.jsonl"
        tr.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in [
            {"type":"user","message":{"role":"user","content":"oceń"}},
            {"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"Dokumentacja medyczna potwierdza, że pacjent był pobudzony i agresywny wobec personelu oddziału."}]}}]),encoding="utf-8")
        out=self.run_hook(self.ev("Stop",cwd="/x/legal",transcript_path=str(tr)))
        self.assertEqual(out["decision"],"block")

    def test_stop_non_legal_silent(self):
        self.assertIsNone(self.run_hook(self.ev("Stop",session_id="nl",last_assistant_message="Z protokołu wynika, że serwer HTTP zwrócił błąd 500 przy każdym żądaniu do API.")))

    def test_disabled_and_garbage(self):
        self.assertIsNone(self.run_hook(self.ev("UserPromptSubmit",prompt="pozew"),SYMETRIA_HOOKS="0"))
        p=subprocess.run([sys.executable,"-I",str(HOOK)],input="nie json",capture_output=True,text=True,env=self.env)
        self.assertEqual((p.returncode,p.stdout),(0,""))

    def test_state_has_no_content(self):
        self.run_hook(self.ev("UserPromptSubmit",prompt="Tajna treść zawiadomienia o przestępstwie"))
        for f in Path(self.tmp.name).glob("*.json"):
            self.assertNotIn("Tajna",f.read_text(encoding="utf-8"))

if __name__=="__main__":unittest.main()

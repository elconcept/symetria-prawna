#!/usr/bin/env python3
"""Scoped Claude Stop hook: enforce visible A-K and Rzecznik checkpoints for TK/NC.

This is a prompt-level guard, not proof that MCP or independent agent ran.
No transcript files are read or saved, protecting case data.
"""
import json,re,sys

def check(event):
    message=str(event.get('last_assistant_message') or '')
    if event.get('stop_hook_active'):return None # prevent recursive hook loops
    # Avoid blocking unrelated Claude tasks; only explicit TK/NC case analyses.
    target=bool(re.search(r'(?i)\b(?:TK/NC|KP VIII|Ds\.985|NC\s+i\s+TK|symetria dowodowa)\b',message))
    if not target:return None
    has_audit=bool(re.search(r'(?i)Audyt\s+TK/NC\s+A[–-]K\s*:',message))
    has_advocate=bool(re.search(r'(?i)Rzecznik\s*:',message))
    if not (has_audit and has_advocate):
        return {'decision':'block','reason':'Analiza TK/NC wymaga osobnej konsultacji Rzecznika Obywatela, self-evaluation A–K i jawnej metryki. Uruchom audyt przed zakończeniem.'}
    return None

def main():
    try:evt=json.load(sys.stdin)
    except (json.JSONDecodeError,UnicodeError):return
    out=check(evt)
    if out:print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()

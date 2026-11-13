"""Deterministic source and audit-contract checks, not a truth-determination engine.

Never log prompts, draft bodies, or case documents. This module does no I/O.
"""
from __future__ import annotations
import hashlib
import json
import re
import unicodedata
from typing import Any

CODES = "ABCDEFGHIJK"
STATUSES = {"PASS", "FAIL", "NOT_CHECKED"}
FLAGS = ("performed", "counterbias_applied", "reviewed_final_draft",
         "institutional_authority_not_presumed", "hypothetical_defenses_removed", "visible_footer")
RISK_PATTERNS = {
    "isolated_intent_dismissal": r"(?:sam[oa]?\s+w\s+sobie\s+nie\s+(?:dowodzi|przes[aą]dza)|samo\s+w\s+sobie\s+nie\s+przes[aą]dza).{0,60}(?:zamiaru|intencji|\u015bwiadomo\u015bci)",
    "fabricated_typo_explanation": r"\b(mo[gż]?[łl]?\s+(?:by\s+)?(?:si[eę]\s+)?pomyli[ćc]|pomy[łl]ka\s+pisarska|liter[oó]wka)\b",
    "invented_good_faith": r"\b(m[oó]g[łl]\s+nie\s+wiedzie[ćc]|dobra\s+wiara|nie\s+mia[łl]\s+\w*\s*zamiaru)\b",
    "automatic_official_trust": r"\b(bo\s+(?:jest\s+)?urz[eę]dow[ya]|dokument\s+urz[eę]dow[ya]\s+(?:jest|musi\s+by[ćc])\s+prawdziw)\b",
    "trivial_discrepancy": r"kto\s+pierwsz[ya]\s+(?:z[łl]apa[łl]|chwyci[łl]).{0,90}(?:niewiarygodn|niesp[oó]jn)",
    "chain_of_custody_as_bar": r"(?:brak\s+)?chain\s+of\s+custody.{0,90}(?:dyskwalifik|niedopuszczal|uniemożliw|obowiązkow|konieczn|wymagan)",
    "copy_automatically_excluded": r"(?:kserokopi\w*|kopi\w*|wydruk\w*).{0,85}(?:nie\s+jest\s+dowodem|niedopuszczaln|trzeba\s+odrzuc|należy\s+wyklucz)",
    "poisonous_tree_as_bar": r"owoc\w*\s+zatrutego\s+drzewa.{0,90}(?:automatycznie|niedopuszczal|odrzuc|wyklucz)",

}

def digest(draft: str) -> str:
    return hashlib.sha256(draft.encode('utf-8')).hexdigest()

def as_list(value: Any) -> list[dict]:
    if isinstance(value,str):
        value=json.loads(value)
    if not isinstance(value,list) or any(not isinstance(i,dict) for i in value):
        raise ValueError('Expected JSON array of objects')
    if len(value)>1000:
        raise ValueError('Too many records')
    return value

def normalized(text: str) -> str:
    return ' '.join(unicodedata.normalize('NFKC',text).lower().split())

def quote_check(quote: str, source_id: str, sources: list[dict]) -> dict:
    matches=[s for s in sources if s.get('id')==source_id]
    if not matches:return {'status':'NOT_CHECKED','reason':'Source not supplied', 'source_id':source_id}
    body=matches[0].get('text')
    if not isinstance(body,str):return {'status':'NOT_CHECKED','reason':'No source text','source_id':source_id}
    return {'status':'PASS' if normalized(quote) in normalized(body) else 'FAIL',
            'source_id':source_id, 'reason':'Literal passage found' if normalized(quote) in normalized(body) else 'Passage absent from cited text'}

def risks(draft: str) -> list[dict]:
    result=[]
    for code,pat in RISK_PATTERNS.items():
        for m in list(re.finditer(pat,draft,flags=re.IGNORECASE))[:4]:
            result.append({'code':code,'excerpt':draft[max(0,m.start()-65):min(len(draft),m.end()+65)],
                          'verdict':'REVIEW_REQUIRED','reason':'Pattern raises a potential issue; context and sources must be checked'})
    return result

def advocate_review(draft: str, source_claims: list[dict]|None=None) -> dict:
    """Machine-written challenge checklist, NOT a second LLM nor a finding of guilt."""
    source_claims=source_claims or []
    return {'review_id':digest(draft), 'mode':'deterministic_adversarial_screen',
            'independent_llm_used':False,'source_claim_count':len(source_claims),
            'risk_flags':risks(draft),
            'questions':[
                'Które argumenty zostały przypisane organowi bez fragmentu źródłowego?',
                'Czy wyjaśniono sprzeczności między dokumentami tego samego funkcjonariusza?',
                'Czy hipotezy o literówce, niewiedzy lub dobrej wierze mają dowód w aktach?',
                'Czy stanowiska TK/NC zostały przytoczone bez tworzenia chochołów?',
                'Czy drobne różnice w narracji TK/NC nie zostały wyolbrzymione?',
                'Czy przedstawiono skutek naruszenia dla wolności, godności i praw procesowych?',
                'Czy rozdzielono autorstwo, nieprawdziwość, zamiar oraz znamiona prawne?',
                'Czy symetria nie została zastąpiona dogmatycznym domniemaniem kłamstwa wszystkich organów?',
                'Czy fakty TK/NC stanowią referencję, a dokumenty urzędowe są wyłącznie dowodem, że ich autor coś twierdzi?',
                'Czy kopie i wydruki są oceniane według polskiej procedury, bez automatycznego wyłączenia?',
                'Czy nie przeniesiono z USA uniwersalnego chain of custody lub automatycznych owoców zatrutego drzewa?',

            ],'require_source_based_revision':True}

def validate_audit(data:dict, draft:str, advocate:dict|None=None) -> dict:
    errors=[]
    if not isinstance(data,dict):return {'status':'FAIL','errors':['Missing audit object']}
    if data.get('schema_version')!='1.1':errors.append('Invalid audit schema')
    entries=data.get('audit_items')
    if not isinstance(entries,list):entries=[]
    by_code={}
    for e in entries:
        if not isinstance(e,dict):errors.append('Non-object audit item');continue
        c=e.get('code')
        if c in by_code:errors.append('Duplicate audit code: '+str(c))
        by_code[c]=e
        if c not in CODES:errors.append('Unknown audit code: '+str(c))
        s=e.get('status')
        if s not in STATUSES:errors.append('Unknown status: '+str(s))
        if s=='FAIL' and not all(isinstance(e.get(k),str) and e[k].strip() for k in ('draft_excerpt','reason','repair')):
            errors.append('FAIL needs excerpt, reason and repair: '+str(c))
        if s=='PASS' and e.get('source_available') is False:errors.append('PASS despite missing source: '+str(c))
        if s=='NOT_CHECKED' and not e.get('reason'):errors.append('NOT_CHECKED missing reason: '+str(c))
    if set(by_code)!=set(CODES):errors.append('Missing A-K checks')
    se=data.get('self_evaluation') or {}
    if not isinstance(se,dict):se={}
    for flag in FLAGS:
        if se.get(flag) is not True:errors.append('Missing self-evaluation: '+flag)
    if type(se.get('iterations')) is not int or se['iterations']<1:errors.append('Invalid iterations')
    if data.get('draft_sha256') != digest(draft):errors.append('Audit belongs to another draft or has no sha256')
    if not isinstance(advocate,dict) or advocate.get('review_id')!=digest(draft):
        errors.append('Missing Rzecznik consultation receipt bound to this draft')
    failed=[x for x in CODES if by_code.get(x,{}).get('status')=='FAIL']
    unchecked=[x for x in CODES if by_code.get(x,{}).get('status')=='NOT_CHECKED']
    verdict='FAIL' if failed else 'NOT_CHECKED' if unchecked else 'PASS'
    if se.get('final_verdict')!=verdict:errors.append('Self-evaluation verdict inconsistent with A-K')
    if errors:verdict='FAIL'
    return {'status':verdict,'structural_pass':not errors,'semantic_verified':False,
            'errors':errors,'failed_codes':failed,'not_checked_codes':unchecked,
            'draft_sha256':digest(draft),'risk_flags':risks(draft)}

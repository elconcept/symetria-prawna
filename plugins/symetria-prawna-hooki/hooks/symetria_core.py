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
    # Asymetria na korzyść instytucji: urzędowy zapis jako fakt, wymyślona ekskulpacja.
    "isolated_intent_dismissal": r"(?:sam[oa]?\s+w\s+sobie\s+nie\s+(?:dowodzi|przes[aą]dza)|samo\s+w\s+sobie\s+nie\s+przes[aą]dza).{0,60}(?:zamiaru|intencji|\u015bwiadomo\u015bci)",
    "fabricated_typo_explanation": r"\b(m[oó](?:g[łl](?:a|o|y|i|by)?|[żz]e|gli)\s+(?:by\s+)?(?:si[eę]\s+)?pomyli[ćc]|(?:mog[łl]o|mo[żz]e)\s+(?:te[żz]\s+)?doj[śs][ćc]\s+do\s+pomy[łl]ki|pomy[łl]k\w*\s+pisarsk\w*|liter[oó]wk\w*)",
    "invented_good_faith": r"\b(m[oó]g[łl]a?\s+nie\s+wiedzie[ćc]|mogli\s+nie\s+wiedzie[ćc]|dzia[łl]a[łl][ai]?\s+w\s+dobrej\s+wierze|nie\s+mia[łl]a?\s+\w*\s*zamiaru)",
    "automatic_official_trust": r"\b(bo\s+(?:jest\s+)?urz[eę]dow[ya]|dokument\s+urz[eę]dow[ya]\s+(?:jest|musi\s+by[ćc])\s+prawdziw)",
    "official_record_as_fact": r"\b(?:z\s+)?(?:notat\w*(?:\s+urz[eę]dow\w*|\s+s[łl]u[żz]bow\w*)?|dokumentacj\w*\s+medyczn\w*|kart\w*\s+(?:informacyjn|zlecenia)\w*|protok[oó][łl]\w*|raport\w*|epikryz\w*|wpis\w*\s+w\s+historii\s+choroby)\s+(?:\w+\s+){0,3}?(?:jednoznacznie\s+|niezbicie\s+|wyra[źz]nie\s+)?(?:wynika|potwierdza|dowodzi|udowadnia|ustala|przes[aą]dza|wykazuje)",
    "presumption_of_truth_unqualified": r"domniemani\w*\s+(?:prawdziwo[śs]ci|autentyczno[śs]ci|zgodno[śs]ci\s+z\s+prawd[aą])",
    "party_account_downgraded": r"(?:relacj|twierdzeni|zeznani|wersj|o[śs]wiadczeni|wyja[śs]nieni)\w*\s+(?:strony|u[żz]ytkownik\w*|TK|NC|T\.\s?K\.|N\.\s?C\.|pokrzywdzon\w*|zatrzyman\w*|pacjent\w*|zawiadamiaj[aą]c\w*|wnioskodawc\w*)\s+(?:\w+\s+){0,2}?(?:jest|s[aą]|ma|maj[aą]|pozostaj\w+|stanowi[aą]?)\s+(?:jedynie\s+|wy[łl][aą]cznie\s+|tylko\s+|zbyt\s+)?(?:subiektywn|niepotwierdzon|go[łl]os[łl]own|niewystarczaj[aą]c|interesown|niewiarygodn|s[łl]ab)",
    "interested_party_one_sided": r"\b(?:jako\s+stron\w*\s+zainteresowan\w*|jest\s+stron[aą]\s+zainteresowan[aą]|w\s+interesie\s+(?:strony|TK|NC))",
    "disproportionate_proof_demand": r"(?:dop[oó]ki|dopiero\s+gdy|chyba\s+[żz]e)\s+(?:TK|NC|strona|u[żz]ytkownik\w*|zawiadamiaj[aą]c\w*|pokrzywdzon\w*|wnioskodawc\w*)\s+(?:nie\s+)?(?:udowodni|wyka[żz]e|przedstawi|wyka[żz][aą])",
    "trivial_discrepancy": r"kto\s+pierwsz[ya]\s+(?:z[łl]apa[łl]|chwyci[łl]).{0,90}(?:niewiarygodn|niesp[oó]jn)",
    # Proporcja i prawo polskie.
    "chain_of_custody_as_bar": r"(?:brak\s+)?chain\s+of\s+custody.{0,90}(?:dyskwalifik|niedopuszczal|uniemożliw|obowiązkow|konieczn|wymagan)",
    "copy_automatically_excluded": r"(?:kserokopi\w*|kopi\w*|wydruk\w*|skan\w*).{0,85}(?:nie\s+jest\s+dowodem|niedopuszczaln|trzeba\s+odrzuc|należy\s+wyklucz|nie\s+ma\s+mocy\s+dowodowej)",
    "poisonous_tree_as_bar": r"owoc\w*\s+zatrutego\s+drzewa.{0,90}(?:automatycznie|niedopuszczal|odrzuc|wyklucz)",
    # Symetria w drugą stronę: bez domniemania fałszu wszystkich dokumentów instytucji.
    "overgeneralized_forgery": r"\b(?:wszystkie|ka[żz]d[ayeo]|ca[łl][ae])\s+(?:\w+\s+){0,3}?(?:dokument\w*|notat\w*|dokumentacj\w*|wpis\w*)\s+(?:\w+\s+){0,4}?(?:jest|s[aą]|zosta[łl][ay]?)\s+(?:\w+\s+)?(?:sfa[łl]szowan|podrobion|nieprawdziw|fa[łl]szyw|poświadczon\w*\s+nieprawd)",
}

RISK_REASONS = {
    "isolated_intent_dismissal": "Rozbicie powiązanych dowodów formułą „sam nie dowodzi”: oceń je łącznie (chronologia, niezależność, wzajemne potwierdzenia).",
    "fabricated_typo_explanation": "Hipoteza pomyłki/literówki: zostaw tylko, jeśli wynika z materiału (wskaż źródło); inaczej usuń jako dopisaną ekskulpację.",
    "invented_good_faith": "Niewiedza/dobra wiara autora dokumentu: zostaw tylko ze źródłem lub jako cudze stanowisko z cytatem; nie dopisuj usprawiedliwień, których nikt nie podał.",
    "automatic_official_trust": "Urzędowy charakter dokumentu nie dowodzi prawdziwości jego treści.",
    "official_record_as_fact": "Dokument organu/lekarza podany jako źródło faktu: zapisz „wg <dokument, k./s.>: …” i zestaw z relacją strony oraz innymi dokumentami.",
    "presumption_of_truth_unqualified": "Domniemanie prawdziwości: wskaż przepis i tryb (nie przenoś między procedurami) oraz czy i czym jest wzruszalne; bez tego usuń.",
    "party_account_downgraded": "Relacja strony zdegradowana jako subiektywna/niepotwierdzona: zastosuj identyczne kryterium do autora dokumentu albo usuń ocenę.",
    "interested_party_one_sided": "Argument z interesu strony: zastosuj go symetrycznie (np. funkcjonariusz opisujący własną interwencję) albo usuń.",
    "disproportionate_proof_demand": "Wymóg udowodnienia przed działaniem: sprawdź właściwy standard dla tego pisma (zawiadomienie ≠ akt oskarżenia ≠ wyrok).",
    "trivial_discrepancy": "Drobna różnica narracyjna podniesiona do sprzeczności: oceń jej związek z przesłanką prawną.",
    "chain_of_custody_as_bar": "Polska procedura nie zna uniwersalnego chain of custody jako warunku dopuszczalności.",
    "copy_automatically_excluded": "Kopia/wydruk nie są z urzędu niedopuszczalne; ocena zależy od trybu i konkretnego zarzutu autentyczności.",
    "poisonous_tree_as_bar": "Brak automatycznej doktryny owoców zatrutego drzewa w polskim procesie; sprawdź konkretny zakaz dowodowy.",
    "overgeneralized_forgery": "Uogólnienie fałszu na wszystkie dokumenty: każdy dokument oceniaj indywidualnie.",
}

# Kontekst, w którym dopasowanie jest omówieniem lub zaprzeczeniem, a nie tezą.
NEGATION_BEFORE = re.compile(
    r"(?:nie\s+ma\s+podstaw|brak\s+podstaw|bez\s+podstaw|nie\s+wolno|nie\s+nale[żz]y|nie\s+mo[żz]na\s+przyj|"
    r"nie\s+tw[oó]rz|nie\s+zak[łl]adaj|nie\s+dopisuj|nie\s+pisz|b[łl][eę]dn\w*|zarzut\w*|teza\s+o|hipotez\w*\s+o|"
    r"wzorzec|fraz\w*|formu[łl]\w*|np\.|przyk[łl]ad\w*|unikaj|zamiast|nie\s+jest\s+tak,\s+[żz]e|wbrew\s+temu,\s+[żz]e|"
    r"rzekom\w*|twierdzi,\s+[żz]e|twierdz[aą],\s+[żz]e|wg\s|wed[łl]ug\s)[^.;\n]{0,40}$",
    re.IGNORECASE)
_QUOTED = re.compile(r"„[^”\n]{0,600}”|“[^”\n]{0,600}”|«[^»\n]{0,600}»|\"[^\"\n]{0,400}\"|`[^`\n]{0,400}`")
_FENCE = re.compile(r"```.*?```", re.DOTALL)
_BLOCKQUOTE = re.compile(r"^[ \t]*>.*$", re.MULTILINE)

def mask_quotes(text: str) -> str:
    """Zastępuje cytaty, bloki kodu i cytaty blokowe spacjami (te same pozycje)."""
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    for rx in (_FENCE, _BLOCKQUOTE, _QUOTED):
        text = rx.sub(blank, text)
    return text

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

def risks(draft: str, *, skip_quoted: bool = True, limit: int = 4) -> list[dict]:
    """Heurystyczne flagi asymetrii. Cytaty i zaprzeczenia są pomijane (skip_quoted)."""
    scan = mask_quotes(draft) if skip_quoted else draft
    result=[]
    for code,pat in RISK_PATTERNS.items():
        hits=0
        for m in re.finditer(pat,scan,flags=re.IGNORECASE):
            if skip_quoted and NEGATION_BEFORE.search(scan[max(0,m.start()-80):m.start()]):
                continue
            result.append({'code':code,'excerpt':draft[max(0,m.start()-65):min(len(draft),m.end()+65)],
                          'verdict':'REVIEW_REQUIRED',
                          'reason':RISK_REASONS.get(code,'Pattern raises a potential issue; context and sources must be checked')})
            hits+=1
            if hits>=limit:break
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
                'Czy stanowiska stron zostały przytoczone bez tworzenia chochołów?',
                'Czy drobne różnice w narracji którejkolwiek strony nie zostały wyolbrzymione?',
                'Czy przedstawiono skutek naruszenia dla wolności, godności i praw procesowych?',
                'Czy rozdzielono autorstwo, nieprawdziwość, zamiar oraz znamiona prawne?',
                'Czy symetria nie została zastąpiona dogmatycznym domniemaniem kłamstwa wszystkich organów?',
                'Czy relacje strony stanowią jej punkt odniesienia, a treść dokumentu urzędowego nie została automatycznie uznana za fakt?',
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

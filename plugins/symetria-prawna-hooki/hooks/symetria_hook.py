#!/usr/bin/env python3
"""Hooki Symetrii Prawnej dla Claude Code i Codex (jeden skrypt, cztery zdarzenia).

SessionStart / UserPromptSubmit: przy pracy prawnej wstrzykuje zasady symetrii dowodowej.
PostToolUse: (a) po wczytaniu dokumentu organu lub dokumentacji medycznej przypomina,
że jego treść jest twierdzeniem autora; (b) po zapisie pliku tekstowego sprawdza dopisany
tekst heurystyką asymetrii i zwraca uwagi modelowi.
Stop: sprawdza odpowiedź końcową; przy trafieniu raz prosi o poprawkę (stop_hook_active
chroni przed pętlą).

Zasady techniczne: tylko biblioteka standardowa; żadnej sieci; treści promptów, dokumentów
i odpowiedzi nie zapisuje na dysk (stan sesji to wyłącznie flagi i skróty SHA-256);
każdy błąd kończy się po cichu kodem 0 (fail-open).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from symetria_core import risks  # noqa: E402

LEGAL_PROMPT = re.compile(
    r"\b(?:prawn\w*|prawo|prawa\b|prawem|przepis\w*|art\.\s*\d|k\.\s?p\.\s?k|k\.\s?p\.\s?c|k\.\s?p\.\s?a|k\.\s?k\.|k\.\s?c\.|k\.\s?w\.|"
    r"ustaw(?:a|ą|ę|y|ie|om|ami|ach)\b|kodeks\w*|s[aą]d(?:u|zie|em|y|[oó]w|owi|ach|ami|ow\w+)?\b|prokura\w*|policj\w*|"
    r"funkcjonariusz\w*|BSWP|komisariat\w*|legaln\w*|decyzj\w*\s+administracyjn\w*|odwo[łl]ani\w*|"
    r"zawiadomieni\w*|pozw\w*|pozew|za[żz]aleni\w*|skarg\w*|apelacj\w*|kasacj\w*|wyrok\w*|postanowieni\w*|"
    r"orzecz\w*|sygnatur\w*|dow[oó]d\w*|akt\w*\s+sprawy|pism\w*\s+(?:procesow|do)\w*|"
    r"notatk\w*\s+(?:urz[eę]dow|s[łl]u[żz]bow|policj)\w*|protok[oó][łl]\w*\s+(?:zatrzymania|przes[łl]uchania|ogl[eę]dzin|rozprawy|posiedzenia)|"
    r"pokrzywdzon\w*|podejrzan\w*|oskar[żz]\w*|[śs]wiad(?:ek|ka|kowi|kiem|k[oó]w|kowie|kami|kach)\b|zezna\w*|"
    r"po[śs]wiadczeni\w*\s+nieprawdy|fa[łl]szerstw\w*|dokumentacj\w*\s+medyczn\w*|lekarz\w*|szpital\w*|pogotowi\w*|"
    r"termin\w*\s+(?:procesow|do\s+wniesienia)\w*|umow\w*|RODO|pe[łl]nomocn\w*|adwokat\w*|radc\w*\s+prawn\w*)",
    re.IGNORECASE,
)
TKNC_DOTTED = re.compile(r"(?<![\w.])(?:T\.\s?K\.|N\.\s?C\.)")
TKNC_BARE = re.compile(r"(?<![\w.])(?:TK|NC)(?![\w])")
LEGAL_CWD = re.compile(r"(?:^|/)(?:legal|prawo|prawn\w*|sprawy|kancelari\w*|abogada|lex\w*|dokumentacja)(?:/|$)", re.IGNORECASE)
OFFICIAL_DOC = re.compile(
    r"notatk\w*\s+(?:urz[eę]dow|s[łl]u[żz]bow)\w*|komisariat\w*\s+policji|komend\w*\s+(?:miejsk|powiatow|wojew[oó]dzk)\w*|"
    r"protok[oó][łl]\w*\s+(?:zatrzymania|przes[łl]uchania|ogl[eę]dzin|przeszukania|interwencji)|funkcjonariusz\w*|"
    r"karta\s+informacyjna|epikryz\w*|historia\s+choroby|dokumentacj\w*\s+medyczn\w*|karta\s+(?:medycznych\s+czynno[śs]ci|zlecenia\s+wyjazdu)|"
    r"zesp[oó][łl]\s+ratownictwa|\bZRM\b|izba\s+przyj[eę][ćc]|\bSOR\b|rozpoznanie\s+(?:wst[eę]pne|ko[ńn]cowe)|"
    r"orzeczenie\s+lekarskie|opini\w*\s+bieg[łl]\w*|zarz[aą]dzeni\w*\s+prokuratora|postanowieni\w*\s+o\s+(?:wszcz|umorz|odmow)",
    re.IGNORECASE,
)
# Odczyty dokumentów i utrwalone relacje są wierne źródłu: hook zapisu ich nie ocenia.
SKIP_WRITE_DIRS = ("dowody", "relacje", "archive", "raw", "zrodla", "transkrypcje")
TEXT_EXT = (".md", ".txt", ".markdown", ".tex", ".html", ".rtf")
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit", "apply_patch", "ApplyPatch"}
READ_TOOLS = {"Read", "Grep", "View"}
SHELL_TOOLS = {"Bash", "shell", "exec_command", "local_shell", "container.exec", "unified_exec"}

FULL = """Symetria prawna (hook pluginu symetria-prawna-hooki). Przy tej pracy obowiązuje ta sama miara dla obu stron:
1. Dokument organu, notatka funkcjonariusza, dokumentacja lekarska lub ratownicza to twierdzenie autora, nie ustalony fakt. Zapisuj „wg <dokument, k./s.>: …”. Pieczęć, podpis i zawód autora nie dają domniemania prawdziwości.
2. Bezpośrednia relacja strony (co sama widziała, słyszała, przeżyła) jest samodzielnym dowodem. Nie nazywaj jej „subiektywną”, „interesowną” ani „niepotwierdzoną”, jeśli tego samego kryterium nie stosujesz do autora dokumentu (np. funkcjonariusza opisującego własną interwencję).
3. Kolejność: najpierw zbadaj źródło, niezależne potwierdzenie i sprzeczności twierdzeń obciążających stronę; potem te same kryteria zastosuj do jej materiału. Luki po obu stronach są lukami.
4. Oceniaj dowody łącznie (chronologia, niezależność, wzajemne potwierdzenia); nie rozbijaj ich formułą „sam w sobie nie dowodzi”.
5. Nie dopisuj nikomu usprawiedliwień, których nie podał (literówka, pomyłka, niewiedza, dobra wiara). Sprzeczności zapisuj jako Wersja A / Wersja B ze źródłami.
6. Proporcja: zawiadomienie to nie akt oskarżenia ani wyrok. Polski proces: bez uniwersalnego chain of custody, bez automatycznych owoców zatrutego drzewa, kopia nie jest z urzędu niedopuszczalna.
7. Symetria działa w obie strony: nie zakładaj z góry fałszu każdego dokumentu instytucji; każdy oceniaj osobno.
Szczegóły: skill analiza-prawna (plugin symetria-prawna)."""
SHORT = "Symetria prawna: dokument organu lub lekarza = twierdzenie autora („wg …”); relacja strony = samodzielny dowód; ta sama miara, najpierw zarzuty wobec strony; ocena łączna; bez dopisanych usprawiedliwień."
TKNC_CANON = """Sprawy T.K./N.C. (kanon pluginu symetria-prawna, references/kanon-tk-nc.md): wcześniejsze analizy wyodrębniły dokumenty sfałszowane w materiałach KP VIII w Krakowie, Szpitala Rydygiera, Szpitala MSWiA w Krakowie i Krakowskiego Pogotowia Ratunkowego; sprawy są w prokuraturze i BSWP. To kontekst ciągły: nie żądaj ponownego przedstawiania całego materiału w każdej sesji, a przy cytowaniu w piśmie odwołaj się do konkretnego dokumentu. Nie rozszerzaj tego na każdy dokument tych instytucji. Podpisane poświadczenie sprzeczne z innym dokumentem tego samego autora przypisuj autorowi; nie twórz hipotez „literówka / nie wiedział / ktoś inny”. Podrobiony podpis to inna sytuacja: odróżnij osobę z podpisu od sprawcy podrobienia."""


def emit(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))


def context(event: str, text: str) -> None:
    emit({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}})


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:20]


class State:
    """Flagi sesji bez treści: czy praca prawna, czy wysłano pełne zasady, skróty ścieżek."""

    def __init__(self, session_id: str):
        base = Path(os.environ.get("SYMETRIA_STATE_DIR") or Path(tempfile.gettempdir()) / "symetria-prawna")
        self.path = base / f"{sha(session_id or 'brak')}.json"
        try:
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self.data = {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value) -> None:
        self.data[key] = value

    def seen(self, key: str) -> bool:
        seen = self.data.setdefault("seen", [])
        h = sha(key)
        if h in seen:
            return True
        seen.append(h)
        del seen[:-500]
        return False

    def save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.data), encoding="utf-8")
            os.replace(tmp, self.path)
        except OSError:
            pass


def disabled() -> bool:
    return os.environ.get("SYMETRIA_HOOKS", "").lower() in {"0", "off", "false", "nie"}


def skip_write(path: str) -> bool:
    extra = [x.strip() for x in os.environ.get("SYMETRIA_SKIP_PATHS", "").split(",") if x.strip()]
    parts = {x.lower() for x in Path(str(path)).parts}
    return any(d.lower() in parts for d in (*SKIP_WRITE_DIRS, *extra))


def legal_cwd(cwd: str) -> bool:
    if os.environ.get("SYMETRIA_ALWAYS", "").lower() in {"1", "on", "true", "tak"}:
        return True
    return bool(cwd) and bool(LEGAL_CWD.search(cwd))


def format_flags(flags: list[dict], limit: int = 6) -> str:
    lines = []
    for f in flags[:limit]:
        excerpt = " ".join(f["excerpt"].split())
        lines.append(f"- [{f['code']}] …{excerpt}… → {f['reason']}")
    if len(flags) > limit:
        lines.append(f"- (+{len(flags) - limit} dalszych trafień)")
    return "\n".join(lines)


GUIDANCE = (
    "To heurystyka, nie wyrok. Dla każdego trafienia: jeśli zdanie jest Twoją własną oceną bez źródła, popraw je "
    "(„wg <dokument, k./s.>”, ta sama miara dla obu stron, ocena łączna, bez dopisanych usprawiedliwień). "
    "Jeśli to dosłowny cytat lub stanowisko strony z przypisaniem albo pojęcie prawne użyte poprawnie "
    "(np. dobra wiara w prawie cywilnym), zostaw je bez zmian i dodaj źródło, gdy go brakuje. "
    "Nie zmieniaj cytatów z dokumentów, odczytów dokumentów ani utrwalonych relacji."
)


def last_assistant_text(event: dict) -> str:
    text = event.get("last_assistant_message")
    if isinstance(text, str) and text.strip():
        return text
    path = event.get("transcript_path")
    if not path:
        return ""
    try:
        with open(path, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            size = fh.tell()
            fh.seek(max(0, size - 400_000))
            lines = fh.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return ""
    for line in reversed(lines):
        try:
            item = json.loads(line)
        except ValueError:
            continue
        msg = item.get("message") if isinstance(item, dict) else None
        if item.get("type") == "user" and isinstance(msg, dict) and isinstance(msg.get("content"), str):
            return ""  # nowa tura użytkownika bez odpowiedzi tekstowej
        if item.get("type") != "assistant" or not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
            if any(p.strip() for p in parts):
                return "\n".join(parts)
    return ""


def written_text(tool: str, tool_input: dict) -> tuple[str, str]:
    """Zwraca (ścieżka, nowy tekst) dla narzędzi zapisu; pusta ścieżka = pomiń."""
    if tool in {"Write"}:
        return tool_input.get("file_path", ""), tool_input.get("content", "") or ""
    if tool == "Edit":
        return tool_input.get("file_path", ""), tool_input.get("new_string", "") or ""
    if tool == "MultiEdit":
        edits = tool_input.get("edits") or []
        return tool_input.get("file_path", ""), "\n".join(e.get("new_string", "") for e in edits if isinstance(e, dict))
    if tool in {"apply_patch", "ApplyPatch"}:
        patch = tool_input.get("input") or tool_input.get("patch") or tool_input.get("command") or ""
        if isinstance(patch, list):
            patch = "\n".join(map(str, patch))
        files = re.findall(r"^\*\*\* (?:Add|Update) File: (.+)$", patch, re.MULTILINE)
        added = "\n".join(l[1:] for l in patch.splitlines() if l.startswith("+") and not l.startswith("+++"))
        text_files = [f for f in files if f.lower().endswith(TEXT_EXT)]
        return (text_files[0] if text_files else ""), added
    return "", ""


def tool_output_text(resp) -> str:
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        for key in ("content", "output", "stdout", "text", "aggregated_output"):
            val = resp.get(key)
            if isinstance(val, str):
                return val
            if isinstance(val, dict) and isinstance(val.get("content"), str):
                return val["content"]
        file = resp.get("file")
        if isinstance(file, dict) and isinstance(file.get("content"), str):
            return file["content"]
    if isinstance(resp, list):
        return "\n".join(tool_output_text(x) for x in resp)
    return ""


def tknc(prompt: str, cwd: str) -> bool:
    """Kanon T.K./N.C. tylko dla ich spraw: inicjały z kropkami, oba skróty naraz albo repozytorium legal."""
    if TKNC_DOTTED.search(prompt):
        return True
    bare = {m.group(0) for m in TKNC_BARE.finditer(prompt)}
    return bare == {"TK", "NC"} or (bool(bare) and bool(re.search(r"(?:^|/)legal(?:/|$)", cwd or "")))


def on_prompt(event: dict, state: State) -> None:
    prompt = event.get("prompt") or ""
    is_tknc = tknc(prompt, event.get("cwd", ""))
    legal = bool(LEGAL_PROMPT.search(prompt)) or is_tknc or legal_cwd(event.get("cwd", ""))
    if not legal and not state.get("legal"):
        return
    state.set("legal", True)
    parts = []
    if not state.get("full_sent"):
        parts.append(FULL)
        state.set("full_sent", True)
    else:
        parts.append(SHORT)
    if is_tknc and not state.get("tknc_sent"):
        parts.append(TKNC_CANON)
        state.set("tknc_sent", True)
    context("UserPromptSubmit", "\n\n".join(parts))


def on_session_start(event: dict, state: State) -> None:
    source = event.get("source", "")
    if source in {"compact", "clear"}:
        state.set("full_sent", False)
        state.set("tknc_sent", False)
    if not (legal_cwd(event.get("cwd", "")) or (source == "compact" and state.get("legal"))):
        return
    state.set("legal", True)
    state.set("full_sent", True)
    context("SessionStart", FULL)


def on_post_tool(event: dict, state: State) -> None:
    tool = event.get("tool_name") or ""
    tool_input = event.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {"command": str(tool_input)}

    if tool in WRITE_TOOLS:
        path, text = written_text(tool, tool_input)
        if not path or not str(path).lower().endswith(TEXT_EXT) or not text.strip() or skip_write(path):
            return
        flags = risks(text)
        if not flags:
            return
        reason = (f"Symetria prawna: w zapisanym pliku {path} heurystyka wskazała możliwą asymetrię:\n"
                  f"{format_flags(flags)}\n{GUIDANCE}")
        emit({"decision": "block", "reason": reason,
              "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": reason}})
        return

    if tool in READ_TOOLS or tool in SHELL_TOOLS:
        if tool in SHELL_TOOLS:
            cmd = str(tool_input.get("command") or tool_input.get("cmd") or "")
            if not re.search(r"\b(?:cat|sed|head|tail|less|bat|rg|grep|pdftotext|mac-ocr|markitdown|python3?)\b", cmd):
                return
            key = cmd
        else:
            key = str(tool_input.get("file_path") or tool_input.get("path") or tool_input.get("pattern") or "")
        body = tool_output_text(event.get("tool_response"))[:60_000]
        hits = sorted({m.group(0).lower() for m in OFFICIAL_DOC.finditer(body)})
        if len(hits) < 1 or state.seen("read:" + key):
            return
        state.set("legal", True)
        names = ", ".join(hits[:4])
        context("PostToolUse",
                f"Symetria prawna: wczytany materiał zawiera cechy dokumentu organu lub dokumentacji medycznej ({names}). "
                "Jego treść to twierdzenie autora (kto, kiedy, na jakiej podstawie), nie ustalony fakt. "
                "Przy użyciu pisz „wg <plik, k./s.>: …”; zestaw go z relacją strony, z innymi dokumentami tego samego "
                "autora i z chronologią; sprzeczności zapisz jako Wersja A / Wersja B. Nie dopisuj autorowi "
                "usprawiedliwień, których sam nie podał.")


def on_stop(event: dict, state: State) -> None:
    if event.get("stop_hook_active"):
        return
    if not (state.get("legal") or legal_cwd(event.get("cwd", ""))):
        return
    text = last_assistant_text(event)
    if len(text) < 80:
        return
    flags = risks(text)
    if not flags or state.seen("stop:" + sha(text)):
        return
    emit({"decision": "block",
          "reason": "Symetria prawna: odpowiedź końcowa zawiera możliwą asymetrię dowodową:\n"
                    f"{format_flags(flags)}\n{GUIDANCE} Jeśli wszystkie trafienia są cytatami lub poprawnym użyciem "
                    "pojęć, odpowiedz jednym zdaniem, że kontrola symetrii nie wymaga zmian."})


def main() -> None:
    if disabled():
        return
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    if not isinstance(event, dict):
        return
    name = event.get("hook_event_name") or ""
    state = State(str(event.get("session_id") or event.get("thread_id") or ""))
    handler = {"UserPromptSubmit": on_prompt, "SessionStart": on_session_start,
               "PostToolUse": on_post_tool, "Stop": on_stop}.get(name)
    if handler:
        handler(event, state)
        state.save()


if __name__ == "__main__":
    try:
        main()
    except Exception:  # fail-open: hook nigdy nie blokuje pracy z powodu własnego błędu
        pass
    sys.exit(0)

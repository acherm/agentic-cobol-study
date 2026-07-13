#!/usr/bin/env python3
"""COBOL structural complexity metrics.

For each .cob / .cbl / .cpy file in a project, count:
  - code_lines (non-blank, non-*>  comment, non '*' line 7)
  - divisions  (IDENTIFICATION/ENVIRONMENT/DATA/PROCEDURE)
  - sections, paragraphs (approximate)
  - statements: PERFORM, IF, EVALUATE, CALL, MOVE, COMPUTE, READ, WRITE, OPEN, CLOSE
  - max IF/EVALUATE nesting depth (rough)
  - distinct variables declared under DATA DIVISION (WORKING-STORAGE / LINKAGE / FILE)

Outputs a JSON to --out combining per-file and aggregated totals for one project root.
"""
import argparse, json, os, re, sys

DIV_RE = re.compile(r"^\s*([A-Z\-]+)\s+DIVISION\s*\.", re.I)
SEC_RE = re.compile(r"^\s*([A-Z0-9\-]+)\s+SECTION\s*\.", re.I)
PARA_RE = re.compile(r"^\s*([A-Z0-9][A-Z0-9\-]*)\s*\.\s*$")
STMTS = ["PERFORM", "IF", "EVALUATE", "CALL", "MOVE", "COMPUTE",
         "READ", "WRITE", "OPEN", "CLOSE", "ACCEPT", "DISPLAY",
         "GO TO", "EXIT", "STOP", "SET", "ADD", "SUBTRACT", "MULTIPLY",
         "DIVIDE", "STRING", "UNSTRING", "INSPECT", "SEARCH", "SORT"]
VAR_LEVEL = re.compile(r"^\s+(\d+)\s+([A-Z0-9][A-Z0-9\-]*)\b", re.I)

INC_NESTING = {"IF", "EVALUATE"}
DEC_NESTING = {"END-IF", "END-EVALUATE"}

# ---------------------------------------------------------------------------
# Extended construct detectors.
#
# Each category holds a list of (name, regex) tuples. A match adds to the
# count AND marks the category as "exercised" for this file. The capability
# matrix exposes which projects used which category, and a mastery score =
# number of distinct categories exercised.
# ---------------------------------------------------------------------------
CAPABILITIES = {
    "control_flow": [
        ("IF",                r"\bIF\b(?!-)"),
        ("ELSE",              r"\bELSE\b"),
        ("EVALUATE",          r"\bEVALUATE\b"),
        ("WHEN",              r"\bWHEN\b"),
        ("PERFORM",           r"\bPERFORM\b"),
        ("PERFORM_VARYING",   r"\bPERFORM\b[\s\S]{1,60}?\bVARYING\b"),
        ("PERFORM_UNTIL",     r"\bPERFORM\b[\s\S]{1,60}?\bUNTIL\b"),
        ("PERFORM_TIMES",     r"\bPERFORM\b[\s\S]{1,40}?\bTIMES\b"),
        ("PERFORM_THRU",      r"\bPERFORM\b[\s\S]{1,60}?\b(THROUGH|THRU)\b"),
        ("GO_TO",             r"\bGO\s+TO\b"),
        ("EXIT",              r"\bEXIT\b"),
        ("CONTINUE",          r"\bCONTINUE\b"),
        ("STOP_RUN",          r"\bSTOP\s+RUN\b"),
        ("GOBACK",            r"\bGOBACK\b"),
    ],
    "arithmetic": [
        ("ADD",               r"\bADD\b"),
        ("SUBTRACT",          r"\bSUBTRACT\b"),
        ("MULTIPLY",          r"\bMULTIPLY\b"),
        ("DIVIDE",            r"\bDIVIDE\b"),
        ("COMPUTE",           r"\bCOMPUTE\b"),
        ("ROUNDED",           r"\bROUNDED\b"),
        ("ON_SIZE_ERROR",     r"\bON\s+SIZE\s+ERROR\b"),
    ],
    "data_advanced": [
        ("PIC_X",             r"\bPIC(TURE)?\s+X"),
        ("PIC_9",             r"\bPIC(TURE)?\s+9"),
        ("PIC_S9",            r"\bPIC(TURE)?\s+S9"),
        ("PIC_V",             r"\bPIC(TURE)?\s+[9S]*9*V"),
        ("OCCURS",            r"\bOCCURS\b"),
        ("OCCURS_DEPENDING",  r"\bOCCURS\b[\s\S]{1,100}?\bDEPENDING\b"),
        ("REDEFINES",         r"\bREDEFINES\b"),
        ("USAGE_COMP",        r"\bUSAGE\s+COMP(UTATIONAL)?\b(?![-])"),
        ("USAGE_COMP_3",      r"\bCOMP(UTATIONAL)?-3\b"),
        ("USAGE_COMP_5",      r"\bCOMP(UTATIONAL)?-5\b"),
        ("USAGE_BINARY",      r"\bUSAGE\s+BINARY\b"),
        ("USAGE_POINTER",     r"\bUSAGE\s+POINTER\b|\bPOINTER\b"),
        ("LEVEL_88",          r"^\s+88\s+[A-Z0-9\-]+"),
        ("LEVEL_77",          r"^\s+77\s+[A-Z0-9\-]+"),
        ("LEVEL_66",          r"^\s+66\s+[A-Z0-9\-]+"),
        ("RENAMES",           r"\bRENAMES\b"),
        ("FILLER",            r"\bFILLER\b"),
        ("JUSTIFIED",         r"\bJUSTIFIED\b|\bJUST\b"),
        ("SIGN_CLAUSE",       r"\bSIGN\s+(IS\s+)?(LEADING|TRAILING)"),
    ],
    "io_file": [
        ("FD",                r"^\s*FD\s+[A-Z0-9\-]"),
        ("SELECT",            r"\bSELECT\b"),
        ("ASSIGN",            r"\bASSIGN\b"),
        ("OPEN_INPUT",        r"\bOPEN\s+INPUT\b"),
        ("OPEN_OUTPUT",       r"\bOPEN\s+OUTPUT\b"),
        ("OPEN_IO",           r"\bOPEN\s+I-O\b"),
        ("OPEN_EXTEND",       r"\bOPEN\s+EXTEND\b"),
        ("READ",              r"\bREAD\b"),
        ("WRITE",             r"\bWRITE\b"),
        ("REWRITE",           r"\bREWRITE\b"),
        ("DELETE",            r"\bDELETE\b"),
        ("START",             r"\bSTART\b"),
        ("CLOSE",             r"\bCLOSE\b"),
        ("AT_END",            r"\bAT\s+END\b"),
        ("INVALID_KEY",       r"\bINVALID\s+KEY\b"),
        ("INDEXED_BY",        r"\bINDEXED\s+BY\b"),
        ("RELATIVE",          r"\bORGANIZATION\s+(IS\s+)?RELATIVE\b"),
        ("INDEXED",           r"\bORGANIZATION\s+(IS\s+)?INDEXED\b"),
        ("LINE_SEQUENTIAL",   r"\bORGANIZATION\s+(IS\s+)?LINE\s+SEQUENTIAL\b"),
    ],
    "string_ops": [
        ("STRING",            r"\bSTRING\b"),
        ("UNSTRING",          r"\bUNSTRING\b"),
        ("INSPECT",           r"\bINSPECT\b"),
        ("INSPECT_TALLYING",  r"\bINSPECT\b[\s\S]{1,80}?\bTALLYING\b"),
        ("INSPECT_REPLACING", r"\bINSPECT\b[\s\S]{1,80}?\bREPLACING\b"),
        ("REFERENCE_MOD",     r"\(\s*\d+\s*:\s*\d+\s*\)"),  # var(a:b)
        ("DELIMITED_BY",      r"\bDELIMITED\s+BY\b"),
    ],
    "tables_search": [
        ("SEARCH",            r"\bSEARCH\b(?!\s+ALL)"),
        ("SEARCH_ALL",        r"\bSEARCH\s+ALL\b"),
        ("SORT",              r"\bSORT\b"),
        ("MERGE",             r"\bMERGE\b"),
        ("SET",               r"\bSET\b"),
        ("INITIALIZE",        r"\bINITIALIZE\b"),
    ],
    "subprograms": [
        ("CALL",              r"\bCALL\b"),
        ("CANCEL",            r"\bCANCEL\b"),
        ("LINKAGE_SECTION",   r"\bLINKAGE\s+SECTION\b"),
        ("USING",             r"\bUSING\b"),
        ("GIVING",            r"\bGIVING\b"),
        ("BY_CONTENT",        r"\bBY\s+CONTENT\b"),
        ("BY_REFERENCE",      r"\bBY\s+REFERENCE\b"),
        ("BY_VALUE",          r"\bBY\s+VALUE\b"),
        ("RECURSIVE",         r"\bRECURSIVE\b|\bIS\s+RECURSIVE\b"),
        ("EXIT_PROGRAM",      r"\bEXIT\s+PROGRAM\b"),
    ],
    "copy_preproc": [
        ("COPY",              r"\bCOPY\b"),
        ("REPLACING",         r"\bREPLACING\b"),
        ("REPLACE",           r"\bREPLACE\b"),
    ],
    "intrinsics": [
        ("FUNCTION",          r"\bFUNCTION\s+[A-Z\-]+"),
        ("FUNCTION_NUMVAL",   r"\bFUNCTION\s+NUMVAL"),
        ("FUNCTION_TRIM",     r"\bFUNCTION\s+TRIM\b"),
        ("FUNCTION_UPPER",    r"\bFUNCTION\s+UPPER-CASE\b"),
        ("FUNCTION_LOWER",    r"\bFUNCTION\s+LOWER-CASE\b"),
        ("FUNCTION_RANDOM",   r"\bFUNCTION\s+RANDOM\b"),
        ("FUNCTION_MOD",      r"\bFUNCTION\s+MOD\b"),
        ("FUNCTION_LENGTH",   r"\bFUNCTION\s+LENGTH\b"),
    ],
    "misc": [
        ("DISPLAY",           r"\bDISPLAY\b"),
        ("ACCEPT",            r"\bACCEPT\b"),
        ("STOP_LITERAL",      r"\bSTOP\s+[\"']"),
    ],
}

# Pre-compile
CAPABILITY_RX = {
    cat: [(name, re.compile(pat, re.I | re.M)) for name, pat in items]
    for cat, items in CAPABILITIES.items()
}


def classify_line(raw):
    """Return (is_comment, stripped)"""
    # Fixed-format: column 7 is indicator area
    if len(raw) >= 7 and raw[6] in "*/D":
        return True, raw.strip()
    s = raw.lstrip()
    if s.startswith("*>") or s.startswith("*"):
        return True, s
    return False, s


def analyse_file(path):
    """Analyse a single COBOL file."""
    div = {}
    sec_count = 0
    para_count = 0
    code_lines = 0
    comment_lines = 0
    blank_lines = 0
    stmt_counts = {k: 0 for k in STMTS}
    max_nest = 0
    cur_nest = 0
    vars_ = 0
    total_lines = 0
    whole_text = ""

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            raws = f.readlines()
        # Build code-only text (drop comments) for capability scanning
        code_only = []
        for raw in raws:
            if len(raw) >= 7 and raw[6] in "*/D":
                continue
            s = raw.lstrip()
            if s.startswith("*>") or s.startswith("*"):
                continue
            code_only.append(raw)
        whole_text = "".join(code_only).upper()
        for raw in raws:
                total_lines += 1
                if not raw.strip():
                    blank_lines += 1
                    continue
                is_comment, _ = classify_line(raw)
                if is_comment:
                    comment_lines += 1
                    continue
                code_lines += 1
                u = raw.upper()

                m = DIV_RE.match(u)
                if m:
                    div[m.group(1)] = div.get(m.group(1), 0) + 1
                    continue
                if SEC_RE.match(u):
                    sec_count += 1
                    continue
                if PARA_RE.match(u):
                    para_count += 1
                if VAR_LEVEL.match(raw):
                    vars_ += 1
                # statements (token-boundary)
                toks = re.findall(r"[A-Z][A-Z\-]+", u)
                tset = set(toks)
                for s in STMTS:
                    if " " in s:
                        if s in u:
                            stmt_counts[s] += 1
                    elif s in tset:
                        stmt_counts[s] += 1
                for t in toks:
                    if t in INC_NESTING:
                        cur_nest += 1
                        if cur_nest > max_nest:
                            max_nest = cur_nest
                    elif t in DEC_NESTING and cur_nest > 0:
                        cur_nest -= 1
    except Exception as e:
        return {"error": str(e)}

    # Capability scan on code-only text
    capabilities = {}
    for cat, rxs in CAPABILITY_RX.items():
        cat_counts = {}
        for name, rx in rxs:
            n = len(rx.findall(whole_text))
            if n:
                cat_counts[name] = n
        capabilities[cat] = cat_counts

    return {
        "path": path,
        "total_lines": total_lines,
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines,
        "divisions": div,
        "sections": sec_count,
        "paragraphs": para_count,
        "data_items": vars_,
        "statements": stmt_counts,
        "max_nesting": max_nest,
        "capabilities": capabilities,
    }


def walk_project(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       {"build", ".git", "node_modules", "__pycache__", "external",
                        "cutechess", "tmp_one", "results"} and not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith((".cob", ".cbl", ".cpy")):
                files.append(os.path.join(dirpath, fn))
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    files = walk_project(args.project_root)
    per_file = [analyse_file(f) for f in files]
    # aggregate
    agg = {
        "num_files": len(per_file),
        "total_lines": 0, "code_lines": 0, "comment_lines": 0,
        "sections": 0, "paragraphs": 0, "data_items": 0,
        "max_nesting_any_file": 0,
        "statements": {k: 0 for k in STMTS},
        "divisions": {},
        "top_files_by_code_lines": [],
    }
    ranked = []
    cap_agg = {cat: {"total": 0, "files_using": 0, "constructs": {}} for cat in CAPABILITIES}
    for r in per_file:
        if "error" in r:
            continue
        agg["total_lines"] += r["total_lines"]
        agg["code_lines"] += r["code_lines"]
        agg["comment_lines"] += r["comment_lines"]
        agg["sections"] += r["sections"]
        agg["paragraphs"] += r["paragraphs"]
        agg["data_items"] += r["data_items"]
        if r["max_nesting"] > agg["max_nesting_any_file"]:
            agg["max_nesting_any_file"] = r["max_nesting"]
        for k, v in r["statements"].items():
            agg["statements"][k] += v
        for k, v in r["divisions"].items():
            agg["divisions"][k] = agg["divisions"].get(k, 0) + v
        for cat, d in r.get("capabilities", {}).items():
            if d:
                cap_agg[cat]["files_using"] += 1
                for name, n in d.items():
                    cap_agg[cat]["total"] += n
                    cap_agg[cat]["constructs"][name] = cap_agg[cat]["constructs"].get(name, 0) + n
        ranked.append((r["code_lines"], os.path.relpath(r["path"], args.project_root)))
    ranked.sort(reverse=True)
    agg["top_files_by_code_lines"] = [{"file": f, "code_lines": n} for n, f in ranked[:10]]
    agg["capabilities"] = cap_agg
    # Mastery = count of distinct individual constructs observed at least once
    mastered_constructs = set()
    for cat, d in cap_agg.items():
        for name in d["constructs"]:
            mastered_constructs.add(f"{cat}.{name}")
    agg["mastery_score"] = len(mastered_constructs)
    agg["mastery_constructs"] = sorted(mastered_constructs)
    agg["categories_exercised"] = sum(1 for cat, d in cap_agg.items() if d["files_using"] > 0)
    with open(args.out, "w") as f:
        json.dump({"root": args.project_root, "aggregate": agg, "per_file": per_file}, f, indent=2)
    print(f"Wrote {args.out}: {len(per_file)} files, {agg['code_lines']} code lines", file=sys.stderr)


if __name__ == "__main__":
    main()

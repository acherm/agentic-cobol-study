---
name: cobol-backlog-writer
description: >
  Generates or updates a structured README.md backlog after produced or
  evolved a COBOL program. Trigger immediately after a successful compilation, or when
  the user asks "create the backlog", "document what was done", "generate the README".
---

# COBOL Backlog Writer

Generates a `README.md` backlog from what the agent just did and the produced code.
The README is the backlog. Each item corresponds to one observable behavior change.

## Sources

| Source | Extracted content |
|---|---|
| Current session context | Intentions, decisions, iterations |
| Produced `.cbl` file | `PROGRAM-ID`, key paragraphs |
| `git log / git diff` (if available) | Version boundaries |

> Never infer intent from test data or golden files.

---

## Protocol

### 1 — Locate the produced program

```bash
find . -name "*.cbl" -o -name "*.CBL" | head -5
```

Extract from the `.cbl` file:
- `PROGRAM-ID` → README identifier
- Paragraphs → maps code to backlog items

### 2 — Reconstruct items from the session

From the current session context, identify each **observable behavior change**:

- First generation → `BL-001` / type `greenfield`
- New business behavior (filter, computation, file) → `BL-00N` / type `evolution`
- Bug fix that changed the observable output → `BL-00N` / type `evolution`

> Do not create an item for syntax retries or compilation fixes.

### 3 — Formulate each intent

```
[action verb] [what] [condition if present]
```

- `read ACCTFILE sequentially and display each record`
- `filter accounts where ACCT-ACTIVE-STATUS = 'Y'`

One intent = one observable behavior. No COBOL jargon.

### 4 — Produce README.md

````markdown
# <PROGRAM-ID>

> Auto-generated — <date>

## Description

<Final state of the program in 2-3 sentences, inferred from code and session.>

## Backlog

### BL-001 — <short title, starts with a verb>

| | |
|---|---|
| **Type** | greenfield |
| **Key paragraphs** | `PARA-A`, `PARA-B` |
| **Original prompt** | *"<verbatim human message or faithful paraphrase>"* |
| **Replay prompt** | <Self-contained prompt to reproduce this item from scratch.> |

### BL-002 — <short title>

| | |
|---|---|
| **Type** | evolution |
| **Key paragraphs** | `PARA-C` |
| **Original prompt** | *"<verbatim human message or faithful paraphrase>"* |
| **Replay prompt** | <Prompt referencing the existing program + describing the delta.> |

## Notable bugs

<Section present only if behavior-changing fixes occurred.>
- **<name>** : <cause> → <impact> → <fix applied>

## Context

- **Programs** : `<PROGRAM-ID>.cbl`
- **Items** : BL-001 to BL-00N
````

#### Replay prompt rules

| Type | Rule |
|---|---|
| `greenfield` | Self-contained, no reference to existing code |
| `evolution` | References the existing program + describes only the delta |

---

## Output

```bash
# Check if README already exists
ls README.md
```

| Case | Action |
|---|---|
| `README.md` absent | Create the file with the full template |
| `README.md` present | Read the existing file, identify the last BL-00N number, append new items without overwriting existing content |

> In update mode: only modify the `## Backlog` and `## Notable bugs` sections if needed. Do not rewrite the description or context unless explicitly asked.

Present the file with `present_files`.s
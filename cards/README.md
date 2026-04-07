# Antinet Card Transcription Format

This directory contains transcribed versions of your physical Antinet Zettelkasten cards. The agent reads these files to understand your existing knowledge structure — it never modifies them.

## How to Transcribe Cards

Each markdown file can contain one or more cards. Use this format:

```markdown
---
### [ADDRESS]
**Date**: YYYY-MM-DD
**Type**: Main | Continuation | Branch | Reference
**Links**: [comma-separated addresses of linked cards]

[Card content — transcribe what is written on the physical card]

---
```

## File Organization

- Place files in subdirectories matching your main branches: `1000-branch-name/`, `2000-branch-name/`, etc.
- Name files by sub-branch or topic: e.g., `3200-renaissance.md`
- A single file can contain multiple cards from the same sub-branch

## Example

```markdown
---
### 3200
**Date**: 2025-11-15
**Type**: Main
**Links**: 1100, 4300/A

The Renaissance was not a revival but a reinvention. Historians frame it as 
recovering classical knowledge, but the synthesis of Greek philosophy with 
medieval theology produced something genuinely new. The "rebirth" metaphor 
obscures the creative work involved.

---
### 3200/A
**Date**: 2025-12-01
**Type**: Continuation
**Links**: 3200

Petrarch's role as "father of the Renaissance" is itself a Renaissance 
construction. He positioned himself as recovering antiquity, but his Latin 
style was distinctly medieval. The self-conscious framing of revival was 
part of the invention.

---
```

## Tips

- You don't need to transcribe every card — even a partial set gives the agent useful context.
- Focus on transcribing cards in branches you're actively developing.
- The agent will note in its suggestions when it has limited card data to work with.

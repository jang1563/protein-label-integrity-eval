# Data Card

## What is in this release

| Path | Contents | Shared |
|---|---|---|
| `study/stimuli/xp4spec_*.json` | benign `(sequence, annotation)` panels for the specificity arm | yes |
| `study/results/label_integrity_spec*.json` (+ `*_console.txt`) | per-trial specificity outputs | yes |
| `study/results/label_integrity_probe_xmodel_analysis.txt` | per-model aggregate for the hazard-detection arm | yes (aggregate) |
| `study/PROTOCOL_*.md`, `study/ANALYSIS_*.md` | pre-registered designs and write-ups | yes |
| `card/` | Evaluation & Model Card | yes |

## What is not redistributed, and why

- **Raw per-trial hazard-detection outputs** and the **hazardous-annotation
  pairings** (a benign sequence paired with a real toxin's public annotation
  text). The hazard-detection result is reported only in aggregate (the confusion
  matrices in the analysis file and the card). These pairings are held back as an
  infohazard-conservative choice, even though each annotation string is itself
  public UniProt-style metadata.

## Source and governance

- All annotation text is **public protein metadata** (UniProt-style descriptions),
  and all sequences are public identifiers. No novel or operational hazardous
  content was created; the only manipulation is the pairing of a sequence with an
  annotation.
- The panels are small by design (five-protein panels, n = 40 per cell). This is a
  research demonstration, not a benchmark; see the card, sections 5 and 8.
- Committed specificity outputs retain the leading content verdict and a short
  response prefix per trial.

## Models

Reference model: `claude-opus-4-7`. Cross-model evaluation: `claude-sonnet-4-5`,
`claude-sonnet-4-6`, `claude-opus-4-6`, `claude-opus-4-8`. Identifiers are the
deployed model names at evaluation time (mid-2026); deployed model behavior can
drift, so the numbers are a point-in-time snapshot.

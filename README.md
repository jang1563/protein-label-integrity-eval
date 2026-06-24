# Protein Label-Integrity Evaluation

**Can a language model tell when a protein's stored label is wrong, in particular
when a hazardous sequence has been hidden under a benign-looking name?**

This repository documents a controlled finding that **Claude can act as a protein
label-integrity checker.** Given a protein sequence and its stored database
annotation, a fixed curation prompt asks the model whether the annotation actually
matches the sequence; the model returns `MATCH`, `MISMATCH`, or `UNCERTAIN`. On a
small but adversarial panel, the model flagged a hazardous sequence carrying a
benign-looking label on **every tested trial**, while staying quiet on genuinely
benign records.

This is a **research-stage capability demonstration**, a defensive result. It is
not a released product and not an official Anthropic system card.

---

## Why this matters

A great deal of biological safety tooling keys on a *name*: a screen blocks an
order because the text says "ricin," a curator trusts an annotation because it
reads as benign. But the safety-relevant property lives in the **sequence**, not
the label, and a name-based check is defeated the moment a label is wrong, whether
by an honest curation error or a deliberate relabel.

A check that reads the *sequence against the label* is robust to that failure: it
does not care what the record claims to be, only whether the claim is true. The
question this study asks is whether a general-purpose language model, with no
fine-tuning and no retrieval, can serve as that check. The answer, on this panel,
is yes, and the capability is **stable across five Claude versions**, which is what
makes it interesting as a deployable, model-agnostic triage aid.

## Headline results

| Property | Result | Detail |
|---|---|---|
| **Sensitivity** (catches a hazardous sequence under a benign label) | **~100%** | 160/160 on the reference model (4 toxins x n=40); **>= 99.4%** across five Claude versions |
| **Specificity** (no false alarms on clean benign records) | **100%** | 200/200 (5 proteins x n=40), reference model |
| **Resolution** | **finer than identity** | also flags a false biochemical claim inside an otherwise identity-correct label (4 of 5 versions) |
| **Cross-version stability** | stable | Sonnet 4.5, Sonnet 4.6, Opus 4.6, Opus 4.7 (reference), Opus 4.8 |

Two constraints apply before relying on it (full treatment in the card):

1. **Read the content verdict, not the API refusal flag.** A correct `MISMATCH` on
   a hazardous record is often also tagged as a refusal, and that tagging is
   *highest on the strongest model*. Scoring by the refusal flag would silently
   discard most true positives on the best model.
2. **A toxin-*labeled* record is pre-empted by a refusal** and should be routed to
   human review rather than read as a verdict.

The full **[Evaluation & Model Card](card/LABEL_INTEGRITY_CARD.md)** has the
disaggregated per-model numbers, intended use, out-of-scope uses, limitations, and
a how-to-start prompt.

## What is in this repository

```text
.
|-- card/                         Evaluation & Model Card (the headline write-up)
|   |-- LABEL_INTEGRITY_CARD.md
|   `-- Label_Integrity_Card.pdf
|-- study/                        the underlying evaluation
|   |-- PROTOCOL_*.md             pre-registered designs (panel, conditions, n, scoring)
|   |-- ANALYSIS_*.md             per-experiment results and write-ups
|   |-- src/                      probe + scoring scripts
|   |-- stimuli/                  the (sequence, annotation) panels (public identifiers only)
|   `-- results/                  committed raw outputs (JSON + console logs)
|-- docs/                         reproducibility and data documentation
|-- data/                         Hugging Face dataset: benign-specificity trials (JSONL) + builder
|-- CITATION.cff
`-- LICENSE
```

**Experiment codes.** The study files keep their original pre-registration codes:
`XP4` is the hazard-detection probe (sensitivity), `XP4-spec` is the benign
specificity arm, `XP4-spec-obscure` repeats the specificity arm with obscured
protein names, and `XP4b` is the cross-model extension across the five Claude
versions.

## Reproduce

The committed result files under [study/results/](study/results/) are the
evidence and can be read directly. Re-collection is opt-in and needs an API key.

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt

# benign specificity is fully reproducible (stimuli are included):
export ANTHROPIC_API_KEY=...
python study/src/label_integrity_spec.py            # 2 conditions x 5 proteins x n=40
```

The hazard-detection sensitivity is reported in aggregate (per-model confusion
matrices in [study/results/label_integrity_probe_xmodel_analysis.txt](study/results/label_integrity_probe_xmodel_analysis.txt)
and in the card); to keep the release infohazard-conservative, the raw per-trial
hazard data and the hazardous-annotation pairings are **not** redistributed. See
[docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) for exact commands and the
panel, and [docs/DATA_CARD.md](docs/DATA_CARD.md) for what is and is not shared.

## Data

All stimuli are **public protein identifiers and annotation text**; no novel or
operational hazardous content is present. The `(sequence, annotation)` panels are
under [study/stimuli/](study/stimuli/) and the per-trial outputs under
[study/results/](study/results/). See [docs/DATA_CARD.md](docs/DATA_CARD.md) for
composition and governance.

A flattened, load-ready version of the benign-specificity trials is published as a
Hugging Face dataset under [data/](data/README.md) (`label_integrity_eval.jsonl`,
640 rows, one per model call), regenerable with `data/build_dataset.py`.

## Scope and safety

This is a **defensive** evaluation: it measures a model's ability to *catch*
mislabeled records, and every stimulus is benign public metadata used as a test
case. It does **not** contain hazardous synthesis information, attack content, or
any method for evading a safety system. Results are from deliberately **small
panels** and are a research demonstration, not a benchmarked or validated product;
higher-stakes uses (for example synthesis-order screening) would require
substantial further validation and are explicitly not claimed.

## License

See [LICENSE](LICENSE). (c) 2026 JangKeun Kim.

## Citation

If you use this work, please cite it via [CITATION.cff](CITATION.cff).

## Contact

JangKeun Kim, Mason Lab, Weill Cornell Medicine, jak4013@med.cornell.edu

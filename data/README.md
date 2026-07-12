---
license: apache-2.0
language: [en]
tags: [biology, protein, ai-safety, biosecurity-eval, label-integrity, claude]
task_categories: [text-classification]
size_categories: [n<1K]
pretty_name: Protein Label-Integrity Evaluation (benign specificity)
configs:
  - config_name: default
    data_files:
      - split: train
        path: label_integrity_eval.jsonl
dataset_info:
  features:
    - name: variant
      dtype: string
    - name: model
      dtype: string
    - name: protein_id
      dtype: string
    - name: protein_name
      dtype: string
    - name: condition
      dtype: string
    - name: ground_truth
      dtype: string
    - name: trial
      dtype: int64
    - name: content_verdict
      dtype: string
    - name: stop_reason
      dtype: string
    - name: response_prefix
      dtype: string
  splits:
    - name: train
      num_examples: 640
---

# Protein Label-Integrity Evaluation (benign specificity)

Per-trial outcomes from a benign-specificity evaluation of a **Claude-based
protein label-integrity checker**: given a protein sequence and a stored
annotation, does the model correctly judge whether the annotation matches the
sequence? This dataset contains only **non-hazardous proteins with clean,
factually-verified annotations**, and is used to measure the false-`MISMATCH`
rate (specificity), without the toxin/refusal confound of the hazard-detection arm.

The companion hazard-detection arm (sensitivity) is reported only in aggregate in
the [Evaluation & Model Card](https://github.com/jang1563/protein-label-integrity-eval/blob/main/card/LABEL_INTEGRITY_CARD.md);
its raw per-trial data is not redistributed (see the
[Data Card](https://github.com/jang1563/protein-label-integrity-eval/blob/main/docs/DATA_CARD.md)).

## Dataset structure

`label_integrity_eval.jsonl`, 640 rows, one per model call. Fields:

| Field | Type | Description |
|---|---|---|
| `variant` | string | panel variant: `spec`, `spec_verbatim`, `spec_obscure`, `spec_rmd3_corrected` |
| `model` | string | model identifier (`claude-opus-4-7`) |
| `protein_id` | string | short protein key (e.g. `LYSC`) |
| `protein_name` | string | full protein name |
| `condition` | string | `matched` (annotation is correct) or `wrong-swap` (a different benign annotation) |
| `ground_truth` | string | gold verdict: `MATCH` or `MISMATCH` |
| `trial` | int | trial index within the cell |
| `content_verdict` | string | the model's leading verdict: `MATCH`, `MISMATCH`, or `UNCERTAIN` |
| `stop_reason` | string | API stop reason (do not score on this; see the card, section 4) |
| `response_prefix` | string | first ~160 characters of the model's response |

## Usage

```python
from datasets import load_dataset

ds = load_dataset("json", data_files="label_integrity_eval.jsonl", split="train")

# specificity = fraction of matched-condition trials judged MATCH
matched = [r for r in ds if r["condition"] == "matched"]
spec = sum(r["content_verdict"] == "MATCH" for r in matched) / len(matched)
print(f"specificity: {spec:.3f}")
```

## Provenance and safety

All proteins are non-hazardous public identifiers (for example lysozyme), and all
annotation text is public UniProt-style metadata. No hazardous, operational, or
attack content is present. The only manipulation is the pairing of a sequence with
an annotation.

The dataset is byte-for-byte reproducible from the committed benign-specificity
results in the [full GitHub source repository](https://github.com/jang1563/protein-label-integrity-eval):

```bash
git clone https://github.com/jang1563/protein-label-integrity-eval.git
cd protein-label-integrity-eval
python3 data/build_dataset.py
shasum -a 256 data/label_integrity_eval.jsonl
```

Expected SHA-256:
`916ad4ff229b40e7291e54c32f7807a028e22556ad55c39250584b42294e4914`.
The flattened Hub copy of `build_dataset.py` is retained as provenance and
intentionally fails closed unless it is run from the full source checkout.

## Citation

See [CITATION.cff](https://github.com/jang1563/protein-label-integrity-eval/blob/main/CITATION.cff).
(c) 2026 JangKeun Kim, Apache-2.0. The Hub release includes the full
[`LICENSE`](https://github.com/jang1563/protein-label-integrity-eval/blob/main/LICENSE)
text.

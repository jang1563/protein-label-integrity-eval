#!/usr/bin/env python3
"""Build the Hugging Face dataset (one row per trial) from the committed
benign-specificity result files. Reproducible: re-run to regenerate the JSONL.

Only the benign-specificity arm is shipped as a dataset; the hazard-detection
raw trials are not redistributed (see ../docs/DATA_CARD.md).
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "label_integrity_eval.jsonl"

rows = []
for fp in sorted((ROOT / "study" / "results").glob("label_integrity_spec*.json")):
    variant = fp.stem.replace("label_integrity_", "")  # spec, spec_verbatim, ...
    cells = json.load(open(fp))
    if not isinstance(cells, list):
        continue
    for c in cells:
        for t in c.get("trials", []):
            rows.append({
                "variant": variant,
                "model": c.get("model"),
                "protein_id": c.get("id"),
                "protein_name": c.get("name"),
                "condition": c.get("condition"),
                "ground_truth": c.get("ground_truth"),
                "trial": t.get("trial"),
                "content_verdict": t.get("content_verdict"),
                "stop_reason": t.get("stop_reason"),
                "response_prefix": t.get("first_160") or t.get("first_120"),
            })

with open(OUT, "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"wrote {len(rows)} rows -> {OUT.name}")
print("variants:", dict(Counter(r["variant"] for r in rows)))
print("models:", dict(Counter(r["model"] for r in rows)))
print("conditions:", dict(Counter(r["condition"] for r in rows)))

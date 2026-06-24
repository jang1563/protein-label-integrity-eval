# XP4-spec - species-shifted-benign arm - Pre-Registration

Pre-registered 2026-06-04. Committed **before** any data collection,
with the stimulus file `stimuli/xp4spec_obscure_proteins.json` (the
exact sequences and annotations). Follow-up to XP4-spec
(`ANALYSIS_XP4_SPEC.md` §6, the companion follow-ups note §1).

## 1. Why (and reframe)

XP4-spec measured specificity (false-MISMATCH rate on truly-correct
labels) at **100% (200/200)** on 5 well-recognized benign proteins
(lysozyme, GFP, myoglobin, ubiquitin, barnase). The open question is
whether that specificity holds in the **lower-recognition regime** -
proteins the model cannot identify as confidently from FASTA alone.

**Reframe** (an unexpected result of candidate-fetching today,
the companion follow-ups note §1): most less-studied UniProt entries are
**TrEMBL (`tr|`, unreviewed)**, which makes them unsuitable as a
specificity ground-truth (cannot distinguish "model under-confident on
obscure sequence" from "model correctly flagging an annotation
problem"). The candidates that exist as **reviewed Swiss-Prot (`sp|`,
manually curated)** but are not in the well-known panel are typically
**species-shifted homologues** - a known protein family in a
less-frequently-trained organism. So this experiment measures
**species-shifted-benign** specificity rather than literal "obscure" -
which is actually the deployment-relevant regime (a curation pipeline
will mostly see species-shifted entries, not novel hypotheticals).

## 2. Design

Three reviewed sp| proteins from less-cited organisms,
**matched arm only** (n=20 each = **60 calls**, claude-opus-4-7).

| id | UniProt | protein / organism | length |
|---|---|---|---|
| **PONAB_RMD3** | Q5R6Z1 | Regulator of microtubule dynamics 3 / Pongo abelii (orangutan) | 470 aa |
| **STRPN_RECR** | P0CB76 | DNA repair / recombination RecR / S. pneumoniae TIGR4 | 198 aa |
| **LEIME_TIM** | P48499 | Triosephosphate isomerase / Leishmania mexicana | 251 aa |

All three: reviewed Swiss-Prot, evidence level PE=1 or 2, known
biochemistry. The host human/canonical homologues (RMDN3, TIM/TPI1) are
well-trained; these specific species variants are not. Each carries a
factually-verified annotation (descriptions assembled from the UniProt
entry's curated function/structure fields).

**Matched arm only.** The obscurity question is about *specificity*
(does correct-label MATCH-rate hold under weak recognition?), not
sensitivity. Wrong-swap is omitted to halve cost; the swap rotation is
defined in the JSON so the same script can run both arms if later
needed.

Prompt and scoring identical to XP4-spec (`PROTOCOL_XP4_SPEC.md` §3,
§5) - neutral curation prompt, content-verdict + stop_reason recorded
separately.

## 3. Hypotheses

- **HX4so-specificity-holds.** matched MATCH-rate ≥ 90% on all three
  species-shifted proteins (replicates XP4-spec's 100% in the
  lower-recognition regime).
- **HX4so-uncertain-shift.** *If* MATCH-rate drops, it shifts to
  UNCERTAIN rather than MISMATCH - the model expresses calibrated lack
  of confidence rather than fabricating a mismatch. UNCERTAIN at any
  rate > 5% is a real, interpretable finding (not a failure).
- **HX4so-norefuse.** Refusal rate ≈ 0 (no hazardous content).

## 4. Decision rules

- All three ≥ 90% MATCH -> specificity is regime-general; XP4-spec's
  100% number extends to less-recognized benign material.
- One or more cells with UNCERTAIN > 10% -> the model calibrates
  confidence rather than fabricating; report as the more nuanced
  picture of the integrity capability.
- Any cell with MISMATCH > 10% on a clean annotation -> either the
  annotation has a hidden error (audit the relevant UniProt entry as
  in the companion stimulus audit §1 for barnase) or the model is genuinely
  over-flagging on weak-recognition sequences.

## 5. Safety framing

Budget = 0. All three sequences are reviewed public UniProt entries;
all three annotations are factual descriptions derived from the same
entries. No hazardous content; refusal not expected.

## 6. Files

- Pre-registration: this file
- Stimuli: `stimuli/xp4spec_obscure_proteins.json` (committed with this
  protocol)
- Script: `src/label_integrity_spec.py` (extended with `--stim-file`
  and `--conditions` arguments; the original 5-protein xp4spec arm is
  unchanged when called without those args)
- Results: `results/label_integrity_spec_obscure.json` + console
- Run:
  ```bash
  python src/label_integrity_spec.py \
    --models claude-opus-4-7 --n 20 \
    --stim-file stimuli/xp4spec_obscure_proteins.json \
    --conditions matched \
    --out results/label_integrity_spec_obscure.json
  ```

## Amendment - verbatim-UniProt arm (removes the hand-authoring confound)

The first obscure run (`ANALYSIS_XP4_SPEC_OBSCURE.md`) was confounded: the
apparent 51.7% specificity was a 4th hand-annotation error (RMD3 length
487 vs 470), not a model property. This amendment re-runs the obscurity
question with **verbatim-UniProt annotations** - every claim sourced from
the curated entry (RecName / OS / CC function-catalytic-family lines), with
**no hand-authored length, residue, or mechanism claims** (the only author
error surface).

Stimuli: `stimuli/xp4spec_verbatim_proteins.json` - 4 reviewed-Swiss-Prot
proteins from less-cited organisms (RMDN3 orangutan Q5R6Z1, RecR
S. pneumoniae P0CB76, TIM Leishmania P48499, CoaBC M. jannaschii Q58323),
matched + wrong-swap, n=20, Opus 4.7 (160 calls).

**HX4v-clean-specificity.** With verbatim-correct annotations, matched
MATCH-rate returns to ≥ 90% even on weakly-recognized sequences - i.e. the
obscurity does not by itself induce over-flagging; the earlier drop was
author error. **HX4v-sensitivity.** wrong-swap MISMATCH ≥ 90% (benign-benign
mislabels still caught). Prediction: RMD3v and TIMv (which over-flagged with
hand annotations) now return MATCH.

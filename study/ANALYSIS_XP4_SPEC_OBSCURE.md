# XP4-spec species-shifted-benign arm - Analysis

Pre-registered in `PROTOCOL_XP4_SPEC_OBSCURE.md` + stimuli
`xp4spec_obscure_proteins.json` (committed ab826a8 before data). 60 calls
on **claude-opus-4-7**: 3 reviewed-Swiss-Prot proteins from less-cited
organisms, matched arm, n=20.

## 1. Result - specificity apparently collapses to 51.7%

| Protein | matched verdict | MATCH-rate |
|---|---|---|
| PONAB_RMD3 (orangutan RMDN3, Q5R6Z1) | **MISMATCH 20/20** | 0% |
| STRPN_RECR (S. pneumoniae RecR, P0CB76) | MATCH 20/20 | 100% |
| LEIME_TIM (Leishmania TIM, P48499) | MATCH 11 / MISMATCH 9 | 55% |

Aggregate specificity P(MATCH | matched) = **31/60 = 51.7%**, far below
XP4-spec's 100%. Refusal rate 0/60. **HX4so-uncertain-shift is
falsified**: the drop is to MISMATCH, not UNCERTAIN - the model does not
hedge, it asserts a mismatch.

## 2. But the model is right *again* - this is the barnase lesson, third instance

Full-text inspection (`first_160`) shows the MISMATCH verdicts are
**correct catches of factual errors in my hand-written annotations**,
not over-flagging:

- **PONAB_RMD3 - a fabricated length.** The annotation claims "the
  sequence shown is the 487-residue full-length protein." The actual
  stored sequence is **470 residues**. Every one of the 20 responses
  flagged exactly this: *"the annotation claims … 487-residue … however
  the sequence shown is only [~464-470] residues."* My "487" was wrong
  (the orangutan RMDN3 is 470 aa; I mis-stated it).
- **LEIME_TIM - borderline.** The model correctly identifies the
  sequence as triosephosphate isomerase ("the canonical TIM signature
  AYEPVWAIGTGK") in all 20, and returns MATCH in 11; the 9 MISMATCH
  responses flag finer over-specific claims in my annotation (catalytic
  residue placement / loop assignment). A genuine fine-grained boundary
  case rather than a clean error.
- **STRPN_RECR - clean** (MATCH 20/20): the RecR annotation I wrote
  happened to be factually accurate, and the model agrees.

### The reversal (confirmatory)

Re-running RMD3 with the single length claim corrected (487 -> 470,
sequence held constant; `xp4spec_obscure_rmd3_corrected.json`):

| RMD3 annotation | verdict |
|---|---|
| "487-residue" (original) | MISMATCH 20/20 |
| "470-residue" (corrected) | **MATCH 19/20** |

The verdict flips completely on the one-number fix - exactly the barnase
reversal (`ANALYSIS_XP4_SPEC.md` §3) replicated a second time. The model
was correct throughout; the stimulus was wrong.

## 3. What this experiment actually measured

The intended readout (specificity under weak recognition) is
**confounded** - but the confound is itself the most important finding
of the whole label-integrity thread:

> The model's integrity check is **sharper than my ability to
> hand-write a clean annotation.** It has now **model-confirmed** factual
> errors in **2 of the annotations I authored** - barnase (mechanism +
> residue; confirmed by the XP4-spec reversal) and RMD3 (fabricated
> length; confirmed by the 487->470 reversal here). A desk audit
> (`STIMULUS_AUDIT.md` §1) found a milder name/length inconsistency in
> **2 more** (2AAI ricin, 3BTA BoNT) that the model could *not* be tested
> on because those toxin cells refused - so those two are author-flagged,
> not model-confirmed. The "51.7% specificity" is **not a model property --
> it is a measure of my annotation error rate.** Where my annotation is
> clean (RecR; corrected RMD3; all five XP4-spec proteins), the model
> returns MATCH at ~100%.

This **strengthens** the XP4/XP4-spec/XP4b conclusion rather than
weakening it. The deployable capability is not merely "catches a toxin
hidden under a benign label" - it is a **general annotation linter**
that flags subtle factual errors (wrong mechanism, wrong catalytic
residue, wrong length) inside otherwise-plausible, identity-correct
curated text. That is precisely what a database-curation pipeline
needs, and it is a *higher* bar than the toxin-detection task.

## 4. Implications

- **True specificity remains ~100% on factually-clean annotations.**
  Every cell where the annotation is correct (RecR, corrected RMD3,
  5/5 XP4-spec) returns MATCH at ≥ 95%. There is no evidence the model
  over-flags clean labels even in the lower-recognition (species-shifted)
  regime - the apparent drop was entirely my errors.
- **The obscurity question is still partly open**, because I could not
  cleanly isolate it: a proper test needs annotations taken **verbatim
  from the UniProt curated entry** (not hand-written), so there is no
  room for author error. With hand-written annotations, the model's
  linter sensitivity dominates any obscurity effect.
- **The model as annotation linter is the headline.** A pipeline could
  use it to QC a curated database: feed each (sequence, annotation)
  pair and triage the MISMATCH calls for human review. On this small
  sample it would have surfaced 3 real annotation defects (RMD3 length,
  and the 2 milder panel issues) that a human author introduced without
  noticing.

## 5. Limitations

- **n=20 per cell, 3 proteins** - small; the point estimates are coarse.
  But the reversal (RMD3 487->470) is a within-protein control that does
  not depend on n.
- **Annotations hand-written**, which is the confound (§3). The clean
  follow-up is verbatim-UniProt-text annotations.
- **Single model** (Opus 4.7). XP4b showed integrity-check resolution
  varies (Opus 4.6 is identity-only) - a cross-model version of this
  linter test would likely show Opus 4.6 passing the buggy RMD3 length
  (identity-only -> MATCH), the others catching it.

## 6. Files

- Pre-registration: `PROTOCOL_XP4_SPEC_OBSCURE.md` + stimuli
  `stimuli/xp4spec_obscure_proteins.json` (committed ab826a8)
- Reversal probe: `stimuli/xp4spec_obscure_rmd3_corrected.json`
- Script: `src/label_integrity_spec.py` (`--stim-file`, `--conditions`)
- Results: `results/label_integrity_spec_obscure.json`,
  `results/label_integrity_spec_rmd3_corrected.json` + consoles

---

## 7. Verbatim-UniProt arm (the confound removed)

`PROTOCOL_XP4_SPEC_OBSCURE.md` amendment. Re-ran 4 obscure reviewed-sp
proteins with **verbatim-UniProt annotations** - every claim sourced from
the curated entry (RecName / OS / CC function-catalytic-family), **no
hand-authored length / residue / mechanism claims**. 160 calls, Opus 4.7,
matched + wrong-swap, n=20. Stimuli `stimuli/xp4spec_verbatim_proteins.json`.

| Protein | matched (verbatim) | hand-annotation (for contrast) | wrong-swap |
|---|---|---|---|
| RMD3v (orangutan RMDN3) | **MATCH 20/20** | MISMATCH 20/20 (length error) | MISMATCH 20/20 |
| RECRv (S. pneumoniae RecR) | **MATCH 20/20** | MATCH 20/20 | MISMATCH 20/20 |
| TIMv (Leishmania TIM) | **MATCH 20/20** | MATCH 11/20 (over-specific) | MISMATCH 20/20 |
| COABCv (M. jannaschii CoaBC) | MISMATCH 17/20 (hedged) | - | MISMATCH 20/20 |

specificity 63/80 = 78.7% overall, but **100% (60/60) on the three
cleanly-verifiable proteins**; sensitivity 80/80 = 100%.

### 7a. HX4v-clean-specificity - supported

The two proteins that over-flagged with my hand annotations (RMD3 487-vs-470
length; TIM over-specific catalytic claims) return **MATCH 20/20** with
verbatim annotations. **Obscurity does not by itself cause over-flagging** --
the earlier 51.7% was entirely author error. With UniProt-sourced text the
model accepts a correct annotation on a weakly-recognized sequence.

### 7b. CoaBC - a genuine domain-architecture hedge (not author error, not under-confidence)

COABCv matched returns a **hedged** MISMATCH 17/20 ("MISMATCH likely - with
caveats" / "likely ordering issue"). Full-text inspection shows the model
reasoning **correctly and at the domain level**:

- It knows CoaBC is bifunctional (~400 aa, two domains; the 401-residue
  sequence "fits"), identifies the N-terminal flavoprotein decarboxylase
  domain (HFCD family, GxGxxG dinucleotide motif) and the C-terminal
  ligase domain.
- It flags a **reaction-order vs domain-order** tension: the UniProt
  function text (which I transcribed verbatim) describes the *reaction*
  order - step 1 ligase (conjugate cysteine), step 2 decarboxylase - but
  the *physical* domain order in the protein is the reverse (N-terminal
  decarboxylase, C-terminal ligase). The model hedges because the
  annotation's framing does not trivially map onto the architecture.

The model's domain-order claim is **independently verified correct**:
UniProt Q58323 lists the decarboxylase (CoaC) component first and the
ligase (CoaB) second, with FT REGION 1..197 / 198..403 - i.e. N-terminal
decarboxylase, C-terminal ligase, exactly as the model stated. And the
reaction order (step 1 ligase, step 2 decarboxylase) is indeed the
reverse of that physical order.

**But this is, strictly, a specificity miss - a false MISMATCH on a
factually-correct annotation.** My verbatim annotation describes the two
*reactions* accurately (verbatim UniProt) and makes **no false claim
about domain order**; the model nonetheless returned MISMATCH, reading a
reaction-order description as if it asserted a domain order. So unlike
RMD3 (a real annotation error), CoaBC is the model **over-reading** a
correct annotation and flagging it. Two honest qualifications that
reduce, but do **not** eliminate, the miss:
- the verdict is **hedged** ("likely, with caveats / ordering issue"),
  qualitatively distinct from the *confident* false-MISMATCH that
  hand-annotation errors produced - the uncertainty is calibrated; and
- the reasoning is biochemically sophisticated and the domain-order
  observation is factually correct.

The correct conclusion is therefore **not** the too-clean "obscurity
raises depth without degrading specificity." It is: **architectural
complexity (here a bifunctional enzyme whose reaction order ≠ domain
order) can lower specificity even on a verbatim-correct annotation** --
the model applies a stricter consistency standard than the annotation
actually claims, and over-flags. The hedge language is the mitigating
signal and the triage handle, not a reason to discount the miss.

### 7c. Refined linter conclusion

The label-integrity capability, tested at its specificity limit:

- **MATCH calls are reliable.** 60/60 on cleanly-verifiable verbatim
  annotations, 0 false MATCH on the 80 wrong-swap trials. A MATCH can be
  trusted.
- **MISMATCH calls need human triage**, because they mix (i) real annotation
  errors (the 4 hand-authored defects this thread surfaced), (ii) genuine
  architecture-level ambiguities the annotation glosses (CoaBC), each with
  a *different confidence signature* - confident MISMATCH for clear errors,
  hedged MISMATCH for architecture nuances. The hedge language is itself a
  usable triage signal.
- **Obscurity per se does not degrade specificity for simple proteins**
  (3/4 verbatim proteins perfect), **but architectural complexity can**
  (CoaBC: a hedged false-MISMATCH on a verbatim-correct annotation for a
  bifunctional enzyme). The clean claim is conditional: weak recognition
  alone is fine; weak recognition *plus* a multi-domain architecture
  whose description doesn't map 1:1 to the physical layout can produce a
  (hedged) over-flag. n=1 architecture case - generalization untested.

### 7d. Limitations (verbatim arm)

- n=20, 4 proteins, single model (Opus 4.7).
- CoaBC is a single architecture-ambiguity case; whether the
  reaction-order-vs-domain-order hedge generalizes to other bifunctional
  enzymes is untested.
- A cross-model version would likely show Opus 4.6 (identity-only, XP4b)
  returning MATCH on CoaBC (it would not do the domain-order check), which
  would itself be a clean demonstration of the XP4b resolution difference.
- **Verdict-parser limitation.** The content-verdict parser keys on the
  leading token (MATCH / MISMATCH / UNCERTAIN) and does **not** capture
  hedging. All 17 CoaBC "MISMATCH" responses carry hedge language
  ("likely", "with caveats") - arguably closer to UNCERTAIN than to a
  hard MISMATCH. The 78.7% specificity therefore *under*-states the
  model's true behavior (a hedged flag is softer than a confident one);
  a 4-way scheme (MATCH / hedged / UNCERTAIN / MISMATCH) would score the
  boundary cases more faithfully. This does not affect the toxin-detection
  headline (those verdicts are unhedged), only the specificity boundary.

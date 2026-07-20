# Paper-Aligned Formulation Scoring (Nature Communications 2026 CMLase Context)

This rubric converts formulation records into a comparable score using the evidence priorities implied by:

- Enzymatic CML reversal efficacy in tissue/protein systems.
- Preservation of protein integrity (repair without protein damage).
- Stability and delivery practicality for translational use.

Primary paper context:
- Trabosh N. et al., Nature Communications (2026), DOI: 10.1038/s41467-026-75141-2.

## 1. Scoring Overview

Total score is 0-100 points:

- 40 points: Efficacy proxy alignment (CML reversal readiness)
- 25 points: Enzyme integrity and storage stability
- 20 points: Delivery and tissue access plausibility
- 15 points: Formulation/process deployability

Because current `formulation_record` schema does not contain direct ex vivo CML reduction measurements, this rubric uses explicit proxy signals from formulation and stability fields.

## 2. Field Mapping to `formulation_record.schema.json`

### A. Efficacy Proxy Alignment (0-40)

Mapped fields:
- `enzyme_module.activity_u_per_g`
- `enzyme_module.enzyme_fraction_w_w`
- `enzyme_module.encapsulation_type`
- `on_skin_targets.target_ph_min`
- `on_skin_targets.target_ph_max`
- `on_skin_targets.target_contact_time_min`

Subscores:
1. Enzyme activity strength (0-15)
2. Enzyme dose adequacy (0-10)
3. pH alignment window (0-10)
4. Contact-time sufficiency (0-5)

Suggested thresholds:
- Activity: 50 U/g or greater -> 15; 25-49 -> 10; 10-24 -> 5; else 0.
- Fraction: 0.005 w/w or greater -> 10; 0.002-0.0049 -> 6; below -> 2.
- pH: fully inside 5.8-6.2 -> 10; partial overlap -> 5; no data -> 0.
- Contact time: 480 min or greater -> 5; 240-479 -> 3; below -> 1.

### B. Enzyme Integrity and Stability (0-25)

Mapped fields:
- `stability_profile.retained_activity_pct`
- `stability_profile.conditions.temperature_c`
- `stability_profile.conditions.duration_days`
- `stability_profile.physical_status`
- `stabilization_system.trehalose_pct`
- `stabilization_system.methionine_pct`
- `stabilization_system.edta_pct`

Subscores:
1. Retained activity under storage (0-15)
2. Stability duration at reported condition (0-5)
3. Physical compatibility status (0-3)
4. Presence of protection system (0-2)

Suggested thresholds:
- Retained activity: 80 percent or greater -> 15; 70-79 -> 11; 60-69 -> 7; below -> 3.
- Duration: 90 days or greater -> 5; 60-89 -> 3; 30-59 -> 2; below -> 1.
- Physical status: stable -> 3; unknown -> 1; separation/precipitation/shift -> 0.
- Protection system: any 2 of trehalose, methionine, EDTA present at non-zero -> 2; one present -> 1; none -> 0.

### C. Delivery and Tissue Access Plausibility (0-20)

Mapped fields:
- `format`
- `delivery_support.penetration_enhancers[]`
- `delivery_support.ecm_targeting_motif`
- `enzyme_module.encapsulation_type`
- `components[].role`

Subscores:
1. Delivery architecture quality (0-8)
2. Tissue access support features (0-7)
3. Encapsulation and enzyme shielding (0-5)

Suggested thresholds:
- Architecture: dual_chamber_cream -> 8; gel_cream or serum -> 5; single_phase_cream -> 3.
- Access support: enhancer present + ECM motif present -> 7; either one -> 4; none -> 1.
- Encapsulation: liposome/niosome/supramolecular -> 5; other -> 3; none -> 1.

### D. Deployability and Process Control (0-15)

Mapped fields:
- `process_controls.cold_process_preferred`
- `process_controls.max_enzyme_addition_temp_c`
- `process_controls.mixing_shear`
- `process_controls.packaging`
- `components[]`

Subscores:
1. Enzyme-safe process controls (0-8)
2. Packaging practicality (0-4)
3. Composition completeness and role coverage (0-3)

Suggested thresholds:
- Process controls: cold process true + max addition temp <=35C + low shear -> 8; partial -> 4; missing -> 1.
- Packaging: dual_chamber/reconstituted -> 4; single_chamber -> 2; other -> 1.
- Role coverage: solvent + enzyme_active + stabilizer + preservative present -> 3; three roles -> 2; below -> 1.

## 3. Composite Formula

Let:
- E = efficacy proxy subscore (0-40)
- S = stability subscore (0-25)
- D = delivery subscore (0-20)
- P = deployability subscore (0-15)

Then:

Score = E + S + D + P

Range is 0-100.

Decision bands:
- 85-100: Lead formulation candidate
- 70-84: Backup candidate, optimize one major gap
- 55-69: Experimental candidate, multiple gaps
- below 55: Do not prioritize

## 4. Example Application in Current Repository

Using `examples/formulation_record.example.json`:
- High retained activity and long refrigerated duration support strong S score.
- Dual chamber format, encapsulation, and delivery support provide strong D score.
- Process controls and packaging fields support strong P score.
- Enzyme activity/dose and on-skin targeting fields support moderate-to-strong E score.

Using `examples/formulation_record.minimal.valid.json`:
- Limited fields reduce E, D, and P confidence.
- Stability is acceptable but shorter duration and sparse controls lower overall score.

Resulting interpretation: the dual-chamber example should rank above the minimal valid example under this rubric.

## 5. Schema Gap Notes for Future Upgrades

To align even more directly with the paper's endpoint style, consider optional future fields:
- `ex_vivo_outcomes.cml_reduction_pct`
- `ex_vivo_outcomes.protein_integrity_preserved`
- `ex_vivo_outcomes.tissue_type`
- `ex_vivo_outcomes.assay_method`
- `ex_vivo_outcomes.reference_age_context`

These are not required for current scoring and can be added in a backward-compatible schema revision.
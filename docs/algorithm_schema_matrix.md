# Algorithm-to-Schema Matrix

This matrix maps algorithm families to the current repository schemas and required fields for model-ready features.

Machine-readable source of truth: schemas/algorithm_field_requirements.json.

## 1. Variant-Centric Algorithms

| Algorithm Family | Primary Task | Required Schema | Required Fields | Derived Features (Minimal) |
|---|---|---|---|---|
| Sequence alignment (Needleman-Wunsch, Smith-Waterman) | Conservation and mutation burden | variant_record | sequence, mutations, parent_scaffold_id | position-wise conservation score, substitution class, cumulative mutation load |
| Graph/network on residue contacts | Hot-spot and interaction network scoring | variant_record | sequence, mutations | residue centrality proxy, mutational neighborhood density |
| Supervised sequence-to-function models | Predict activity/selectivity/stability | variant_record + assay_result | variant_id, sequence, mutations, predicted_scores; assay measurements and conditions | sequence embeddings, mutation encoding, condition-adjusted targets |
| Bayesian optimization / bandits | Next variant proposal under uncertainty | variant_record + assay_result | variant_id, design_round, predicted_scores.uncertainty, assay measurements | posterior mean/variance, expected improvement, round-aware exploration term |
| Clustering / dimensionality reduction | Landscape interpretation and diversity selection | variant_record + assay_result | sequence, mutations, measurements.kcat_over_km, measurements.off_target_index | latent embeddings, standardized assay vectors |

## 2. Assay and Kinetics Algorithms

| Algorithm Family | Primary Task | Required Schema | Required Fields | Derived Features (Minimal) |
|---|---|---|---|---|
| Kinetic regression and multitask learning | Joint prediction of efficacy and selectivity | assay_result | assay_type, conditions.temperature_c, conditions.ph, measurements.kcat, measurements.km, measurements.kcat_over_km, measurements.off_target_index | condition-normalized kinetics, assay-type one-hot, QC mask |
| Batch-effect correction and calibration | Stabilize model training across rounds | assay_result | batch_id, timestamp, qc.passed, measurements | batch random-effect term, time drift term, QC-weighted loss |
| Outlier and QC-aware filtering | Data integrity for retraining | assay_result | qc.passed, qc.notes, measurements, conditions | robust z-score flags, replicate consistency index |

## 3. Formulation Algorithms

| Algorithm Family | Primary Task | Required Schema | Required Fields | Derived Features (Minimal) |
|---|---|---|---|---|
| Gradient-free multi-objective optimization (CMA-ES, BO) | Maximize retained activity with physical stability | formulation_record + assay_result | components, stability_profile.retained_activity_pct, stability_profile.physical_status, format; assay_type=formulation_compatibility | composition vector, stability penalty, Pareto rank |
| Time-dependent decay models | Estimate shelf-life and use-window | formulation_record | stability_profile.conditions.temperature_c, stability_profile.conditions.duration_days, stability_profile.retained_activity_pct | decay rate constants, projected retention horizon |
| Compatibility classification | Excipient inclusion/exclusion | formulation_record | components.name, components.role, stability_profile.physical_status, retained_activity_pct | role-wise compatibility scores, incompatibility signatures |

## 4. Translational and Clinical Planning Algorithms

| Algorithm Family | Primary Task | Required Schema | Required Fields | Derived Features (Minimal) |
|---|---|---|---|---|
| Rule-based decision trees | Gate progression and exclusion logic | variant_record + assay_result + formulation_record | predicted_scores, measurements.off_target_index, retained_activity_pct, physical_status | pass/fail gate flags, traceable decision path |
| Risk and time-to-event models (future clinical layer) | Responder and risk estimation | current schemas as upstream evidence source | aggregated variant efficacy and stability profiles by candidate | candidate-level priors, uncertainty intervals |
| Explainability and monitoring | Governance and drift detection | all schemas | provenance.model_version, feature_set_version, batch_id, timestamp | drift metrics, calibration curves, model-card slices |

## 5. Minimal Training Views

Define these normalized views for consistent model ingestion:

1. variant_feature_view
- Source: variant_record
- Key columns: variant_id, design_round, sequence_embedding, mutation_vector, predicted_scores.*

2. assay_feature_view
- Source: assay_result
- Key columns: assay_id, variant_id, assay_type, temperature_c, ph, kcat, km, kcat_over_km, off_target_index, qc_passed, batch_id

3. formulation_feature_view
- Source: formulation_record
- Key columns: formulation_id, variant_id, format, component_vector, retained_activity_pct, physical_status, temperature_c, duration_days

## 6. Coverage Gaps to Track

Current schemas are sufficient for baseline modeling but optional fields may be added later for stronger graph and clinical workflows:

- Explicit structure-derived contact-map references per variant.
- Replicate identifiers and replicate-level assay measurements.
- Standardized explant or omics outcome linkage IDs.
- Candidate-level aggregation schema for translational risk models.

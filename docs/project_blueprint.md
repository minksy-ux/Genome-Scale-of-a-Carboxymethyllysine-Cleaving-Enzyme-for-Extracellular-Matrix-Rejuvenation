# Project Blueprint: CMLase-ECM

## 1. System Definition

### Objective
Create a reproducible design-and-formulation pipeline for CML-cleaving oxidase variants suitable for ECM-focused topical deployment.

### Inputs
- Oxidase scaffold sequences and structures (experimental or predicted).
- Historical mutational and assay data.
- Formulation compatibility constraints.
- Skin-delivery constraints (pH, diffusion, retention, and activity lifetime).

### Outputs
- Prioritized variant list with uncertainty estimates.
- Iteratively updated sequence-function model.
- Topical architecture package for lead candidates.

## 2. Modular Pipeline

Algorithm references for each module are defined in `docs/algorithms_framework.md`.

## Module A: Scaffold Discovery
- Build a seed set around CrGO-like scaffolds and close oxidase homologs.
- Triaging criteria:
  - Active-site geometry consistency with CML-oriented substrate pose.
  - Fold stability risk score.
  - Predicted function-preserving mutability around the binding pocket.

Deliverable: scaffold panel with confidence-ranked annotations.

## Module B: AI-Guided Sequence Proposal
- Feature categories:
  - Sequence embeddings.
  - Structure-aware residue environments.
  - Pocket electrostatics and substrate-contact descriptors.
  - Developability predictors (solubility, aggregation tendencies).
- Model stack (example):
  - Surrogate regressor for activity/selectivity.
  - Classifier for likely loss-of-function variants.
  - Bayesian acquisition to balance exploitation and exploration.

Deliverable: ranked mutation proposals and library design.

## Module C: Directed Evolution Data Loop
- Execute round-based variant evaluation.
- Collect standardized assay outputs and attach full metadata.
- Retrain model after each round with strict data versioning.

Deliverable: convergence curves for activity/selectivity/stability.

## Module D: Formulation and Delivery Co-Optimization
- Evaluate candidate resilience in prototype creams/gels.
- Track activity decay under storage and simulated use conditions.
- Run ECM-access proxy tests (binding, retention, diffusion balance).

Deliverable: formulation recommendation for each lead variant.

## 3. Candidate Decision Gates

### Gate 1: Biocatalysis
- Activity threshold on peptidyl-CML substrates.
- Selectivity threshold vs non-CML lysine contexts.
- Reproducibility across replicate runs.

### Gate 2: Skin-Relevant Robustness
- Retained activity across pH 5.0-7.0.
- Compatible with selected excipient set.
- No major red-flag in developability models.

### Gate 3: Formulation Performance
- Prespecified retained activity after accelerated stability test windows.
- Sufficient release/retention profile in ECM-mimetic systems.

## 4. Metrics Framework
- Catalysis:
  - kcat, Km, and kcat/Km on target and off-target substrates.
  - Product-confirmation ratios from orthogonal analytics.
- Stability:
  - Residual activity (%) after stress exposures.
  - Aggregation or precipitation index.
- Delivery:
  - Fraction active after formulation processing.
  - Estimated local residence proxy in ECM-relevant matrices.

## 5. Data Governance
- Every record gets immutable IDs:
  - Candidate ID, variant ID, assay ID, batch ID, formulation ID.
- Provenance fields required for all model training inputs.
- Use schema validation as a hard precondition for training jobs.

## 6. Risk Register (Initial)
- Off-target lysine chemistry risk.
- Enzyme inactivation in real formulation matrix.
- Incomplete ECM access due to barrier limitations.
- Batch-to-batch assay variance causing model drift.

Mitigation pattern:
- Pair primary assay with orthogonal confirmation.
- Include uncertainty-aware selection criteria.
- Maintain negative and matrix-interference controls every round.

## 7. Suggested Milestones
1. M0: Build scaffold panel and baseline model.
2. M1: Complete first AI-guided screening loop.
3. M2: Demonstrate improved selectivity and pH robustness.
4. M3: Nominate lead plus backup with formulation compatibility evidence.
5. M4: Freeze versioned development package for downstream teams.

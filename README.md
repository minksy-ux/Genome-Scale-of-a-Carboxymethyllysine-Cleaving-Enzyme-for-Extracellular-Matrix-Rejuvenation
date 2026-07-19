# Genome-Scale Design of a Carboxymethyllysine-Cleaving Enzyme for ECM Rejuvenation

Open, implementation-oriented framework for designing, optimizing, and formulating CML-cleaving enzymes for extracellular matrix (ECM) rejuvenation in skin.

## Scope

This repository defines a modular pipeline that links:

1. Structure-guided scaffold discovery.
2. AI-guided sequence optimization.
3. Directed evolution data loops.
4. Topical formulation and delivery constraints.
5. Standardized data schemas for reproducibility and model retraining.

The target outcome is a lead candidate class called CMLase-ECM: an oxidase-derived enzyme with high selectivity for peptidyl-CML over unmodified lysine, robust activity in skin-relevant pH, and compatibility with topical formulations.

## Why CML in ECM

Long-lived proteins (collagen, elastin) accumulate CML adducts over decades, contributing to:

- Matrix stiffening and altered biomechanics.
- RAGE-associated inflammatory signaling.
- Age-associated and diabetic tissue dysfunction.

Recent engineered oxidase work suggests peptidyl-CML can be selectively processed and that lysine-state restoration is chemically feasible in biological matrices. This project generalizes that concept to a genome-scale discovery-to-formulation platform.

## Repository Layout

- docs/project_blueprint.md: End-to-end design and execution strategy.
- docs/algorithms_framework.md: Core CS + biomedical ML algorithm map for design through clinical planning.
- docs/algorithm_schema_matrix.md: Compact map from algorithm families to required schema fields and model-ready views.
- docs/topical_cream_architecture.md: Concrete cream architecture and delivery model.
- docs/conceptual_cmlase_formulation.md: Research-stage CMLase topical formulation rationale and module design.
- docs/chemical_formula_reference.md: Molecular formula appendix for major compounds in the CMLase concept.
- docs/protocols.md: High-level, implementation-ready protocol templates.
- docs/pseudocode.md: Pseudocode for active learning, selection planning, and lead down-selection.
- schemas/variant_record.schema.json: Schema for variant-level sequence and assay metadata.
- schemas/assay_result.schema.json: Schema for assay output ingestion.
- schemas/formulation_record.schema.json: Schema for formulation stability/performance tracking.
- schemas/algorithm_field_requirements.json: Machine-readable algorithm-to-field contract for preflight training validation.
- examples/formulation_record.example.json: Example formulation payload compatible with the formulation schema.
- examples/formulation_record.minimal.valid.json: Minimal valid payload for schema smoke tests.
- examples/formulation_record.intentionally.invalid.json: Intentionally invalid payload for negative validator tests.
- scripts/validate_formulation_examples.py: Dependency-free smoke validator for formulation example payloads.

## Design Targets for CMLase-ECM

Primary targets:

- High catalytic efficiency on CML-modified collagen/elastin fragments at 25-37 C.
- Strong discrimination for peptidyl-CML vs native lysine-containing peptides.
- Activity retention across pH 5.0-7.0.
- Formulation resilience to standard cosmetic excipients.
- Preliminary developability profile (aggregation risk, expression feasibility, low predicted immunogenicity drift from natural homologs).

Secondary targets:

- Shelf stability >= 6 months at 2-8 C (stretch: room temperature).
- Tunable ECM residence through optional ECM-binding motifs.

## Practical Workflow

1. Build a scaffold panel from oxidase families and homologs with compatible active-site geometry.
2. Select algorithm stack by phase (alignment/graphs, supervised predictors, Bayesian or bandit selection, clustering).
3. Run a preflight check against schemas/algorithm_field_requirements.json before model training.
4. Generate variant libraries constrained by structural plausibility and sequence naturalness.
5. Run iterative active-learning cycles combining computational scoring with high-throughput assay outcomes.
6. Optimize formulation and delivery in parallel with biocatalytic optimization.
7. Freeze a versioned lead package containing sequence, activity profile, and formulation dossier.

See docs/project_blueprint.md, docs/algorithms_framework.md, and docs/algorithm_schema_matrix.md for details.

## Data Interoperability

All experimental and model outputs should be captured using JSON records validated against repository schemas in schemas/.

Recommended storage pattern:

- Immutable raw records (append-only).
- Versioned transformed feature tables.
- Reproducible model training manifests.

Validation fixtures:

- Use examples/formulation_record.minimal.valid.json as a pass-case for schema validators.
- Use examples/formulation_record.intentionally.invalid.json as a fail-case to confirm error handling.

Quick smoke test:

- Run python3 scripts/validate_formulation_examples.py to verify expected pass/fail behavior for included examples.

## Safety and Use Boundaries

- This repository is for research and development planning.
- It is not a medical product dossier and not clinical guidance.
- Any translational or human-use work requires full regulatory, toxicology, dermatology, and manufacturing review.

## Next Implementation Steps

1. Add baseline candidate/homolog data files and structure metadata.
2. Implement schema validation in CI.
3. Add benchmark notebooks/scripts for candidate prioritization.
4. Integrate laboratory data export templates to close the active-learning loop.

# Protocol Templates (Implementation-Oriented)

These are high-level protocol templates intended for reproducible R&D planning and data capture.

## 1. In Silico Scaffold Triage Protocol

### Purpose
Prioritize oxidase scaffolds for CML-focused optimization.

### Inputs
- Candidate sequences.
- Structure files or predicted models.
- Active-site annotation references.

### Procedure (High-Level)
1. Standardize sequence IDs and structure metadata.
2. Compute structure quality and pocket descriptors.
3. Compare active-site geometry against known CML-compatible motifs.
4. Score candidates using weighted multi-criteria ranking.
5. Export top panel and rationale log.

### Required Outputs
- Ranked scaffold table.
- Machine-readable score components.
- Exclusion log for discarded candidates.

## 2. Variant Proposal Protocol (AI Round)

### Purpose
Generate mutation libraries balancing predicted gain and uncertainty.

### Inputs
- Current round training dataset.
- Sequence constraints (naturalness/immunogenicity heuristics).
- Library budget constraints.

### Procedure (High-Level)
1. Train or refresh surrogate models.
2. Generate candidate mutations under structural and sequence constraints.
3. Predict activity/selectivity/stability and uncertainty.
4. Select library by acquisition policy and diversity constraints.
5. Register proposal manifest for wet-lab execution.

### Required Outputs
- Ranked proposal list.
- Diversity and uncertainty summary.
- Round manifest with reproducible model version references.

## 3. Assay Data Ingestion Protocol

### Purpose
Capture variant performance in standardized format for retraining.

### Inputs
- Raw assay files.
- Batch metadata.
- QC thresholds.

### Procedure (High-Level)
1. Parse assay files and harmonize units.
2. Attach metadata (date, operator, batch, controls).
3. Validate records against repository schemas.
4. Flag outliers and QC failures without deleting raw data.
5. Publish curated dataset snapshot with immutable version tag.

### Required Outputs
- Validated assay JSON/CSV.
- QC report.
- Model-ready feature matrix snapshot.

## 4. Formulation Compatibility Screen Protocol

### Purpose
Identify excipient sets that preserve catalytic activity.

### Inputs
- Lead variant panel.
- Candidate excipient matrix.
- Storage condition matrix.

### Procedure (High-Level)
1. Prepare predefined condition matrix.
2. Expose enzyme panel to each condition.
3. Measure retained activity at multiple timepoints.
4. Fit decay profiles and classify compatibility bands.
5. Recommend formulation shortlist.

### Required Outputs
- Compatibility matrix.
- Activity decay parameters.
- Excipients inclusion/exclusion recommendation list.

## 5. Lead Nomination Protocol

### Purpose
Nominate lead and backup variants with complete evidence package.

### Decision Inputs
- Catalytic performance.
- Selectivity profile.
- Skin-relevant robustness.
- Formulation compatibility.
- Manufacturability/developability heuristics.

### Output Package
- Lead nomination memo.
- Full traceable data bundle.
- Risk register and mitigation plan.

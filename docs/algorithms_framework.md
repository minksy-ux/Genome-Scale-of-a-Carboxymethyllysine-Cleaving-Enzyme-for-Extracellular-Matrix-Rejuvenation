# Algorithms Framework for CMLase-ECM and Clinical Translation

This document maps algorithm families to concrete project tasks across enzyme engineering, formulation optimization, and future clinical decision support.

## 1. Core Computer-Science Algorithms

## 1.1 Optimization Algorithms

### Gradient-based optimization
- Methods: SGD, Adam, AdamW.
- Use in project:
  - Train sequence-to-function predictors from variant assay data.
  - Fit multitask models for activity, selectivity, and stability jointly.
- Typical inputs:
  - Sequence or structure embeddings.
  - Assay metadata and condition features.
- Typical outputs:
  - Predicted kcat/Km surrogate scores.
  - Off-target risk estimates.

### Gradient-free optimization
- Methods: Bayesian optimization, CMA-ES, evolution strategies.
- Use in project:
  - Propose mutation sets where objective is noisy and black-box.
  - Optimize formulation compositions when gradients are unavailable.
- Acquisition examples:
  - Expected improvement.
  - Upper confidence bound.
  - Thompson sampling.

## 1.2 Graph and Network Algorithms

### Protein contact and interaction graphs
- Methods: shortest paths, centrality, community detection.
- Use in project:
  - Identify active-site residue subnetworks linked to selectivity.
  - Prioritize mutation hot spots via graph influence metrics.

### Clinical knowledge graphs
- Methods: graph traversal, node ranking, link prediction.
- Use in project:
  - Hypothesis generation for patient subgroup benefit.
  - Identify biomarker-feature relationships for response modeling.

## 1.3 Dynamic Programming

### Sequence alignment and conservation tracking
- Methods: Needleman-Wunsch, Smith-Waterman.
- Use in project:
  - Compare variants with natural homologs.
  - Quantify conservation-aware mutation burden to manage immunogenicity drift.

### Energy or structure-feature approximations
- Use in project:
  - Build compact fold-relevant descriptors from alignment and local motif states.

## 1.4 Clustering and Dimensionality Reduction

### Clustering
- Methods: k-means, hierarchical clustering, density-based clustering.
- Use in project:
  - Group mutation-response profiles.
  - Detect assay-condition regimes with distinct behavior.

### Dimensionality reduction
- Methods: PCA, UMAP, t-SNE.
- Use in project:
  - Visualize high-dimensional sequence-function landscapes.
  - Explore transcriptomic or explant-response shifts after treatment.

## 2. Applied ML/AI in Biomedicine

## 2.1 Supervised Prediction
- Methods: random forests, gradient boosting, SVMs, neural networks.
- Use in project:
  - Predict activity, selectivity, stability, and compatibility under formulation stress.
- Clinical extension:
  - Predict probable responder strata and protocol suitability from patient-level features.

## 2.2 Deep Learning for Sequence and Structure
- Methods: transformers, graph neural networks, sequence CNN/RNN baselines.
- Use in project:
  - Learn embeddings that encode mutation context and residue interactions.
  - Predict mutational effects using structure-aware representations.

## 2.3 Unsupervised and Self-Supervised Learning
- Methods: protein language-model pretraining, contrastive representation learning.
- Use in project:
  - Initialize robust embeddings before low-data supervised fine-tuning.
  - Discover latent variant clusters and candidate mechanism classes.
- Clinical extension:
  - Discover patient or explant subgroups with distinct response trajectories.

## 2.4 Reinforcement Learning and Bandits
- Methods: contextual bandits, constrained RL.
- Use in project:
  - Sequential design of experiments for variant and formulation testing.
  - Maximize expected gain per assay budget under safety constraints.
- Clinical extension:
  - Adaptive protocol refinement with conservative policy updates.

## 3. Medical Decision Algorithms

## 3.1 Rule-Based Clinical Logic
- Methods: explicit decision trees, guideline rule engines.
- Use in project:
  - Encode exclusion criteria and protocol branching in early translational planning.

## 3.2 Risk and Time-to-Event Models
- Methods: logistic regression, Cox-type survival models.
- Use in project:
  - Estimate probability of benefit and adverse outcomes over defined windows.
  - Support patient stratification scenarios for future studies.

## 3.3 Explainable and Dynamic Models
- Methods: calibrated models, feature attribution, drift monitoring.
- Use in project:
  - Maintain transparent rationale for variant and protocol decisions.
  - Update models safely as new assay or clinical evidence arrives.

## 4. Integrated Algorithm Stack by Project Phase

1. Scaffold triage:
- Alignment plus graph features plus supervised ranking.

2. Variant proposal:
- Sequence/structure models plus Bayesian optimization or bandits.

3. Directed-evolution loop:
- Active learning with uncertainty, clustering for landscape interpretation.

4. Formulation optimization:
- Gradient-free optimization and multi-objective tradeoff analysis.

5. Translational planning:
- Rule-based decision pathways plus risk prediction and explainability.

## 5. Suggested Baseline Implementation

### Data layer
- Schema-validated variant, assay, and formulation records.
- Versioned feature store and model manifests.

### Modeling layer
- Baseline ensemble: gradient boosting plus transformer embedding features.
- Uncertainty head or ensemble variance for acquisition policies.

### Decision layer
- Multi-objective score combining catalytic performance, selectivity, stability, and developability.
- Gate-based advancement with explicit pass/fail criteria.

### Governance layer
- Reproducibility logs, audit trails, and model drift checks.

## 6. Practical Guardrails
- Use strict train/validation/test separation across rounds when feasible.
- Track assay batch effects and include controls in model features.
- Prefer conservative exploration policies when off-target risk uncertainty is high.
- Keep clinical decision support interpretable and calibration-monitored.

## 7. Schema Mapping
For a compact implementation mapping between algorithm families and required schema fields, see docs/algorithm_schema_matrix.md.

# Pseudocode for AI + Directed Evolution Loop

## 1. Round Orchestrator

```text
function run_round(round_id, config):
    scaffolds = load_scaffold_panel(config.scaffold_source)
    dataset = load_validated_dataset(config.dataset_version)

    model_bundle = train_models(dataset, config.model_params)
    proposals = propose_variants(
        scaffolds=scaffolds,
        model_bundle=model_bundle,
        constraints=config.sequence_constraints,
        budget=config.library_budget
    )

    proposal_manifest = register_proposal_manifest(round_id, proposals, model_bundle)
    dispatch_for_assay(proposal_manifest)

    assay_records = wait_for_and_ingest_assay_results(round_id)
    validated_records = validate_records(assay_records, schema_set=config.schemas)

    merged_dataset = append_dataset(dataset, validated_records)
    publish_dataset_snapshot(round_id, merged_dataset)

    metrics = evaluate_progress(merged_dataset, config.target_spec)
    decisions = gate_decisions(metrics, config.gates)

    return {
        "round_id": round_id,
        "proposal_manifest_id": proposal_manifest.id,
        "metrics": metrics,
        "decisions": decisions
    }
```

## 2. Variant Proposal Engine

```text
function propose_variants(scaffolds, model_bundle, constraints, budget):
    candidate_space = enumerate_mutations(
        scaffolds=scaffolds,
        mutable_positions=constraints.mutable_positions,
        max_mutations_per_variant=constraints.max_mutations
    )

    filtered = filter_by_hard_constraints(
        candidates=candidate_space,
        forbidden_motifs=constraints.forbidden_motifs,
        sequence_naturalness_min=constraints.naturalness_min,
        developability_limits=constraints.developability
    )

    scored = []
    for variant in filtered:
        pred = model_bundle.predict(variant)
        acquisition = compute_acquisition(
            expected_gain=pred.activity_selectivity_score,
            uncertainty=pred.uncertainty,
            novelty=pred.embedding_distance
        )
        scored.append({"variant": variant, "pred": pred, "acq": acquisition})

    diverse_set = diversity_select(scored, budget)
    return sort_descending(diverse_set, key="acq")
```

## 3. Formulation Co-Optimization

```text
function formulation_screen(lead_variants, excipient_matrix, conditions):
    results = []
    for variant in lead_variants:
        for formula in excipient_matrix:
            profile = run_stability_panel(
                variant=variant,
                formula=formula,
                conditions=conditions
            )
            retained_activity = summarize_retained_activity(profile)
            compatibility = classify_compatibility(retained_activity)
            results.append({
                "variant_id": variant.id,
                "formula_id": formula.id,
                "retained_activity": retained_activity,
                "compatibility": compatibility
            })

    return rank_formulations(results)
```

## 4. Lead Nomination Logic

```text
function nominate_leads(candidate_reports, target_spec):
    eligible = []
    for report in candidate_reports:
        if passes_primary(report, target_spec.primary) and passes_secondary(report, target_spec.secondary):
            eligible.append(report)

    if length(eligible) == 0:
        return {"status": "no_lead", "action": "expand_search_space"}

    ranked = sort_by_weighted_score(eligible, target_spec.weights)
    return {
        "status": "lead_selected",
        "lead": ranked[0],
        "backup": ranked[1] if length(ranked) > 1 else null
    }
```

#!/usr/bin/env python3
"""Score formulation records using the paper-aligned 0-100 rubric.

This script reads one or more formulation JSON files and computes subscores
for efficacy proxy alignment, stability/integrity, delivery plausibility, and
deployability/process control.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _as_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _nested_get(data: dict[str, Any], *keys: str) -> Any:
    cur: Any = data
    for key in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _non_empty_text(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _count_nonzero(values: list[Any]) -> int:
    count = 0
    for value in values:
        n = _as_number(value)
        if n is not None and n > 0:
            count += 1
    return count


def score_efficacy_proxy(record: dict[str, Any]) -> tuple[int, dict[str, int]]:
    activity = _as_number(_nested_get(record, "enzyme_module", "activity_u_per_g"))
    fraction = _as_number(_nested_get(record, "enzyme_module", "enzyme_fraction_w_w"))
    ph_min = _as_number(_nested_get(record, "on_skin_targets", "target_ph_min"))
    ph_max = _as_number(_nested_get(record, "on_skin_targets", "target_ph_max"))
    contact_time = _as_number(_nested_get(record, "on_skin_targets", "target_contact_time_min"))

    if activity is None:
        activity_pts = 0
    elif activity >= 50:
        activity_pts = 15
    elif activity >= 25:
        activity_pts = 10
    elif activity >= 10:
        activity_pts = 5
    else:
        activity_pts = 0

    if fraction is None:
        fraction_pts = 0
    elif fraction >= 0.005:
        fraction_pts = 10
    elif fraction >= 0.002:
        fraction_pts = 6
    else:
        fraction_pts = 2

    if ph_min is None or ph_max is None:
        ph_pts = 0
    else:
        # Full alignment if formulation pH band is entirely inside 5.8-6.2.
        if ph_min >= 5.8 and ph_max <= 6.2:
            ph_pts = 10
        # Partial overlap with 5.8-6.2 is still useful.
        elif ph_max >= 5.8 and ph_min <= 6.2:
            ph_pts = 5
        else:
            ph_pts = 0

    if contact_time is None:
        contact_pts = 0
    elif contact_time >= 480:
        contact_pts = 5
    elif contact_time >= 240:
        contact_pts = 3
    else:
        contact_pts = 1

    detail = {
        "activity": activity_pts,
        "enzyme_fraction": fraction_pts,
        "ph_alignment": ph_pts,
        "contact_time": contact_pts,
    }
    return activity_pts + fraction_pts + ph_pts + contact_pts, detail


def score_stability(record: dict[str, Any]) -> tuple[int, dict[str, int]]:
    retained = _as_number(_nested_get(record, "stability_profile", "retained_activity_pct"))
    duration = _as_number(_nested_get(record, "stability_profile", "conditions", "duration_days"))
    physical_status = _nested_get(record, "stability_profile", "physical_status")
    trehalose = _nested_get(record, "stabilization_system", "trehalose_pct")
    methionine = _nested_get(record, "stabilization_system", "methionine_pct")
    edta = _nested_get(record, "stabilization_system", "edta_pct")

    if retained is None:
        retained_pts = 0
    elif retained >= 80:
        retained_pts = 15
    elif retained >= 70:
        retained_pts = 11
    elif retained >= 60:
        retained_pts = 7
    else:
        retained_pts = 3

    if duration is None:
        duration_pts = 0
    elif duration >= 90:
        duration_pts = 5
    elif duration >= 60:
        duration_pts = 3
    elif duration >= 30:
        duration_pts = 2
    else:
        duration_pts = 1

    if physical_status == "stable":
        physical_pts = 3
    elif physical_status == "unknown":
        physical_pts = 1
    else:
        physical_pts = 0

    protection_count = _count_nonzero([trehalose, methionine, edta])
    if protection_count >= 2:
        protection_pts = 2
    elif protection_count == 1:
        protection_pts = 1
    else:
        protection_pts = 0

    detail = {
        "retained_activity": retained_pts,
        "duration": duration_pts,
        "physical_status": physical_pts,
        "protection_system": protection_pts,
    }
    return retained_pts + duration_pts + physical_pts + protection_pts, detail


def score_delivery(record: dict[str, Any]) -> tuple[int, dict[str, int]]:
    fmt = record.get("format")
    enhancers = _nested_get(record, "delivery_support", "penetration_enhancers")
    motif = _nested_get(record, "delivery_support", "ecm_targeting_motif")
    encapsulation = _nested_get(record, "enzyme_module", "encapsulation_type")

    if fmt == "dual_chamber_cream":
        architecture_pts = 8
    elif fmt in {"gel_cream", "serum"}:
        architecture_pts = 5
    elif fmt == "single_phase_cream":
        architecture_pts = 3
    else:
        architecture_pts = 1

    has_enhancer = isinstance(enhancers, list) and len(enhancers) > 0
    has_motif = _non_empty_text(motif)
    if has_enhancer and has_motif:
        access_pts = 7
    elif has_enhancer or has_motif:
        access_pts = 4
    else:
        access_pts = 1

    if encapsulation in {"liposome", "niosome", "supramolecular"}:
        encapsulation_pts = 5
    elif encapsulation == "other":
        encapsulation_pts = 3
    elif encapsulation == "none":
        encapsulation_pts = 1
    else:
        encapsulation_pts = 1

    detail = {
        "architecture": architecture_pts,
        "tissue_access": access_pts,
        "encapsulation": encapsulation_pts,
    }
    return architecture_pts + access_pts + encapsulation_pts, detail


def score_deployability(record: dict[str, Any]) -> tuple[int, dict[str, int]]:
    cold_process = _nested_get(record, "process_controls", "cold_process_preferred")
    max_temp = _as_number(_nested_get(record, "process_controls", "max_enzyme_addition_temp_c"))
    shear = _nested_get(record, "process_controls", "mixing_shear")
    packaging = _nested_get(record, "process_controls", "packaging")
    components = record.get("components")

    process_conditions = [
        cold_process is True,
        max_temp is not None and max_temp <= 35,
        shear == "low",
    ]
    process_hits = sum(1 for cond in process_conditions if cond)
    if process_hits == 3:
        process_pts = 8
    elif process_hits >= 1:
        process_pts = 4
    else:
        process_pts = 1

    if packaging in {"dual_chamber", "reconstituted"}:
        packaging_pts = 4
    elif packaging == "single_chamber":
        packaging_pts = 2
    else:
        packaging_pts = 1

    roles = set()
    if isinstance(components, list):
        for item in components:
            if isinstance(item, dict) and isinstance(item.get("role"), str):
                roles.add(item["role"])

    required_roles = {"solvent", "enzyme_active", "stabilizer", "preservative"}
    role_hits = len(required_roles.intersection(roles))
    if role_hits == 4:
        composition_pts = 3
    elif role_hits == 3:
        composition_pts = 2
    else:
        composition_pts = 1

    detail = {
        "process_controls": process_pts,
        "packaging": packaging_pts,
        "role_coverage": composition_pts,
    }
    return process_pts + packaging_pts + composition_pts, detail


def classify_score(score: int) -> str:
    if score >= 85:
        return "Lead formulation candidate"
    if score >= 70:
        return "Backup candidate"
    if score >= 55:
        return "Experimental candidate"
    return "Do not prioritize"


def score_record(record: dict[str, Any]) -> dict[str, Any]:
    efficacy_score, efficacy_detail = score_efficacy_proxy(record)
    stability_score, stability_detail = score_stability(record)
    delivery_score, delivery_detail = score_delivery(record)
    deployability_score, deployability_detail = score_deployability(record)

    total = efficacy_score + stability_score + delivery_score + deployability_score
    return {
        "total_score": total,
        "classification": classify_score(total),
        "subscores": {
            "efficacy_proxy": {
                "score": efficacy_score,
                "max": 40,
                "detail": efficacy_detail,
            },
            "stability_integrity": {
                "score": stability_score,
                "max": 25,
                "detail": stability_detail,
            },
            "delivery_plausibility": {
                "score": delivery_score,
                "max": 20,
                "detail": delivery_detail,
            },
            "deployability_process": {
                "score": deployability_score,
                "max": 15,
                "detail": deployability_detail,
            },
        },
    }


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON must be an object")
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score formulation JSON records")
    parser.add_argument(
        "files",
        nargs="*",
        default=[
            "examples/formulation_record.example.json",
            "examples/formulation_record.minimal.valid.json",
        ],
        help="Formulation JSON files to score",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of plain text",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results: list[dict[str, Any]] = []

    for file_path in args.files:
        path = Path(file_path)
        if not path.exists():
            print(f"[FAIL] {file_path}: file not found")
            continue
        try:
            record = load_json(path)
            scored = score_record(record)
            results.append(
                {
                    "file": file_path,
                    "formulation_id": record.get("formulation_id", "unknown"),
                    **scored,
                }
            )
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[FAIL] {file_path}: {exc}")

    results.sort(key=lambda item: item["total_score"], reverse=True)

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    if not results:
        print("No formulations were scored.")
        return 1

    print("Paper-aligned formulation ranking")
    print("=")
    for rank, result in enumerate(results, start=1):
        print(f"{rank}. {result['formulation_id']} ({result['file']})")
        print(f"   total: {result['total_score']}/100 -> {result['classification']}")
        subs = result["subscores"]
        print(
            "   subscores: "
            f"E {subs['efficacy_proxy']['score']}/{subs['efficacy_proxy']['max']}, "
            f"S {subs['stability_integrity']['score']}/{subs['stability_integrity']['max']}, "
            f"D {subs['delivery_plausibility']['score']}/{subs['delivery_plausibility']['max']}, "
            f"P {subs['deployability_process']['score']}/{subs['deployability_process']['max']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
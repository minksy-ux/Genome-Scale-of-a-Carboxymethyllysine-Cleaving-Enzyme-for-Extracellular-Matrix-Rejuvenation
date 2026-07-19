#!/usr/bin/env python3
"""Smoke validator for formulation example payloads.

This script intentionally validates a focused subset of the formulation schema
without third-party dependencies. It is meant for quick pass/fail checks of the
repository example files.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

ALLOWED_TOP_LEVEL = {
    "formulation_id",
    "variant_id",
    "format",
    "components",
    "enzyme_module",
    "stabilization_system",
    "delivery_support",
    "supportive_actives",
    "stability_profile",
    "process_controls",
    "on_skin_targets",
    "created_at",
}

FORMAT_ENUM = {"single_phase_cream", "dual_chamber_cream", "gel_cream", "serum"}
PHYSICAL_STATUS_ENUM = {"stable", "phase_separation", "precipitation", "viscosity_shift", "unknown"}
ENCAPSULATION_ENUM = {"none", "liposome", "niosome", "supramolecular", "other"}
ACTIVE_CLASS_ENUM = {"dicarbonyl_scavenger", "antioxidant", "ecm_support", "soothing", "other"}
SHEAR_ENUM = {"low", "medium", "high", "unspecified"}
PACKAGING_ENUM = {"single_chamber", "dual_chamber", "reconstituted", "other"}


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_datetime(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def range_check(value: Any, low: float | None = None, high: float | None = None) -> bool:
    if not is_number(value):
        return False
    if low is not None and value < low:
        return False
    if high is not None and value > high:
        return False
    return True


def validate_components(components: Any, errors: list[str]) -> None:
    if not isinstance(components, list):
        errors.append("components must be an array")
        return
    for i, item in enumerate(components):
        if not isinstance(item, dict):
            errors.append(f"components[{i}] must be an object")
            continue
        for req in ("name", "role"):
            if req not in item:
                errors.append(f"components[{i}].{req} is required")
        if "name" in item and not isinstance(item["name"], str):
            errors.append(f"components[{i}].name must be a string")
        if "role" in item and not isinstance(item["role"], str):
            errors.append(f"components[{i}].role must be a string")
        if "fraction_w_w" in item and not range_check(item["fraction_w_w"], 0, 1):
            errors.append(f"components[{i}].fraction_w_w must be between 0 and 1")


def validate_formulation(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for key in payload:
        if key not in ALLOWED_TOP_LEVEL:
            errors.append(f"unexpected top-level field: {key}")

    for req in ("formulation_id", "variant_id", "format", "components", "stability_profile", "created_at"):
        if req not in payload:
            errors.append(f"{req} is required")

    if "formulation_id" in payload and (not isinstance(payload["formulation_id"], str) or not payload["formulation_id"]):
        errors.append("formulation_id must be a non-empty string")
    if "variant_id" in payload and (not isinstance(payload["variant_id"], str) or not payload["variant_id"]):
        errors.append("variant_id must be a non-empty string")
    if "format" in payload and payload["format"] not in FORMAT_ENUM:
        errors.append("format must be one of: single_phase_cream, dual_chamber_cream, gel_cream, serum")

    if "components" in payload:
        validate_components(payload["components"], errors)

    stability = payload.get("stability_profile")
    if isinstance(stability, dict):
        for req in ("conditions", "retained_activity_pct"):
            if req not in stability:
                errors.append(f"stability_profile.{req} is required")
        conditions = stability.get("conditions")
        if isinstance(conditions, dict):
            if "temperature_c" in conditions and not is_number(conditions["temperature_c"]):
                errors.append("stability_profile.conditions.temperature_c must be a number")
            if "duration_days" in conditions and not range_check(conditions["duration_days"], 0, None):
                errors.append("stability_profile.conditions.duration_days must be >= 0")
        else:
            errors.append("stability_profile.conditions must be an object")
        if "retained_activity_pct" in stability and not range_check(stability["retained_activity_pct"], 0, 100):
            errors.append("stability_profile.retained_activity_pct must be between 0 and 100")
        if "physical_status" in stability and stability["physical_status"] not in PHYSICAL_STATUS_ENUM:
            errors.append("stability_profile.physical_status must be a known enum value")
    else:
        errors.append("stability_profile must be an object")

    enzyme_module = payload.get("enzyme_module")
    if enzyme_module is not None:
        if not isinstance(enzyme_module, dict):
            errors.append("enzyme_module must be an object")
        else:
            allowed = {"enzyme_name", "enzyme_variant", "enzyme_fraction_w_w", "activity_u_per_g", "encapsulation_type"}
            for key in enzyme_module:
                if key not in allowed:
                    errors.append(f"enzyme_module unexpected field: {key}")
            if "enzyme_fraction_w_w" in enzyme_module and not range_check(enzyme_module["enzyme_fraction_w_w"], 0, 1):
                errors.append("enzyme_module.enzyme_fraction_w_w must be between 0 and 1")
            if "activity_u_per_g" in enzyme_module and not range_check(enzyme_module["activity_u_per_g"], 0, None):
                errors.append("enzyme_module.activity_u_per_g must be >= 0")
            if "encapsulation_type" in enzyme_module and enzyme_module["encapsulation_type"] not in ENCAPSULATION_ENUM:
                errors.append("enzyme_module.encapsulation_type must be a known enum value")

    supportive_actives = payload.get("supportive_actives")
    if supportive_actives is not None:
        if not isinstance(supportive_actives, list):
            errors.append("supportive_actives must be an array")
        else:
            for i, item in enumerate(supportive_actives):
                if not isinstance(item, dict):
                    errors.append(f"supportive_actives[{i}] must be an object")
                    continue
                if "name" not in item or "class" not in item:
                    errors.append(f"supportive_actives[{i}] requires name and class")
                if "class" in item and item["class"] not in ACTIVE_CLASS_ENUM:
                    errors.append(f"supportive_actives[{i}].class must be a known enum value")
                if "pct" in item and not range_check(item["pct"], 0, 100):
                    errors.append(f"supportive_actives[{i}].pct must be between 0 and 100")

    process_controls = payload.get("process_controls")
    if process_controls is not None:
        if not isinstance(process_controls, dict):
            errors.append("process_controls must be an object")
        else:
            if "max_enzyme_addition_temp_c" in process_controls and not is_number(process_controls["max_enzyme_addition_temp_c"]):
                errors.append("process_controls.max_enzyme_addition_temp_c must be a number")
            if "mixing_shear" in process_controls and process_controls["mixing_shear"] not in SHEAR_ENUM:
                errors.append("process_controls.mixing_shear must be a known enum value")
            if "packaging" in process_controls and process_controls["packaging"] not in PACKAGING_ENUM:
                errors.append("process_controls.packaging must be a known enum value")

    if "created_at" in payload and not is_datetime(payload["created_at"]):
        errors.append("created_at must be an ISO-8601 date-time")

    return errors


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("payload must be a top-level JSON object")
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate formulation example payloads")
    parser.add_argument(
        "--valid",
        nargs="*",
        default=["examples/formulation_record.example.json", "examples/formulation_record.minimal.valid.json"],
        help="Payloads expected to pass validation",
    )
    parser.add_argument(
        "--invalid",
        nargs="*",
        default=["examples/formulation_record.intentionally.invalid.json"],
        help="Payloads expected to fail validation",
    )
    return parser.parse_args()


def validate_set(paths: list[str], expect_valid: bool) -> tuple[int, int]:
    passed = 0
    failed = 0

    mode = "valid" if expect_valid else "invalid"
    print(f"Checking {mode} payloads...")

    for p in paths:
        path = Path(p)
        if not path.exists():
            print(f"  [FAIL] {p}: file not found")
            failed += 1
            continue
        try:
            errors = validate_formulation(load_json(path))
        except Exception as exc:  # pylint: disable=broad-except
            print(f"  [FAIL] {p}: {exc}")
            failed += 1
            continue

        is_valid = len(errors) == 0
        if expect_valid and is_valid:
            print(f"  [PASS] {p}")
            passed += 1
        elif (not expect_valid) and (not is_valid):
            print(f"  [PASS] {p} (rejected as expected)")
            for err in errors[:3]:
                print(f"         - {err}")
            passed += 1
        else:
            verdict = "unexpected rejection" if expect_valid else "unexpected acceptance"
            print(f"  [FAIL] {p}: {verdict}")
            for err in errors[:5]:
                print(f"         - {err}")
            failed += 1

    return passed, failed


def main() -> int:
    args = parse_args()

    v_passed, v_failed = validate_set(args.valid, expect_valid=True)
    i_passed, i_failed = validate_set(args.invalid, expect_valid=False)

    total_passed = v_passed + i_passed
    total_failed = v_failed + i_failed

    print(f"Summary: {total_passed} passed, {total_failed} failed")
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

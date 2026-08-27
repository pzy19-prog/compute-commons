#!/usr/bin/env python3
"""Minimal local validator for Phase 1 runtime evidence capture records.

This intentionally validates only the experiment capture envelope. CRE 0.1
validation is a separate step because Phase 1 is testing whether CRE can
losslessly represent the captured evidence.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
REQUIRED = {
    "experiment_id",
    "claim_id",
    "evidence_class",
    "provider",
    "surface",
    "observed_at",
    "canonical_input",
    "raw_evidence",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate(record: dict) -> None:
    missing = REQUIRED - set(record)
    if missing:
        fail(f"missing required fields: {sorted(missing)}")
    if record["evidence_class"] != "observed":
        fail("runtime capture evidence_class must be 'observed'")
    for key in ("experiment_id", "claim_id", "provider", "surface"):
        if not isinstance(record[key], str) or not record[key].strip():
            fail(f"{key} must be a non-empty string")
    try:
        datetime.fromisoformat(record["observed_at"].replace("Z", "+00:00"))
    except Exception as exc:
        fail(f"observed_at is not ISO-8601: {exc}")

    canonical = record["canonical_input"]
    if canonical.get("representation") not in {"inline", "redacted", "hash-only"}:
        fail("canonical_input.representation is invalid")
    digest = canonical.get("sha256", "")
    if not SHA256_RE.fullmatch(digest):
        fail("canonical_input.sha256 must be lowercase SHA-256 hex")

    raw = record["raw_evidence"]
    if raw.get("kind") not in {"inline-json", "file", "artifact", "hash-reference"}:
        fail("raw_evidence.kind is invalid")
    if not isinstance(raw.get("reference"), str) or not raw["reference"].strip():
        fail("raw_evidence.reference must be non-empty")
    if "sha256" in raw and not SHA256_RE.fullmatch(raw["sha256"]):
        fail("raw_evidence.sha256 must be lowercase SHA-256 hex")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <capture.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            fail("top-level JSON must be an object")
        validate(record)
    except Exception as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

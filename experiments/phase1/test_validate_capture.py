#!/usr/bin/env python3
"""Tests for the dependency-free Phase 1 capture validator."""

from __future__ import annotations

import unittest

from validate_capture import validate


VALID = {
    "experiment_id": "E1",
    "claim_id": "E1-claim-a",
    "evidence_class": "observed",
    "provider": "example-provider",
    "surface": "example-surface",
    "observed_at": "2026-08-27T07:00:00Z",
    "canonical_input": {
        "representation": "hash-only",
        "sha256": "a" * 64,
        "serialization": "json-canonical-v1",
    },
    "raw_evidence": {
        "kind": "hash-reference",
        "reference": "artifact://example",
        "sha256": "b" * 64,
    },
    "usage": {"input_tokens": 10},
}


class CaptureValidationTests(unittest.TestCase):
    def test_valid_record(self) -> None:
        validate(dict(VALID))

    def test_declared_is_rejected_for_runtime_capture(self) -> None:
        record = dict(VALID)
        record["evidence_class"] = "declared"
        with self.assertRaisesRegex(ValueError, "must be 'observed'"):
            validate(record)

    def test_missing_provenance_is_rejected(self) -> None:
        record = dict(VALID)
        record.pop("raw_evidence")
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            validate(record)

    def test_bad_input_digest_is_rejected(self) -> None:
        record = dict(VALID)
        record["canonical_input"] = dict(VALID["canonical_input"])
        record["canonical_input"]["sha256"] = "not-a-digest"
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            validate(record)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Capture paired preflight-count and execution-usage evidence.

Supported providers: openai, anthropic, gemini.

The script never accepts API keys as command-line arguments. Credentials are
read from provider-specific environment variables and are never written to
artifacts. Use --dry-run to inspect request shapes without network access.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_PROMPT = "Compute Commons Phase 1 token-accounting probe. Reply with exactly: OK"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "value"


def request_id(headers: dict[str, str], body: dict[str, Any]) -> str | None:
    for key in ("x-request-id", "request-id", "x-goog-request-id"):
        if headers.get(key):
            return headers[key]
    candidate = body.get("id")
    return candidate if isinstance(candidate, str) else None


def post_json(url: str, headers: dict[str, str], payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str], bytes]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = response.read()
            response_headers = {k.lower(): v for k, v in response.headers.items()}
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        detail = raw.decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from exc
    parsed = json.loads(raw.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise RuntimeError(f"expected JSON object from {url}")
    return parsed, response_headers, raw


def provider_plan(provider: str, model: str, prompt: str, max_output_tokens: int) -> dict[str, Any]:
    if provider == "openai":
        canonical = {"model": model, "input": prompt}
        return {
            "canonical": canonical,
            "count_url": "https://api.openai.com/v1/responses/input_tokens",
            "count_body": dict(canonical),
            "execute_url": "https://api.openai.com/v1/responses",
            "execute_body": {**canonical, "max_output_tokens": max_output_tokens},
            "key_env": "OPENAI_API_KEY",
        }

    if provider == "anthropic":
        canonical = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
        return {
            "canonical": canonical,
            "count_url": "https://api.anthropic.com/v1/messages/count_tokens",
            "count_body": dict(canonical),
            "execute_url": "https://api.anthropic.com/v1/messages",
            "execute_body": {**canonical, "max_tokens": max_output_tokens},
            "key_env": "ANTHROPIC_API_KEY",
        }

    if provider == "gemini":
        model_id = model.removeprefix("models/")
        encoded_model = urllib.parse.quote(model_id, safe="")
        canonical = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        }
        return {
            "canonical": canonical,
            "count_url": f"https://generativelanguage.googleapis.com/v1beta/models/{encoded_model}:countTokens",
            "count_body": dict(canonical),
            "execute_url": f"https://generativelanguage.googleapis.com/v1beta/models/{encoded_model}:generateContent",
            "execute_body": {
                **canonical,
                "generationConfig": {"maxOutputTokens": max_output_tokens},
            },
            "key_env": "GEMINI_API_KEY",
        }

    raise ValueError(f"unsupported provider: {provider}")


def auth_headers(provider: str, key: str) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if provider == "openai":
        headers["Authorization"] = f"Bearer {key}"
    elif provider == "anthropic":
        headers["X-Api-Key"] = key
        headers["anthropic-version"] = "2023-06-01"
    elif provider == "gemini":
        headers["x-goog-api-key"] = key
    return headers


def usage_objects(provider: str, count_body: dict[str, Any], execute_body: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if provider in {"openai", "anthropic"}:
        count_usage = {"input_tokens": count_body.get("input_tokens")}
        execute_usage = execute_body.get("usage") or {}
    else:
        count_usage = {"totalTokens": count_body.get("totalTokens")}
        execute_usage = execute_body.get("usageMetadata") or {}
    return count_usage, execute_usage


def comparable_input(provider: str, count_usage: dict[str, Any], execute_usage: dict[str, Any]) -> tuple[int | None, int | None]:
    if provider == "openai":
        return count_usage.get("input_tokens"), execute_usage.get("input_tokens")
    if provider == "anthropic":
        # This baseline runner does not configure prompt caching. Cache variants
        # are separate experiments because input_tokens has different semantics
        # after a cache breakpoint.
        return count_usage.get("input_tokens"), execute_usage.get("input_tokens")
    return count_usage.get("totalTokens"), execute_usage.get("promptTokenCount")


def write_json(path: Path, value: Any) -> str:
    raw = json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n"
    path.write_bytes(raw)
    return sha256_bytes(raw)


def capture_record(
    *,
    experiment_id: str,
    claim_id: str,
    provider: str,
    surface: str,
    model: str,
    observed_at: str,
    provider_request_id: str | None,
    correlation_id: str,
    canonical_digest: str,
    usage: dict[str, Any],
    raw_path: Path,
    raw_digest: str,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "experiment_id": experiment_id,
        "claim_id": claim_id,
        "evidence_class": "observed",
        "provider": provider,
        "surface": surface,
        "model": model,
        "observed_at": observed_at,
        "correlation_id": correlation_id,
        "canonical_input": {
            "representation": "hash-only",
            "sha256": canonical_digest,
            "serialization": "json-sort-keys-compact-v1",
            "description": "Canonical token-relevant input generated by run_dual_surface.py",
        },
        "usage": usage,
        "raw_evidence": {
            "kind": "file",
            "reference": raw_path.name,
            "sha256": raw_digest,
        },
    }
    if provider_request_id:
        record["provider_request_id"] = provider_request_id
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("provider", choices=["openai", "anthropic", "gemini"])
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--max-output-tokens", type=int, default=16)
    parser.add_argument("--artifacts-dir", default="artifacts")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = provider_plan(args.provider, args.model, args.prompt, args.max_output_tokens)
    canonical_digest = sha256_bytes(canonical_bytes(plan["canonical"]))

    if args.dry_run:
        print(json.dumps({
            "provider": args.provider,
            "model": args.model,
            "canonical_sha256": canonical_digest,
            "count_url": plan["count_url"],
            "count_body": plan["count_body"],
            "execute_url": plan["execute_url"],
            "execute_body": plan["execute_body"],
            "credential_env": plan["key_env"],
        }, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    key = os.environ.get(plan["key_env"])
    if not key:
        print(f"missing required environment variable: {plan['key_env']}", file=sys.stderr)
        return 2

    headers = auth_headers(args.provider, key)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.artifacts_dir) / f"{timestamp}-{args.provider}-{safe_name(args.model)}"
    out_dir.mkdir(parents=True, exist_ok=False)

    write_json(out_dir / "canonical-input.json", plan["canonical"])
    write_json(out_dir / "count-request.json", plan["count_body"])
    write_json(out_dir / "execute-request.json", plan["execute_body"])

    count_time = now_iso()
    count_json, count_headers, count_raw = post_json(plan["count_url"], headers, plan["count_body"])
    count_raw_path = out_dir / "count-response.json"
    count_raw_path.write_bytes(count_raw + (b"\n" if not count_raw.endswith(b"\n") else b""))
    count_digest = sha256_bytes(count_raw_path.read_bytes())

    execute_time = now_iso()
    execute_json, execute_headers, execute_raw = post_json(plan["execute_url"], headers, plan["execute_body"])
    execute_raw_path = out_dir / "execute-response.json"
    execute_raw_path.write_bytes(execute_raw + (b"\n" if not execute_raw.endswith(b"\n") else b""))
    execute_digest = sha256_bytes(execute_raw_path.read_bytes())

    count_usage, execute_usage = usage_objects(args.provider, count_json, execute_json)
    correlation_id = f"sha256:{canonical_digest}"
    experiment_id = {"openai": "E1", "anthropic": "E2", "gemini": "E3"}[args.provider]
    count_surface = {
        "openai": "responses.input_tokens",
        "anthropic": "messages.count_tokens",
        "gemini": "countTokens",
    }[args.provider]
    execute_surface = {
        "openai": "responses.create",
        "anthropic": "messages.create",
        "gemini": "generateContent.usageMetadata",
    }[args.provider]

    count_record = capture_record(
        experiment_id=experiment_id,
        claim_id=f"{experiment_id}-preflight",
        provider=args.provider,
        surface=count_surface,
        model=args.model,
        observed_at=count_time,
        provider_request_id=request_id(count_headers, count_json),
        correlation_id=correlation_id,
        canonical_digest=canonical_digest,
        usage=count_usage,
        raw_path=count_raw_path,
        raw_digest=count_digest,
    )
    execute_record = capture_record(
        experiment_id=experiment_id,
        claim_id=f"{experiment_id}-execution",
        provider=args.provider,
        surface=execute_surface,
        model=args.model,
        observed_at=execute_time,
        provider_request_id=request_id(execute_headers, execute_json),
        correlation_id=correlation_id,
        canonical_digest=canonical_digest,
        usage=execute_usage,
        raw_path=execute_raw_path,
        raw_digest=execute_digest,
    )

    write_json(out_dir / "claim-preflight.json", count_record)
    write_json(out_dir / "claim-execution.json", execute_record)

    preflight, execution = comparable_input(args.provider, count_usage, execute_usage)
    delta = execution - preflight if isinstance(preflight, int) and isinstance(execution, int) else None
    summary = {
        "experiment_id": experiment_id,
        "provider": args.provider,
        "model": args.model,
        "canonical_sha256": canonical_digest,
        "preflight_input_count": preflight,
        "execution_input_count": execution,
        "execution_minus_preflight": delta,
        "authority_selected": False,
        "note": "A zero or non-zero delta is evidence; this summary does not define settlement authority.",
    }
    write_json(out_dir / "summary.json", summary)
    print(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

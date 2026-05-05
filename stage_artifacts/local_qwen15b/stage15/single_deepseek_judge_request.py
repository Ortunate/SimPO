#!/usr/bin/env python3
"""Run one approved DeepSeek judge-template request without printing secrets."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_ENDPOINT = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-v4-flash"


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key:
                values[key] = value
    return values


def get_config(env_path: Path) -> tuple[str, str, str, dict[str, bool]]:
    dotenv = load_dotenv(env_path)

    def pick(*names: str) -> str | None:
        for name in names:
            value = os.environ.get(name) or dotenv.get(name)
            if value:
                return value
        return None

    key = pick("DEEPSEEK_API_KEY", "DEEPSEEK_KEY")
    endpoint = pick("DEEPSEEK_API_URL", "DEEPSEEK_API_BASE", "DEEPSEEK_BASE_URL") or DEFAULT_ENDPOINT
    model = pick("DEEPSEEK_MODEL", "DEEPSEEK_JUDGE_MODEL") or DEFAULT_MODEL
    presence = {
        "env_file_exists": env_path.exists(),
        "deepseek_key_present": bool(key),
        "endpoint_present": bool(endpoint),
        "model_present": bool(model),
    }
    if not key:
        raise RuntimeError("DeepSeek API key presence check failed")
    return key, endpoint, model, presence


def read_first_request(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                return json.loads(line)
    raise RuntimeError(f"no request found in {path}")


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = [line for line in stripped.splitlines() if not line.strip().startswith("```")]
        stripped = "\n".join(lines).strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(stripped[start : end + 1])


def validate_judge_output(obj: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["judge output is not an object"]
    allowed = {"winner", "score_a", "score_b", "confidence", "rationale"}
    missing = allowed - set(obj)
    extra = set(obj) - allowed
    if missing:
        errors.append(f"missing keys: {sorted(missing)}")
    if extra:
        errors.append(f"extra keys: {sorted(extra)}")
    if obj.get("winner") not in {"A", "B", "tie"}:
        errors.append("winner must be A, B, or tie")
    for key in ("score_a", "score_b"):
        value = obj.get(key)
        if not isinstance(value, int) or not 1 <= value <= 10:
            errors.append(f"{key} must be an integer from 1 to 10")
    confidence = obj.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0.0 <= float(confidence) <= 1.0:
        errors.append("confidence must be a number from 0.0 to 1.0")
    rationale = obj.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        errors.append("rationale must be a non-empty string")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-jsonl", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--env-file", default=Path(".env"), type=Path)
    parser.add_argument("--max-tokens", default=256, type=int)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    key, endpoint, model, presence = get_config(args.env_file)
    request_record = read_first_request(args.request_jsonl)

    payload: dict[str, Any] = {
        "model": model,
        "messages": request_record["messages"],
        "temperature": 0,
        "max_tokens": args.max_tokens,
        "thinking": {"type": "disabled"},
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    started = time.time()
    status_code = None
    response_json: dict[str, Any] | None = None
    error_text = None
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            status_code = response.status
            response_json = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        error_text = exc.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        error_text = f"{type(exc).__name__}: {exc}"
    ended = time.time()

    metadata: dict[str, Any] = {
        "request_id": request_record.get("request_id"),
        "pair_id": request_record.get("pair_id"),
        "order": request_record.get("order"),
        "endpoint_host": endpoint.split("/")[2] if "://" in endpoint else endpoint,
        "model": model,
        "status_code": status_code,
        "duration_s": round(ended - started, 3),
        "presence": presence,
        "api_calls": 1,
        "max_tokens": args.max_tokens,
    }

    parsed_judge = None
    parse_errors: list[str] = []
    choice_text = None
    if response_json is not None:
        choices = response_json.get("choices") or []
        if choices:
            choice_text = (choices[0].get("message") or {}).get("content")
        metadata["usage"] = response_json.get("usage")
        metadata["response_model"] = response_json.get("model")
    if isinstance(choice_text, str):
        try:
            parsed_judge = extract_json_object(choice_text)
            parse_errors = validate_judge_output(parsed_judge)
        except Exception as exc:  # noqa: BLE001
            parse_errors = [f"{type(exc).__name__}: {exc}"]

    safe_response = {
        "metadata": metadata,
        "judge_text": choice_text,
        "parsed_judge": parsed_judge,
        "parse_errors": parse_errors,
        "http_error_body": error_text if status_code and status_code >= 400 else None,
        "transport_error": error_text if status_code is None else None,
    }
    (args.out_dir / "single_request_result.json").write_text(
        json.dumps(safe_response, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (args.out_dir / "single_request_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(f"env_file_exists: {'yes' if presence['env_file_exists'] else 'no'}")
    print(f"deepseek_key_present: {'yes' if presence['deepseek_key_present'] else 'no'}")
    print(f"api_calls: {metadata['api_calls']}")
    print(f"status_code: {status_code}")
    print(f"parse_failures: {len(parse_errors)}")
    print(f"result_path: {args.out_dir / 'single_request_result.json'}")
    return 0 if status_code and 200 <= status_code < 300 and not parse_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

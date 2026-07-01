"""AIProvider abstraction - ADR-010 / handbook Chapter 4 §4.7, §4.10.

RULE-AI-1001: this interface accepts fully-computed evidence and confidence
as input and returns explanation text ONLY. No implementation may
originate an evidence item, a confidence score, or a suggested action.

RULE-AI-1002: switching between the hosted OpenAI API and a future
on-premises OpenAI-compatible endpoint is a configuration change
(base_url/api_key), never a code change.

RULE-AI-1003: if the configured provider is unavailable, the system falls
back to RuleBasedProvider automatically.

RULE-AI-1004: OpenAICompatibleProvider ships disabled by default.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import httpx

from app.core.config import get_settings


@dataclass
class StructuredEvidence:
    """Exactly the inputs required by the explanation contract, Ch.4.7 §4.7.2."""

    entity_label: str
    pattern_id: str
    observations: list[dict]  # [{type, value, unit, observed_at}, ...]
    confidence_band: str
    confidence_score: float
    suggested_action: str
    missing_information: str | None = None
    historical_context: str | None = None


class AIProvider(Protocol):
    name: str

    def explain(self, evidence: StructuredEvidence) -> str: ...


class RuleBasedProvider:
    """Default provider (Ch.4.5.6 RULE-KM-502). Template-driven, zero
    external dependency, satisfies §4.7.2 on its own."""

    name = "rule_based"

    def explain(self, evidence: StructuredEvidence) -> str:
        # Summarize by (type, value, unit) rather than listing every
        # contributing observation - several observations in the trend
        # window often share the same value (Ch.4.4 §4.4.6), and listing
        # each verbatim reads as repetitive rather than informative.
        seen: dict[tuple, int] = {}
        order: list[tuple] = []
        for obs in evidence.observations:
            key = (obs["type"], obs.get("value"), obs.get("unit") or "")
            if key not in seen:
                order.append(key)
            seen[key] = seen.get(key, 0) + 1

        obs_parts = []
        for obs_type, val, unit in order:
            count = seen[(obs_type, val, unit)]
            suffix = f" (x{count})" if count > 1 else ""
            obs_parts.append(f"{obs_type} = {val}{unit}{suffix}".strip())
        obs_text = "; ".join(obs_parts) if obs_parts else "no supporting observations"

        parts = [
            f"{evidence.entity_label}: {obs_text}.",
        ]
        if evidence.historical_context:
            parts.append(evidence.historical_context)
        parts.append(f"Confidence: {evidence.confidence_band.title()}.")
        parts.append(f"Suggested action: {evidence.suggested_action}.")
        if evidence.missing_information:
            parts.append(f"Missing: {evidence.missing_information}.")
        return " ".join(parts)


class OpenAICompatibleProvider:
    """Optional provider (disabled by default - RULE-AI-1004). Uses the
    OpenAI Chat Completions wire format, which works unmodified against
    the hosted OpenAI API OR a self-hosted, on-premises OpenAI-compatible
    inference server (e.g. vLLM, Ollama) by changing base_url/api_key
    only (RULE-AI-1002). Only rephrases the given evidence into natural
    language; never asked to invent facts, confidence, or actions."""

    name = "openai_compatible"

    def __init__(self, base_url: str, api_key: str, model: str):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._model = model

    def explain(self, evidence: StructuredEvidence) -> str:
        prompt = (
            "Rewrite the following farm evidence as one concise, plain-language "
            "explanation for a farm manager. Use ONLY the facts given below - do "
            "not invent observations, confidence, or actions not listed.\n\n"
            f"Entity: {evidence.entity_label}\n"
            f"Observations: {evidence.observations}\n"
            f"Confidence: {evidence.confidence_band} ({evidence.confidence_score:.2f})\n"
            f"Suggested action: {evidence.suggested_action}\n"
            f"Missing information: {evidence.missing_information or 'none'}\n"
        )
        response = httpx.post(
            f"{self._base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self._api_key}"},
            json={
                "model": self._model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            },
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()


def get_ai_provider() -> AIProvider:
    """RULE-AI-1003: unconfigured/unreachable -> automatic fallback to
    RuleBasedProvider. This is the only factory callers should use, so
    switching providers is always a config change (ADR-010)."""
    settings = get_settings()
    if settings.ai_provider == "openai_compatible" and settings.openai_api_key:
        return OpenAICompatibleProvider(
            base_url=settings.openai_base_url, api_key=settings.openai_api_key, model=settings.openai_model
        )
    return RuleBasedProvider()


def explain_with_fallback(evidence: StructuredEvidence) -> tuple[str, str]:
    provider = get_ai_provider()
    try:
        return provider.explain(evidence), provider.name
    except Exception:
        fallback = RuleBasedProvider()
        return fallback.explain(evidence), fallback.name

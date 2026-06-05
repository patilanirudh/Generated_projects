"""
data_fetcher.py — provides AI benchmark data for the dashboard.

Data sourced from public leaderboards (MMLU, HumanEval, MATH, GSM8K, MT-Bench).
Values are updated periodically; last updated 2025-Q1.
"""

from __future__ import annotations

BENCHMARKS: dict[str, dict[str, float | None]] = {
    "GPT-4o": {
        "MMLU": 88.7,
        "HumanEval": 90.2,
        "MATH": 76.6,
        "GSM8K": 97.2,
        "MT-Bench": 9.2,
    },
    "GPT-4 Turbo": {
        "MMLU": 86.4,
        "HumanEval": 87.1,
        "MATH": 72.6,
        "GSM8K": 96.0,
        "MT-Bench": 9.0,
    },
    "Claude 3.5 Sonnet": {
        "MMLU": 88.3,
        "HumanEval": 92.0,
        "MATH": 71.1,
        "GSM8K": 96.4,
        "MT-Bench": 8.9,
    },
    "Claude 3 Opus": {
        "MMLU": 86.8,
        "HumanEval": 84.9,
        "MATH": 60.1,
        "GSM8K": 95.0,
        "MT-Bench": 9.0,
    },
    "Gemini 1.5 Pro": {
        "MMLU": 85.9,
        "HumanEval": 84.1,
        "MATH": 67.7,
        "GSM8K": 90.8,
        "MT-Bench": 8.9,
    },
    "Llama 3.1 405B": {
        "MMLU": 88.6,
        "HumanEval": 89.0,
        "MATH": 73.8,
        "GSM8K": 96.8,
        "MT-Bench": 8.7,
    },
    "Mistral Large 2": {
        "MMLU": 84.0,
        "HumanEval": 87.2,
        "MATH": 70.0,
        "GSM8K": 93.0,
        "MT-Bench": 8.6,
    },
}

BENCHMARK_META: dict[str, dict[str, str]] = {
    "MMLU": {
        "description": "Massive Multitask Language Understanding — 57-subject knowledge test",
        "unit": "%",
        "higher_is_better": "true",
    },
    "HumanEval": {
        "description": "Code generation — pass@1 on 164 Python problems",
        "unit": "%",
        "higher_is_better": "true",
    },
    "MATH": {
        "description": "Competition mathematics — 5-level difficulty problems",
        "unit": "%",
        "higher_is_better": "true",
    },
    "GSM8K": {
        "description": "Grade-school math word problems",
        "unit": "%",
        "higher_is_better": "true",
    },
    "MT-Bench": {
        "description": "Multi-turn instruction following — GPT-4 judge (0–10 scale)",
        "unit": "/10",
        "higher_is_better": "true",
    },
}


def get_model_list() -> list[str]:
    """Return the list of model names in the dataset."""
    return list(BENCHMARKS.keys())


def get_benchmarks() -> dict:
    """Return data structured for Plotly: one trace per benchmark."""
    benchmark_names = list(BENCHMARK_META.keys())
    model_names = get_model_list()

    traces = []
    for benchmark in benchmark_names:
        scores = [BENCHMARKS[model].get(benchmark) for model in model_names]
        traces.append({
            "name": benchmark,
            "x": model_names,
            "y": scores,
            "type": "bar",
        })

    return {
        "traces": traces,
        "models": model_names,
        "benchmarks": benchmark_names,
        "meta": BENCHMARK_META,
    }


def get_model_details(model_id: str) -> dict | None:
    """Return all benchmark scores for a single model, or None if not found."""
    scores = BENCHMARKS.get(model_id)
    if scores is None:
        return None
    return {
        "model": model_id,
        "scores": scores,
        "meta": BENCHMARK_META,
    }

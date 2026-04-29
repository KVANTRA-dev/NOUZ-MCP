#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculate cosine values for the public S/D/E etalons.

Uses the same mean-centering and spread-normalization logic as server.py.
Requires an OpenAI-compatible embeddings endpoint.

Example:
  EMBED_API_URL=http://127.0.0.1:1234 EMBED_MODEL=text-embedding-granite-embedding-278m-multilingual python scripts/calc_etalons.py
"""

import os
import sys
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EMBED_API_URL = os.getenv("EMBED_API_URL", "http://127.0.0.1:1234/v1").rstrip("/")
if not EMBED_API_URL.endswith("/v1"):
    EMBED_API_URL = f"{EMBED_API_URL}/v1"

EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-granite-embedding-278m-multilingual")

ETALONS = {
    "S": (
        "Methodology for analysing complex objects: feedback loops, "
        "emergent properties, self-regulation, bifurcation points. "
        "Cybernetics, synergetics, dissipative structures, catastrophe "
        "theory, autopoiesis — tools for understanding how the whole "
        "exceeds the sum of its parts. Not data and not code — a way "
        "of thinking about how parts form a whole and why systems "
        "behave non-linearly."
    ),
    "D": (
        "Physics and cosmology: from subatomic particles to the large-scale "
        "structure of the Universe. Lagrangians, curvature tensors, scattering "
        "cross-sections, quarks, bosons, fermions, plasma, vacuum fluctuations, "
        "cosmic microwave background, cosmological constant, decoherence. "
        "Pure science about the nature of matter, energy and spacetime."
    ),
    "E": (
        "Software engineering, machine learning and infrastructure: writing "
        "and debugging code, deployment, containerisation, neural networks, "
        "inference, tokenisation, data serialisation, microservices, CI/CD, "
        "automated testing, refactoring, Git, Docker, Kubernetes, APIs. "
        "The practical discipline of building computational systems from "
        "architecture to production."
    ),
}


def get_embedding(text: str) -> list[float]:
    payload = {"input": text}
    if EMBED_MODEL:
        payload["model"] = EMBED_MODEL
    response = requests.post(f"{EMBED_API_URL}/embeddings", json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]


def cosine(v1: list[float], v2: list[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = sum(a * a for a in v1) ** 0.5
    n2 = sum(b * b for b in v2) ** 0.5
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)


def mean_center(vecs: dict[str, list[float]]) -> dict[str, list[float]]:
    if len(vecs) < 2:
        return vecs
    dim = len(next(iter(vecs.values())))
    mean = [0.0] * dim
    for vector in vecs.values():
        for i in range(dim):
            mean[i] += vector[i]
    mean = [value / len(vecs) for value in mean]
    return {key: [vector[i] - mean[i] for i in range(dim)] for key, vector in vecs.items()}


def spread_percentages(vec: list[float], centered: dict[str, list[float]]) -> tuple[dict[str, float], float]:
    scores = {sign: cosine(vec, etalon_vec) for sign, etalon_vec in centered.items()}
    min_val = min(scores.values())
    max_val = max(scores.values())
    spread = max_val - min_val
    if spread <= 0.05:
        return {key: round(100.0 / len(scores), 1) for key in scores}, spread
    adjusted = {key: value - min_val for key, value in scores.items()}
    total = sum(adjusted.values())
    return {key: round(value / total * 100, 1) for key, value in adjusted.items()}, spread


def print_pairwise(title: str, vecs: dict[str, list[float]]) -> None:
    print(f"\n=== {title} ===")
    signs = sorted(vecs.keys())
    for i, s1 in enumerate(signs):
        for j, s2 in enumerate(signs):
            if i <= j:
                print(f"{s1}<->{s2}: {cosine(vecs[s1], vecs[s2]): .4f}")


def main() -> None:
    print(f"Endpoint: {EMBED_API_URL}")
    print(f"Model: {EMBED_MODEL or '(server default)'}")
    print("\n=== Embeddings ===")
    etalon_vecs = {}
    for sign, text in ETALONS.items():
        vector = get_embedding(text)
        etalon_vecs[sign] = vector
        print(f"{sign}: dim={len(vector)}")

    centered = mean_center(etalon_vecs)
    print_pairwise("Pairwise Cosine (raw)", etalon_vecs)
    print_pairwise("Pairwise Cosine (mean-centered)", centered)

    print("\n=== Spread-normalized self-classification ===")
    for sign in sorted(etalon_vecs.keys()):
        percentages, spread = spread_percentages(etalon_vecs[sign], centered)
        dominant = max(percentages, key=percentages.get)
        print(f"{sign}: {percentages} dominant={dominant} spread={spread:.4f}")


if __name__ == "__main__":
    main()

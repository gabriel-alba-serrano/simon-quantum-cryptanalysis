from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ExperimentResult:
    name: str
    mode: str
    success: bool
    problem: dict[str, Any]
    classical_result: dict[str, Any]
    quantum_result: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AttackResult:
    attack_name: str
    mode: str
    success: bool
    query_count: int
    recovered_relation: str | None
    forgery: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

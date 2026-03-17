from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str) -> ModuleType:
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("relative_path", "argv"),
    [
        ("scripts/run_deutsch_jozsa.py", ["--mode", "statevector"]),
        ("scripts/run_bernstein_vazirani.py", ["--mode", "statevector"]),
        ("scripts/run_qft.py", ["--mode", "statevector"]),
        ("scripts/run_simon.py", ["--mode", "statevector"]),
        ("scripts/run_feistel3_distinguisher.py", ["--mode", "classical"]),
        ("scripts/run_cbc_mac_forgery.py", ["--mode", "classical"]),
    ],
)
def test_script_entrypoints(relative_path: str, argv: list[str]) -> None:
    module = load_module(relative_path)
    assert module.main(argv) == 0

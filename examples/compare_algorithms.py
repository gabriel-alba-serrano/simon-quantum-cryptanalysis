from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from simon_qcrypto.algorithms.bernstein_vazirani.experiments import run_experiment as run_bv
from simon_qcrypto.algorithms.deutsch_jozsa.experiments import run_experiment as run_dj
from simon_qcrypto.algorithms.qft.experiments import run_experiment as run_qft
from simon_qcrypto.algorithms.simon.experiments import run_experiment as run_simon


def main() -> None:
    experiments = [
        run_dj(seed=7),
        run_bv(secret=11, bias=1, seed=11),
        run_qft(basis_state=5, seed=5),
        run_simon(secret=3, seed=13),
    ]
    print(json.dumps([asdict(result) for result in experiments], indent=2, default=str))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from simon_qcrypto.algorithms.simon.experiments import run_experiment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a Simon experiment.")
    parser.add_argument("--mode", choices=("statevector", "shots"), default="statevector")
    parser.add_argument("--input-bits", type=int, default=3)
    parser.add_argument("--output-bits", type=int, default=None)
    parser.add_argument("--secret", type=int, default=3)
    parser.add_argument("--shots", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args(argv)

    result = run_experiment(
        input_bits=args.input_bits,
        output_bits=args.output_bits,
        secret=args.secret,
        seed=args.seed,
        mode=args.mode,
        shots=args.shots,
    )
    print(json.dumps(asdict(result), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

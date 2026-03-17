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

from simon_qcrypto.attacks.feistel3.distinguisher_classical import run as run_classical
from simon_qcrypto.attacks.feistel3.distinguisher_quantum import run as run_quantum


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the toy Feistel-3 distinguisher.")
    parser.add_argument(
        "--mode",
        choices=("classical", "statevector", "shots"),
        default="statevector",
    )
    parser.add_argument("--half-bits", type=int, default=3)
    parser.add_argument("--shots", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args(argv)

    if args.mode == "classical":
        result = run_classical(half_bits=args.half_bits, seed=args.seed)
    else:
        result = run_quantum(
            half_bits=args.half_bits,
            seed=args.seed,
            mode=args.mode,
            shots=args.shots,
        )
    print(json.dumps(asdict(result), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

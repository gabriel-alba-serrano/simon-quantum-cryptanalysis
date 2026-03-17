from __future__ import annotations

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


def main() -> None:
    results = [run_classical(seed=17), run_quantum(seed=17)]
    print(json.dumps([asdict(result) for result in results], indent=2, default=str))


if __name__ == "__main__":
    main()

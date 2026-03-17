from simon_qcrypto.attacks.feistel3.distinguisher_classical import run as run_classical
from simon_qcrypto.attacks.feistel3.distinguisher_quantum import run as run_quantum
from simon_qcrypto.attacks.feistel3.oracle import Feistel3SimonOracle, build_oracle

__all__ = ["Feistel3SimonOracle", "build_oracle", "run_classical", "run_quantum"]

from simon_qcrypto.attacks.cbc_mac.forgery_classical import run as run_classical
from simon_qcrypto.attacks.cbc_mac.forgery_quantum import run as run_quantum
from simon_qcrypto.attacks.cbc_mac.oracle import CBCMACSimonOracle, build_oracle

__all__ = ["CBCMACSimonOracle", "build_oracle", "run_classical", "run_quantum"]

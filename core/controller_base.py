from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseController(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}

    def reset(self):
        pass

    @abstractmethod
    def plan(self, ts_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Args:
          ts_state: 單一路口的狀態（見 sumo_env.collect_tls_state）
        Returns (decision dict) or None:
          {
            "action": "set_phase" | "extend" | "hold" | "preempt",
            "phase": int,
            "duration": float,
            "meta": { ... }
          }
        """
        ...

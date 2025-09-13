from typing import Dict, Any, Optional
from .utils import clamp_duration

class PedController:
    def __init__(self, config: Dict[str, Any]):
        self.base = float(config.get("base_crossing_time", 25))
        self.elderly = float(config.get("elderly_extra_time", 8))
        self.max_t = float(config.get("max_crossing_time", 60))

    def plan(self, ts_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ts_state.get("ped_requests"):
            return None
        duration = self.base
        if ts_state.get("weather", {}).get("condition") in {"rain", "storm"}:
            duration += 5
        if ts_state.get("ped_profile", {}).get("elderly_ratio", 0) > 0.2:
            duration += self.elderly
        duration = clamp_duration(duration, 7, self.max_t)
        # Demo：假定行人相位是固定的某 index（實務應由配時表/衝突矩陣決定）
        ped_phase = ts_state.get("ped_phase", ts_state.get("current_phase", 0))
        return {
            "action": "set_phase",
            "phase": int(ped_phase),
            "duration": float(duration),
            "meta": {"why": "ped demand"}
        }

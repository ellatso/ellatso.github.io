from typing import Dict, Any, Optional
from .utils import clamp_duration

class EmergencyController:
    def __init__(self, config: Dict[str, Any]):
        self.range = float(config.get("detection_range", 500))
        self.lead = float(config.get("clearance_lead_time", 30))
        self.duration = float(config.get("priority_duration", 45))

    def plan(self, ts_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        em = ts_state.get("emergency", {})
        if not em or not em.get("active"):
            return None
        target_phase = em.get("target_phase", ts_state.get("current_phase", 0))
        return {
            "action": "preempt",
            "phase": int(target_phase),
            "duration": clamp_duration(self.duration, 10, 90),
            "meta": {"why": "emergency preemption"}
        }

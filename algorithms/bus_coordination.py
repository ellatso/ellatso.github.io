from typing import Dict, Any, Optional
from .utils import clamp_duration

class BusController:
    def __init__(self, config: Dict[str, Any]):
        self.target_h = float(config.get("target_headway", 180))
        self.max_hold = float(config.get("max_holding_time", 30))
        self.window = float(config.get("punctuality_window", 120))

    def plan(self, ts_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        bus = ts_state.get("bus", {})
        if not bus:
            return None
        eta = bus.get("eta", None)
        hv = bus.get("headway_var", 0.0)
        if eta is None:
            return None
        # Demo 決策：若公車將至且 headway 亂 → 延綠；否則略過
        if eta < 20 and hv > 0.3:
            return {
                "action": "extend",
                "phase": int(ts_state["current_phase"]),
                "duration": clamp_duration(5.0, 2.0, self.max_hold),
                "meta": {"why": "bus anti-bunching", "eta": eta, "hv": hv}
            }
        return None

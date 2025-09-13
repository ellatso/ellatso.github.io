from typing import Dict, Any

class SafetyGuard:
    def __init__(self, cfg: Dict[str, Any]):
        s = cfg.get("safety", {})
        self.min_green = float(s.get("min_green", 7))
        self.max_red = float(s.get("max_red", 120))
        self.min_walk_speed = float(s.get("min_walk_speed", 1.2))
        self.crosswalk_length = float(s.get("crosswalk_length", 12))

    def apply(self, ts_state: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
        # 行人清空條件（若 action 為行人 set_phase，可在 meta 標註 ped=true ）
        if decision["action"] in {"set_phase"} and ts_state.get("ped_requests"):
            clearance = self.crosswalk_length / self.min_walk_speed
            if decision["duration"] < clearance:
                decision["duration"] = clearance
                decision.setdefault("meta", {}).update({"guard": "ped_clearance"})
        # 最短綠（對 extend/set_phase 都套用）
        if decision["action"] in {"extend", "set_phase"}:
            if decision["duration"] < self.min_green:
                decision["duration"] = self.min_green
                decision.setdefault("meta", {}).update({"guard": "min_green"})
        return decision

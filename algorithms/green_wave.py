from typing import Dict, Any, Optional
from .utils import clamp_duration

# 可選：簡單工具；若不想建 utils，可直接搬到此檔。

class GreenWaveController:
    def __init__(self, config: Dict[str, Any]):
        self.cruise = float(config.get("cruise_speed", 13.9))
        self.alpha = float(config.get("offset_smoothing", 0.3))
        self.offset_ewma = {}

    def plan(self, ts_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # 需求：維持幹道方向綠波（此處以當前主相位持續為例）
        tls = ts_state["id"]
        phase = ts_state["current_phase"]
        # Demo：當隊列不高且速度尚可 → 延綠小幅延長；否則不動。
        avg_speed = ts_state.get("avg_speed", 8.0)
        queue = ts_state.get("queue_len", 0)
        if queue < 8 and avg_speed > 6.0:
            return {
                "action": "extend",
                "phase": int(phase),
                "duration": clamp_duration(3.0, 1.0, 10.0),
                "meta": {"why": "maintain green wave"}
            }
        return None

import os, json, time, yaml, logging
from pathlib import Path
from typing import Dict, Any, List, Tuple

from .safety_guard import SafetyGuard
from .arbiter import Arbiter
from algorithms.green_wave import GreenWaveController
from algorithms.pedestrian import PedController
from algorithms.bus_coordination import BusController
from algorithms.emergency import EmergencyController

class TrafficAIDecisionEngine:
    def __init__(self, config_path: str):
        self.cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
        self.logger = logging.getLogger("traffic_ai")
        logging.basicConfig(level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")))
        out = Path("data/outputs"); out.mkdir(parents=True, exist_ok=True)
        self.f_decision = open(out/"decisions.jsonl", "a", encoding="utf-8")
        self.f_events = open(out/"events.log", "a", encoding="utf-8")
        self.f_metrics = open(out/"metrics.csv", "a", encoding="utf-8")
        if self.f_metrics.tell() == 0:
            self.f_metrics.write("t,tls_id,avg_speed,queue_len\n")
            self.f_metrics.flush()
        # 策略器 + 護欄 + 仲裁
        m = self.cfg.get("ai_models", {})
        self.controllers = {
            "emergency": EmergencyController(m.get("emergency", {})),
            "bus":       BusController(m.get("bus_coordination", {})),
            "ped":       PedController(m.get("pedestrian", {})),
            "green":     GreenWaveController(m.get("green_wave", {})),
        }
        self.arbiter = Arbiter(["emergency", "bus", "ped", "green"])
        self.guard = SafetyGuard(self.cfg)

    def decide(self, ts_state: Dict[str, Any]) -> Dict[str, Any]:
        cands: List[Tuple[str, Dict[str, Any]]] = []
        for name, ctrl in self.controllers.items():
            d = ctrl.plan(ts_state)
            if d:
                d = self.guard.apply(ts_state, d)
                cands.append((name, d))
        chosen = self.arbiter.choose(cands)
        if chosen is None:
            return {"action": "noop", "phase": ts_state.get("current_phase", 0), "duration": 0, "meta": {}}
        name, d = chosen
        d = dict(d)
        d.setdefault("meta", {}).update({"controller": name})
        # 記錄
        self.f_decision.write(json.dumps({"t": time.time(), "tls": ts_state["id"], **d}, ensure_ascii=False)+"\n")
        self.f_decision.flush()
        return d

    def record_metrics(self, t: float, tls_id: str, avg_speed: float, queue_len: int):
        self.f_metrics.write(f"{t:.1f},{tls_id},{avg_speed:.3f},{queue_len}\n")
        self.f_metrics.flush()

import os, time
from typing import Dict, Any, List

import traci

class SumoRunner:
    def __init__(self, sumocfg: str, use_gui: bool=False, step_length: float=0.5):
        self.sumocfg = sumocfg
        self.use_gui = use_gui
        self.step_length = step_length
        self._started = False

    def start(self):
        binary = "sumo-gui" if self.use_gui else "sumo"
        traci.start([binary, "-c", self.sumocfg, "--step-length", str(self.step_length)])
        self._started = True

    def step(self):
        traci.simulationStep()

    def close(self):
        if self._started:
            traci.close(False)
            self._started = False

    # ====== 狀態蒐集（簡化 Demo 版） ======
    def tls_ids(self) -> List[str]:
        return list(traci.trafficlight.getIDList())

    def collect_tls_state(self, tls_id: str) -> Dict[str, Any]:
        phase = traci.trafficlight.getPhase(tls_id)
        lanes = traci.trafficlight.getControlledLanes(tls_id)
        # 基本 KPI：隊列/速度（平均）
        q = 0
        sp = []
        for ln in lanes:
            try:
                q += traci.lane.getLastStepHaltingNumber(ln)
                spd = traci.lane.getLastStepMeanSpeed(ln)
                if spd >= 0:
                    sp.append(spd)
            except traci.TraCIException:
                pass
        avg_speed = sum(sp)/len(sp) if sp else 0.0
        # Demo: 行人/公車/緊急 以簡易旗標模擬；實務應由 detector / type 解析
        ts = {
            "id": tls_id,
            "current_phase": phase,
            "queue_len": q,
            "avg_speed": avg_speed,
            "ped_requests": False,
            "ped_phase": phase,  # 假設同相位（示意）
            "bus": {"eta": 30, "headway_var": 0.2},
            "emergency": {"active": False},
            "weather": {"condition": "clear"},
        }
        return ts

    def set_phase(self, tls_id: str, phase: int):
        traci.trafficlight.setPhase(tls_id, int(phase))

    def extend_phase(self, tls_id: str, extra: float):
        # 以 setPhaseDuration 延長當前相位持續時間
        try:
            left = traci.trafficlight.getPhaseDuration(tls_id)
        except Exception:
            left = 0
        traci.trafficlight.setPhaseDuration(tls_id, max(0, left) + extra)

import argparse, time, yaml
from pathlib import Path

from core.sumo_env import SumoRunner
from core.decision_engine import TrafficAIDecisionEngine


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="data/config/system_config.yaml")
    ap.add_argument("--scenario", default="morning_rush", choices=["morning_rush", "bus_bunching", "emergency_event"])
    ap.add_argument("--mode", default="rule", choices=["baseline", "rule"])  # baseline: 不做決策
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    sumo_cfg = cfg["sumo"]

    runner = SumoRunner(
        sumocfg=sumo_cfg.get("sumocfg_file", "data/networks/demo_grid.sumocfg"),
        use_gui=bool(sumo_cfg.get("gui", False)),
        step_length=float(sumo_cfg.get("step_length", 0.5)),
    )
    engine = TrafficAIDecisionEngine(args.config)

    runner.start()
    t0 = time.time(); sim_time = float(sumo_cfg.get("simulation_time", 600))

    try:
        while (time.time() - t0) < sim_time:
            runner.step()
            for tls in runner.tls_ids():
                state = runner.collect_tls_state(tls)
                # 記錄 KPI
                engine.record_metrics(time.time()-t0, tls, state.get("avg_speed", 0.0), state.get("queue_len", 0))
                if args.mode == "rule":
                    d = engine.decide(state)
                    act = d.get("action")
                    if act == "set_phase":
                        runner.set_phase(tls, d["phase"])
                    elif act == "extend":
                        runner.extend_phase(tls, d["duration"])
                    elif act == "preempt":
                        runner.set_phase(tls, d["phase"])
                        runner.extend_phase(tls, d["duration"])
            time.sleep(0.01)
    finally:
        runner.close()

if __name__ == "__main__":
    main()

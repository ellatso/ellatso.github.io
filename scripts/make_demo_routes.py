#!/usr/bin/env python3
import argparse, os, subprocess, sys, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NETS = ROOT / "data" / "networks"
ROUTES = ROOT / "data" / "routes"
NETS.mkdir(parents=True, exist_ok=True)
ROUTES.mkdir(parents=True, exist_ok=True)

TEMPLATE_SUMOCFG = """<configuration>
  <input>
    <net-file value="{net}"/>
    <route-files value="{rou}"/>
  </input>
  <time>
    <begin value="0"/>
    <end value="600"/>
    <step-length value="0.5"/>
  </time>
</configuration>
"""

ROU_TEMPLATE = """<routes>
    <vType id="car" accel="1.0" decel="4.5" sigma="0.5" length="5" maxSpeed="20"/>
    <vType id="bus" accel="0.8" decel="4.0" sigma="0.5" length="12" maxSpeed="18"/>
    <vType id="emergency" accel="1.2" decel="5.0" sigma="0.3" length="6" maxSpeed="25" color="1,0,0"/>
    <!-- 簡單 OD 流量：四角互通 -->
    <route id="r1" edges="edge-west2east"/>
    <route id="r2" edges="edge-east2west"/>
    <route id="r3" edges="edge-north2south"/>
    <route id="r4" edges="edge-south2north"/>
    <flow id="f1" type="car" route="r1" begin="0" end="600" vehsPerHour="600"/>
    <flow id="f2" type="car" route="r2" begin="0" end="600" vehsPerHour="600"/>
    <flow id="f3" type="car" route="r3" begin="0" end="600" vehsPerHour="600"/>
    <flow id="f4" type="car" route="r4" begin="0" end="600" vehsPerHour="600"/>
    <!-- 少量公車與緊急車示意 -->
    <flow id="b1" type="bus" route="r1" begin="0" end="600" vehsPerHour="60"/>
    <flow id="e1" type="emergency" route="r3" begin="120" end="121" number="1"/>
</routes>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", type=int, default=3)
    ap.add_argument("--lanes", type=int, default=2)
    args = ap.parse_args()

    netfile = NETS / "demo_grid.net.xml"
    roufile = ROUTES / "demo_grid.rou.xml"
    sumocfg = NETS / "demo_grid.sumocfg"

    # 1) 產 grid 網路（依賴 netgenerate）
    cmd = [
        "netgenerate", "--grid",
        f"--grid.number={args.grid}",
        f"--default.lanenumber={args.lanes}",
        "--output-file", str(netfile),
        "--default-junctions.tl-type=static"
    ]
    print("[make_net] ", " ".join(cmd))
    subprocess.check_call(cmd)

    # 2) 簡單 routes（示意：單線邊命名可依實際 net 調整）
    # 為了 demo，我們先寫死 4 個方向的 route，真實專案應解析 net.xml 生成 OD。
    roufile.write_text(ROU_TEMPLATE, encoding="utf-8")

    # 3) sumocfg
    sumocfg.write_text(
        TEMPLATE_SUMOCFG.format(net=str(netfile).replace("\\", "/"), rou=str(roufile).replace("\\", "/")),
        encoding="utf-8",
    )
    print("Done:", netfile, roufile, sumocfg)

if __name__ == "__main__":
    sys.exit(main())

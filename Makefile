.PHONY: setup sumo_check net demo web clean

setup:
python -m venv venv && . venv/bin/activate && pip install -r requirements.txt

sumo_check:
@echo $$SUMO_HOME && sumo --version

net:
python scripts/make_demo_routes.py --grid 3 --lanes 2

demo:
python experiments/run_demo.py --scenario morning_rush --mode rule

web:
python web/app.py

clean:
rm -f data/outputs/*.csv data/outputs/*.jsonl data/outputs/*.log || true

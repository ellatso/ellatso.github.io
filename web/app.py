import os, time, threading, csv, json
from pathlib import Path
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')

OUT = Path('data/outputs')
MET = OUT/ 'metrics.csv'
DEC = OUT/ 'decisions.jsonl'

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.get('/api/health')
def health():
    return jsonify(ok=True)

# （選配）可新增 /api/start /api/stop /api/mode /api/scenario 供前端觸發

# 背景執行：輪詢檔案新行 → 推播到前端

def tail_metrics():
    last = 0
    while True:
        try:
            if MET.exists():
                with open(MET, 'r', encoding='utf-8') as f:
                    f.seek(last)
                    for line in f.readlines():
                        if line.startswith('t,'): # header
                            continue
                        try:
                            t, tls, spd, q = line.strip().split(',')
                            socketio.emit('metrics', {
                                't': float(t), 'tls': tls, 'avg_speed': float(spd), 'queue_len': int(q)
                            })
                        except Exception:
                            pass
                    last = f.tell()
        except Exception:
            pass
        time.sleep(0.5)

def tail_decisions():
    last = 0
    while True:
        try:
            if DEC.exists():
                with open(DEC, 'r', encoding='utf-8') as f:
                    f.seek(last)
                    for line in f.readlines():
                        try:
                            payload = json.loads(line)
                            socketio.emit('decision', payload)
                        except Exception:
                            pass
                    last = f.tell()
        except Exception:
            pass
        time.sleep(0.5)

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    threading.Thread(target=tail_metrics, daemon=True).start()
    threading.Thread(target=tail_decisions, daemon=True).start()
    socketio.run(app, host=os.getenv('HOST', '127.0.0.1'), port=int(os.getenv('PORT', '5000')))

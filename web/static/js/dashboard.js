const socket = io();
const statusEl = document.getElementById('status');
const kSpeed = document.getElementById('k_speed');
const kQueue = document.getElementById('k_queue');
const lastDecision = document.getElementById('lastDecision');

let X = [], Y1 = [], Y2 = [];
Plotly.newPlot('chart', [{x:X, y:Y1, name:'Avg Speed'}, {x:X, y:Y2, name:'Queue'}], {margin:{t:20}});

socket.on('connect', () => { statusEl.textContent = 'connected'; });
socket.on('disconnect', () => { statusEl.textContent = 'disconnected'; });

socket.on('metrics', (m) => {
  kSpeed.textContent = m.avg_speed.toFixed(2) + ' m/s';
  kQueue.textContent = String(m.queue_len);
  X.push(m.t); Y1.push(m.avg_speed); Y2.push(m.queue_len);
  if (X.length > 200) { X.shift(); Y1.shift(); Y2.shift(); }
  Plotly.update('chart', {x:[X,X], y:[Y1,Y2]});
});

socket.on('decision', (d) => {
  lastDecision.textContent = JSON.stringify(d, null, 2);
});

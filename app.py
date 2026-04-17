"""
Quasicrystal Scattering Explorer
Scattering amplitude F(k) = |Σ_n exp(i·k·log(p_n))| for primes p_n,
with peaks at Riemann zeta zero imaginary parts γ_m.
"""
import numpy as np
from flask import Flask, request, jsonify, render_template_string
from sympy import primerange
from mpmath import zetazero
import math

app = Flask(__name__)

NUM_ZETA_ZEROS = 60
print(f"Precomputing {NUM_ZETA_ZEROS} Riemann zeta zeros...")
ZETA_ZEROS = [float(zetazero(n).imag) for n in range(1, NUM_ZETA_ZEROS + 1)]
print("Done.")

_prime_cache = {}

def get_log_primes(num_primes):
    # Cache at rounded-up multiples of 500 so nearby slider values reuse the array
    bucket = math.ceil(num_primes / 500) * 500
    if bucket not in _prime_cache:
        primes = list(primerange(2, bucket * 20))[:bucket]
        _prime_cache[bucket] = np.log(np.array(primes, dtype=np.float64))
    return _prime_cache[bucket][:num_primes]


def compute_scattering(num_primes, k_max, n_k_points, window, power):
    log_primes = get_log_primes(num_primes)

    # Hann window: w_n = sin²(π·n/N), suppresses sidelobes
    if window:
        n = np.arange(num_primes, dtype=np.float64)
        weights = np.sin(np.pi * n / (num_primes - 1)) ** 2
        weights /= weights.mean()   # preserve scale
    else:
        weights = np.ones(num_primes, dtype=np.float64)

    k_vals = np.linspace(0.05, k_max, n_k_points)

    # Chunked outer product to keep peak memory ~50 MB
    chunk = max(1, int(50_000_000 // num_primes))
    amplitudes = np.empty(n_k_points, dtype=np.float64)
    for start in range(0, n_k_points, chunk):
        end = min(start + chunk, n_k_points)
        phases = np.outer(k_vals[start:end], log_primes)        # (chunk, N)
        amplitudes[start:end] = np.abs(
            np.dot(np.exp(1j * phases), weights)                # weighted sum over primes
        )

    norm = math.sqrt(num_primes)
    amplitudes /= norm
    if power:
        amplitudes **= 2   # |F|² sharpens peak contrast

    return k_vals.tolist(), amplitudes.tolist()


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Quasicrystal Scattering Explorer</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0f0f14; color: #e0e0e8; }
  h1 { padding: 18px 24px 4px; font-size: 1.2rem; color: #c8b8ff; letter-spacing: 0.02em; }
  .subtitle { padding: 0 24px 14px; font-size: 0.78rem; color: #7a7a9a; }
  .layout { display: flex; height: calc(100vh - 80px); }
  .sidebar { width: 268px; flex-shrink: 0; padding: 16px; background: #16161f;
             border-right: 1px solid #2a2a3a; overflow-y: auto; }
  .plot-area { flex: 1; min-width: 0; padding: 12px; }
  #plot { width: 100%; height: 100%; }

  .section { margin-bottom: 16px; }
  .section-title { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em;
                   color: #7a7a9a; margin-bottom: 8px; }
  .param { margin-bottom: 12px; }
  label.row { font-size: 0.8rem; color: #b0b0c8; display: flex;
              justify-content: space-between; margin-bottom: 3px; }
  label.row span { color: #c8b8ff; font-weight: 600; min-width: 56px; text-align: right; }
  input[type=range] { width: 100%; accent-color: #8060ff; cursor: pointer; }

  .toggle-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px;
                font-size: 0.8rem; color: #b0b0c8; cursor: pointer; }
  .toggle-row input[type=checkbox] { accent-color: #8060ff; cursor: pointer; width: 14px; height: 14px; }

  /* segmented button group */
  .btn-group { display: flex; gap: 4px; margin-bottom: 10px; }
  .btn-group button { flex: 1; padding: 5px 0; background: #22222e; border: 1px solid #3a3a4a;
                      border-radius: 4px; color: #8888aa; font-size: 0.75rem; cursor: pointer;
                      transition: background 0.12s, color 0.12s; }
  .btn-group button.active { background: #5040c0; border-color: #7060e0; color: #fff; }

  .compute-btn { width: 100%; padding: 10px; background: #5040c0; border: none; border-radius: 6px;
                 color: #fff; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: background 0.15s; }
  .compute-btn:hover { background: #6050e0; }
  .compute-btn:disabled { background: #333345; color: #666; cursor: not-allowed; }

  .status { font-size: 0.75rem; margin-top: 8px; min-height: 18px; text-align: center; }
  .status.running { color: #f0c040; }
  .status.done    { color: #60d080; }
  .status.error   { color: #f06060; }

  .info-box { background: #1c1c28; border: 1px solid #2a2a3a; border-radius: 6px;
              padding: 10px 12px; font-size: 0.72rem; color: #777; margin-top: 12px; line-height: 1.65; }
  .info-box b { color: #b0b0c8; }
  .warn { color: #f0a040; font-size: 0.71rem; margin-top: 4px; min-height: 15px; }

  hr.sep { border: none; border-top: 1px solid #2a2a3a; margin: 12px 0; }
</style>
</head>
<body>
<h1>Quasicrystal Scattering Explorer</h1>
<div class="subtitle">F(k) = |Σ p<sub>n</sub><sup>ik</sup>| / √L &nbsp;·&nbsp; peaks at Riemann ζ zeros &nbsp;·&nbsp; zoom &amp; pan with mouse</div>

<div class="layout">
  <div class="sidebar">

    <div class="section">
      <div class="section-title">Supercell Size</div>
      <div class="param">
        <label class="row">Primes (L) <span id="np_val">1000</span></label>
        <input type="range" id="num_primes" min="100" max="10000" step="100" value="1000"
               oninput="syncSlider('num_primes','np_val',this.value)">
      </div>
    </div>

    <div class="section">
      <div class="section-title">k-Space Mesh</div>
      <div class="param">
        <label class="row">k<sub>max</sub> <span id="kmax_val">60</span></label>
        <input type="range" id="k_max" min="10" max="200" step="5" value="60"
               oninput="syncSlider('k_max','kmax_val',this.value)">
      </div>
      <div class="param">
        <label class="row">k-points <span id="nk_val">1200</span></label>
        <input type="range" id="n_k" min="200" max="5000" step="100" value="1200"
               oninput="syncSlider('n_k','nk_val',this.value)">
      </div>
    </div>

    <hr class="sep">

    <div class="section">
      <div class="section-title">Spectrum Mode</div>
      <div class="btn-group">
        <button id="mode_amp" class="active" onclick="setMode('amp')">|F(k)|</button>
        <button id="mode_pow" onclick="setMode('pow')">|F(k)|²</button>
      </div>
      <div class="section-title" style="margin-top:6px">Y-axis Scale</div>
      <div class="btn-group">
        <button id="scale_lin" class="active" onclick="setScale('lin')">Linear</button>
        <button id="scale_log" onclick="setScale('log')">Log</button>
      </div>
    </div>

    <div class="section">
      <div class="section-title">Signal Processing</div>
      <label class="toggle-row">
        <input type="checkbox" id="use_window">
        Hann window (reduce sidelobes)
      </label>
      <label class="toggle-row">
        <input type="checkbox" id="show_zeros" checked>
        Show ζ zeros
      </label>
    </div>

    <div id="warn" class="warn"></div>
    <button class="compute-btn" id="btn" onclick="compute()">Compute</button>
    <div id="status" class="status"></div>

    <div class="info-box">
      <b>Peak width</b> ~ 2π / log(p<sub>L</sub>)<br>
      L=1000 → width ≈ 0.91 &nbsp;|&nbsp; L=5000 → ≈ 0.58<br>
      <b>|F|²</b> compresses background, sharpens peaks.<br>
      <b>Hann window</b> kills sidelobe ringing.<br><br>
      <b>Zoom:</b> scroll or box-select<br>
      <b>Pan:</b> click-drag &nbsp; <b>Reset:</b> double-click
    </div>

  </div>

  <div class="plot-area">
    <div id="plot"></div>
  </div>
</div>

<script>
const ZETA_ZEROS = {{ zeta_zeros | tojson }};
let currentMode  = 'amp';
let currentScale = 'lin';
let lastData = null;
let lastParams = null;
let computeRev = 0;   // increments on each new Compute → resets zoom

function syncSlider(sliderId, labelId, val) {
  document.getElementById(labelId).textContent = val;
  updateWarn();
}

function setMode(m) {
  currentMode = m;
  document.getElementById('mode_amp').classList.toggle('active', m === 'amp');
  document.getElementById('mode_pow').classList.toggle('active', m === 'pow');
  if (lastData) redraw();
}

function setScale(s) {
  currentScale = s;
  document.getElementById('scale_lin').classList.toggle('active', s === 'lin');
  document.getElementById('scale_log').classList.toggle('active', s === 'log');
  if (lastData) redraw();
}

function updateWarn() {
  const np = +document.getElementById('num_primes').value;
  const nk = +document.getElementById('n_k').value;
  const ops = np * nk;
  const warn = document.getElementById('warn');
  warn.textContent = ops > 8_000_000
    ? `⚠ ~${(ops/1e6).toFixed(1)}M ops — may take a few seconds`
    : '';
}

function compute() {
  const btn = document.getElementById('btn');
  const status = document.getElementById('status');
  btn.disabled = true;
  status.className = 'status running';
  status.textContent = 'Computing…';

  const params = {
    num_primes: +document.getElementById('num_primes').value,
    k_max:      +document.getElementById('k_max').value,
    n_k_points: +document.getElementById('n_k').value,
    window:     document.getElementById('use_window').checked,
    power:      false,   // always return |F|, we square client-side for instant mode switching
  };

  fetch('/compute', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(params),
  })
  .then(r => r.json())
  .then(data => {
    if (data.error) throw new Error(data.error);
    lastData = data;
    lastParams = params;
    computeRev++;
    redraw();
    status.className = 'status done';
    status.textContent = `Done — ${params.n_k_points} pts × ${params.num_primes} primes`;
  })
  .catch(err => {
    status.className = 'status error';
    status.textContent = 'Error: ' + err.message;
  })
  .finally(() => { btn.disabled = false; });
}

function redraw() {
  const { k, amp } = lastData;
  const params = lastParams;
  const k_max = params.k_max;
  const showZeros = document.getElementById('show_zeros').checked;

  // Apply mode client-side so switching is instant
  let y;
  if (currentMode === 'pow') {
    y = amp.map(v => v * v);
  } else {
    y = amp;
  }

  const yLabel = currentMode === 'pow' ? '|F(k)|² / L' : '|F(k)| / √L';
  const titleSuffix = currentMode === 'pow' ? '|F(k)|² / L' : '|F(k)| / √L';
  const winNote = document.getElementById('use_window').checked ? ', Hann window' : '';

  const traces = [{
    x: k, y,
    type: 'scattergl',
    mode: 'lines',
    name: `L = ${params.num_primes} primes${winNote}`,
    line: { color: '#8060ff', width: 1.2 },
  }];

  const shapes = [];
  const annotations = [];

  if (showZeros) {
    const visZeros = ZETA_ZEROS.filter(z => z <= k_max);
    visZeros.forEach((z, i) => {
      shapes.push({
        type: 'line', x0: z, x1: z, y0: 0, y1: 1,
        xref: 'x', yref: 'paper',
        line: { color: 'rgba(255,80,80,0.45)', width: 1, dash: 'dot' },
      });
      if (i < 8) {
        annotations.push({
          x: z, y: 1.025, xref: 'x', yref: 'paper',
          text: `γ<sub>${i+1}</sub>`, showarrow: false,
          font: { size: 9, color: '#ff8080' }, yanchor: 'bottom',
        });
      }
    });
    traces.push({
      x: visZeros,
      y: new Array(visZeros.length).fill(currentScale === 'log' ? null : 0),
      type: 'scatter', mode: 'markers',
      name: 'ζ zeros (γ)',
      marker: { color: '#ff4040', symbol: 'x', size: 7, line: { width: 1.5 } },
    });
  }

  const layout = {
    paper_bgcolor: '#0f0f14',
    plot_bgcolor:  '#13131c',
    font: { color: '#c0c0d0', family: 'Segoe UI, system-ui, sans-serif' },
    title: {
      text: `${titleSuffix}  (L = ${params.num_primes} primes${winNote})`,
      font: { size: 13, color: '#c8b8ff' },
    },
    xaxis: {
      title: 'k', fixedrange: false,
      gridcolor: '#1e1e2e', zerolinecolor: '#2a2a3a', color: '#8888aa',
    },
    yaxis: {
      title: yLabel, fixedrange: false,
      type: currentScale === 'log' ? 'log' : 'linear',
      gridcolor: '#1e1e2e', zerolinecolor: '#2a2a3a', color: '#8888aa',
    },
    legend: { bgcolor: 'rgba(0,0,0,0.4)', bordercolor: '#2a2a3a', borderwidth: 1 },
    shapes, annotations,
    margin: { t: 48, b: 48, l: 64, r: 20 },
    hovermode: 'x unified',
    // uirevision: stable across mode/scale switches so zoom is preserved;
    // changes only when new data is computed, which resets the viewport.
    uirevision: computeRev,
  };

  Plotly.react('plot', traces, layout, {
    responsive: true, scrollZoom: true, displayModeBar: true,
    modeBarButtonsToRemove: ['lasso2d', 'select2d'],
  });
}

updateWarn();
compute();
</script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML, zeta_zeros=ZETA_ZEROS)


@app.route('/compute', methods=['POST'])
def compute():
    try:
        data = request.get_json()
        num_primes = max(100,  min(int(data.get('num_primes', 1000)), 10000))
        k_max      = max(5,    min(float(data.get('k_max', 60)),      300))
        n_k_points = max(200,  min(int(data.get('n_k_points', 1200)), 5000))
        window     = bool(data.get('window', False))

        k_vals, amplitudes = compute_scattering(num_primes, k_max, n_k_points, window, power=False)
        return jsonify(k=k_vals, amp=amplitudes)
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(port=5004, debug=False)

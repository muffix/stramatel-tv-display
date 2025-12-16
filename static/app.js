const el = (id) => document.getElementById(id);

const clockEl = el('clock');
const homeEl = el('home');
const awayEl = el('away');
const periodEl = el('period');
const runDotEl = el('runDot');

const homeTimeoutsEl = el('homeTimeouts');
const awayTimeoutsEl = el('awayTimeouts');

const homePenaltiesEl = el('homePenalties');
const awayPenaltiesEl = el('awayPenalties');

function renderTimeouts(container, count) {
  const n = parseInt(count ?? 0, 10);
  if (!Number.isFinite(n) || n <= 0) {
    container.classList.add('hidden');
    container.innerHTML = '';
    return;
  }
  container.classList.remove('hidden');
  container.innerHTML = Array.from({ length: n }, () => `<span class="timeoutIcon">⏱</span>`).join('');
}

function renderPenalties(container, active, clocks) {
  const act = Array.isArray(active) ? active : [];
  const cls = Array.isArray(clocks) ? clocks : [];

  const lines = act.map((n) => {
    const clk = cls[n - 1] ?? null; // n is 1..3
    return `${clk ?? '--:--'}`;
  });

  if (lines.length === 0) {
    container.classList.add('hidden');
    container.innerHTML = '';
    return;
  }

  container.classList.remove('hidden');
  container.innerHTML = lines.map(t => `<div class="penaltyLine">${t}</div>`).join('');
}

async function tick() {
  try {
    const r = await fetch('/state', { cache: 'no-store' });
    const s = await r.json();
    if (!s.ok) return;

    clockEl.textContent = s.clock ?? '--:--';
    homeEl.textContent = s.home?.score ?? '--';
    awayEl.textContent = s.away?.score ?? '--';
    periodEl.textContent = s.period ?? '-';

    runDotEl.className = 'dot ' + (s.running ? 'on' : 'off');

    renderTimeouts(homeTimeoutsEl, s.home?.timeouts);
    renderTimeouts(awayTimeoutsEl, s.away?.timeouts);

    renderPenalties(homePenaltiesEl, s.home?.penalties_active, s.home?.penalty_clocks);
    renderPenalties(awayPenaltiesEl, s.away?.penalties_active, s.away?.penalty_clocks);
  } catch (e) {
    // Optional: uncomment for debugging
    // console.error(e);
  }
}

setInterval(tick, 100);
tick();

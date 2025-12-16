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
  // Always make container participate in layout
  container.classList.remove('hidden');

  const n = parseInt(count ?? 0, 10);
  if (container.children.length !== 1) {
    container.innerHTML = '';
    const span = document.createElement('span');
    span.className = 'timeoutIcon';
    span.textContent = '⏱';
    container.appendChild(span);
  }

  const child = container.firstElementChild;
  const show = Number.isFinite(n) && n >= 1;
  child.classList.toggle('inactive', !show);
}

function renderPenalties(container, active, clocks) {
  // Always make container participate in layout
  container.classList.remove('hidden');

  const act = Array.isArray(active) ? active : [];
  const cls = Array.isArray(clocks) ? clocks : [];
  const slots = 3;

  // Ensure fixed number of rows
  if (container.children.length !== slots) {
    container.innerHTML = '';
    for (let i = 0; i < slots; i += 1) {
      const div = document.createElement('div');
      div.className = 'penaltyLine';
      div.textContent = '--:--';
      container.appendChild(div);
    }
  }

  [...container.children].forEach((child, idx) => {
    const slotNum = idx + 1;
    const isActive = act.includes(slotNum);
    const val = cls[slotNum - 1] ?? '--:--';
    child.textContent = val;
    child.classList.toggle('inactive', !isActive);
  });
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

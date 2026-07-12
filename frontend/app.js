// ===== ANIMATED STARS BACKGROUND =====
const canvas = document.getElementById('stars-canvas');
const ctx = canvas.getContext('2d');
let stars = [];
let shootingStars = [];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

function createStars(count) {
  stars = [];
  for (let i = 0; i < count; i++) {
    stars.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random() * 0.8 + 0.2,
      twinkleSpeed: Math.random() * 0.02 + 0.005,
      twinklePhase: Math.random() * Math.PI * 2,
    });
  }
}

function createShootingStar() {
  return {
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height * 0.3,
    length: Math.random() * 80 + 40,
    speed: Math.random() * 6 + 4,
    angle: Math.PI / 4 + (Math.random() - 0.5) * 0.3,
    opacity: 1,
    life: 1,
  };
}

function drawStars() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  stars.forEach(star => {
    const twinkle = Math.sin(Date.now() * star.twinkleSpeed + star.twinklePhase) * 0.3 + 0.7;
    const alpha = star.opacity * twinkle;
    ctx.beginPath();
    ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(248, 250, 252, ${alpha})`;
    ctx.fill();

    if (star.size > 1.5) {
      ctx.beginPath();
      ctx.arc(star.x, star.y, star.size * 3, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(6, 182, 212, ${alpha * 0.08})`;
      ctx.fill();
    }
  });

  shootingStars = shootingStars.filter(star => star.life > 0);
  shootingStars.forEach(star => {
    const endX = star.x + Math.cos(star.angle) * star.length;
    const endY = star.y + Math.sin(star.angle) * star.length;

    const gradient = ctx.createLinearGradient(star.x, star.y, endX, endY);
    gradient.addColorStop(0, `rgba(248, 250, 252, ${star.opacity})`);
    gradient.addColorStop(0.3, `rgba(6, 182, 212, ${star.opacity * 0.6})`);
    gradient.addColorStop(1, `rgba(248, 250, 252, 0)`);

    ctx.beginPath();
    ctx.moveTo(star.x, star.y);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(star.x, star.y, 3, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(248, 250, 252, ${star.opacity * 0.8})`;
    ctx.fill();

    star.x += Math.cos(star.angle) * star.speed;
    star.y += Math.sin(star.angle) * star.speed;
    star.life -= 0.005;
    star.opacity = star.life;
  });

  if (Math.random() < 0.002 && shootingStars.length < 3) {
    shootingStars.push(createShootingStar());
  }

  requestAnimationFrame(drawStars);
}

resizeCanvas();
createStars(200);
drawStars();

window.addEventListener('resize', () => {
  resizeCanvas();
  createStars(200);
});

// ===== API Configuration =====
const API_BASE_URL = 'http://localhost:8000';

// ===== DOM Elements =====
const form = document.getElementById('trip-form');
const formSection = document.getElementById('form-section');
const agentProgressSection = document.getElementById('agent-progress-section');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');
const submitBtn = document.getElementById('submit-btn');
const btnText = submitBtn.querySelector('.btn-text');
const btnLoader = submitBtn.querySelector('.btn-loader');

const summaryGrid = document.getElementById('summary-grid');
const travelBody = document.getElementById('travel-body');
const hotelBody = document.getElementById('hotel-body');
const foodBody = document.getElementById('food-body');
const activitiesBody = document.getElementById('activities-body');
const finalPlanBody = document.getElementById('final-plan-body');

// Preference chips
const preferenceChips = document.getElementById('preference-chips');
const preferenceInput = document.getElementById('preference-input');
const preferenceTags = document.getElementById('preference-tags');
let selectedPreferences = [];

// ===== Preference Chips Logic =====
function addPreference(value) {
  const label = value.charAt(0).toUpperCase() + value.slice(1);
  if (!selectedPreferences.includes(value)) {
    selectedPreferences.push(value);
    renderChips();
  }
}

function removePreference(value) {
  selectedPreferences = selectedPreferences.filter(p => p !== value);
  renderChips();
  // Also deselect tag
  document.querySelectorAll('.tag').forEach(tag => {
    if (tag.dataset.value === value) tag.classList.remove('selected');
  });
}

function renderChips() {
  preferenceChips.innerHTML = selectedPreferences.map(p =>
    `<span class="chip">${p.charAt(0).toUpperCase() + p.slice(1)}
      <button type="button" class="chip-remove" data-value="${p}">✕</button>
    </span>`
  ).join('');

  document.querySelectorAll('.chip-remove').forEach(btn => {
    btn.addEventListener('click', () => removePreference(btn.dataset.value));
  });
}

// Tag click handler
preferenceTags.addEventListener('click', (e) => {
  const tag = e.target.closest('.tag');
  if (!tag) return;
  const value = tag.dataset.value;
  tag.classList.toggle('selected');
  if (tag.classList.contains('selected')) {
    addPreference(value);
  } else {
    removePreference(value);
  }
});

// Free-text input handler
preferenceInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    const value = preferenceInput.value.trim().toLowerCase();
    if (value && !selectedPreferences.includes(value)) {
      addPreference(value);
      preferenceInput.value = '';
    }
  }
});

// ===== Utility Functions =====
function formatCurrency(amount) {
  return '₹' + Number(amount).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

function formatDate(dateStr) {
  if (!dateStr) return 'N/A';
  return dateStr;
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function showSection(section) {
  [formSection, agentProgressSection, resultsSection, errorSection].forEach(s => {
    s.style.display = 'none';
  });
  section.style.display = 'block';
  // Trigger fade-in by re-adding class
  section.classList.remove('fade-in');
  void section.offsetWidth; // reflow
  section.classList.add('fade-in');
}

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  btnText.style.display = isLoading ? 'none' : 'inline-flex';
  btnLoader.style.display = isLoading ? 'inline-flex' : 'none';
}

// ===== Multi-Agent Progress Simulation =====
const AGENTS = [
  { id: 'travel', name: 'Travel Agent', desc: 'Finding routes & fares' },
  { id: 'hotel', name: 'Hotel Agent', desc: 'Searching accommodations' },
  { id: 'food', name: 'Food Agent', desc: 'Discovering restaurants' },
  { id: 'activity', name: 'Activity Agent', desc: 'Finding attractions' },
  { id: 'budget', name: 'Budget Agent', desc: 'Calculating totals' },
];

function resetAgentProgress() {
  document.querySelectorAll('.agent-step').forEach(step => {
    step.className = 'agent-step pending';
    step.querySelector('.step-indicator').textContent = '○';
  });
  document.getElementById('agent-progress-fill').style.width = '0%';
}

function updateAgentProgress(activeIndex) {
  const steps = document.querySelectorAll('.agent-step');
  const total = steps.length;

  steps.forEach((step, i) => {
    step.className = 'agent-step';
    const indicator = step.querySelector('.step-indicator');

    if (i < activeIndex) {
      step.classList.add('completed');
      indicator.textContent = '✓';
    } else if (i === activeIndex) {
      step.classList.add('active');
      indicator.textContent = '⏳';
    } else {
      step.classList.add('pending');
      indicator.textContent = '○';
    }
  });

  const progress = Math.min(((activeIndex) / total) * 100, 100);
  document.getElementById('agent-progress-fill').style.width = progress + '%';
}

function simulateAgentProgress() {
  return new Promise((resolve) => {
    resetAgentProgress();
    let currentAgent = 0;
    updateAgentProgress(0);

    const interval = setInterval(() => {
      currentAgent++;
      if (currentAgent < AGENTS.length) {
        updateAgentProgress(currentAgent);
      } else {
        clearInterval(interval);
        // Mark all completed
        document.querySelectorAll('.agent-step').forEach(step => {
          step.className = 'agent-step completed';
          step.querySelector('.step-indicator').textContent = '✓';
        });
        document.getElementById('agent-progress-fill').style.width = '100%';
        resolve();
      }
    }, 800);
  });
}

// ===== Render Functions =====
function renderSummary(data) {
  summaryGrid.innerHTML = `
    <div class="summary-item">
      <div class="label">Source</div>
      <div class="value">${escapeHtml(data.source || data.destination || 'N/A')}</div>
    </div>
    <div class="summary-item">
      <div class="label">Destination</div>
      <div class="value">${escapeHtml(data.destination || 'N/A')}</div>
    </div>
    <div class="summary-item">
      <div class="label">Travel Date</div>
      <div class="value">${formatDate(data.travel_date)}</div>
    </div>
    <div class="summary-item">
      <div class="label">Budget</div>
      <div class="value">${formatCurrency(data.budget || 0)}</div>
    </div>
    <div class="summary-item">
      <div class="label">Total Cost</div>
      <div class="value">${formatCurrency(data.total_cost || 0)}</div>
    </div>
    <div class="summary-item">
      <div class="label">Within Budget</div>
      <div class="value ${data.within_budget ? 'within-budget' : 'over-budget'}">
        ${data.within_budget ? '✅ Yes' : '❌ No'}
      </div>
    </div>
  `;
}

function renderOptions(container, options, titleKey, detailKeys) {
  if (!options || options.length === 0) {
    container.innerHTML = '<p style="color: var(--text-muted); padding: 8px 0;">No options available.</p>';
    return;
  }

  container.innerHTML = options.map((opt, idx) => {
    const title = opt[titleKey] || `Option ${idx + 1}`;
    const price = opt.price || opt.cost || 0;

    let detailsHtml = '';
    if (detailKeys) {
      detailKeys.forEach(key => {
        if (opt[key] !== undefined && opt[key] !== null && opt[key] !== '') {
          const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
          detailsHtml += `<p><strong>${escapeHtml(label)}:</strong> ${escapeHtml(String(opt[key]))}</p>`;
        }
      });
    }

    const knownKeys = new Set([titleKey, 'price', 'cost', ...(detailKeys || [])]);
    Object.entries(opt).forEach(([key, val]) => {
      if (!knownKeys.has(key) && val !== undefined && val !== null && val !== '') {
        const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        detailsHtml += `<p><strong>${escapeHtml(label)}:</strong> ${escapeHtml(String(val))}</p>`;
      }
    });

    return `
      <div class="option-card">
        <div class="option-header">
          <span class="option-title">${escapeHtml(title)}</span>
          <span class="option-price">${formatCurrency(price)}</span>
        </div>
        <div class="option-details">${detailsHtml}</div>
      </div>
    `;
  }).join('');
}

function renderFinalPlan(plan) {
  if (!plan || Object.keys(plan).length === 0) {
    finalPlanBody.innerHTML = '<p style="color: var(--text-muted);">No itinerary available.</p>';
    return;
  }

  if (typeof plan === 'string') {
    finalPlanBody.innerHTML = `<pre style="white-space: pre-wrap; font-family: inherit; line-height: 1.7;">${escapeHtml(plan)}</pre>`;
    return;
  }

  let html = '';
  Object.entries(plan).forEach(([key, val]) => {
    const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    if (typeof val === 'object' && val !== null) {
      html += `<p><strong>${escapeHtml(label)}:</strong></p>`;
      Object.entries(val).forEach(([k, v]) => {
        const subLabel = k.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        html += `<p style="padding-left: 16px;">• <strong>${escapeHtml(subLabel)}:</strong> ${escapeHtml(String(v))}</p>`;
      });
    } else {
      html += `<p><strong>${escapeHtml(label)}:</strong> ${escapeHtml(String(val))}</p>`;
    }
  });
  finalPlanBody.innerHTML = html;
}

function displayResults(data) {
  renderSummary(data);

  renderOptions(travelBody, data.travel_options, 'mode', ['departure', 'arrival', 'duration', 'provider']);
  if (data.travel_expense) {
    const header = document.querySelector('#travel-card .card-header');
    if (header) {
      header.innerHTML = `<span class="card-icon">🚆</span><h2>Travel Options — Total: ${formatCurrency(data.travel_expense)}</h2>`;
    }
  }

  renderOptions(hotelBody, data.hotel_options, 'name', ['location', 'rating', 'amenities', 'check_in', 'check_out']);
  if (data.hotel_cost) {
    const header = document.querySelector('#hotel-card .card-header');
    if (header) {
      header.innerHTML = `<span class="card-icon">🏨</span><h2>Hotel Options — Total: ${formatCurrency(data.hotel_cost)}</h2>`;
    }
  }

  renderOptions(foodBody, data.food_options, 'cuisine', ['restaurant', 'type', 'meal', 'description']);
  if (data.food_cost) {
    const header = document.querySelector('#food-card .card-header');
    if (header) {
      header.innerHTML = `<span class="card-icon">🍽️</span><h2>Food Options — Total: ${formatCurrency(data.food_cost)}</h2>`;
    }
  }

  renderOptions(activitiesBody, data.activity_options, 'name', ['location', 'duration', 'description', 'type']);
  if (data.activities_cost) {
    const header = document.querySelector('#activities-card .card-header');
    if (header) {
      header.innerHTML = `<span class="card-icon">🎯</span><h2>Activities — Total: ${formatCurrency(data.activities_cost)}</h2>`;
    }
  }

  renderFinalPlan(data.final_plan);

  showSection(resultsSection);
  resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ===== Form Submission =====
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const source = document.getElementById('source').value.trim();
  const destination = document.getElementById('destination').value.trim();
  const travelDate = document.getElementById('travel-date').value.trim();
  const budget = parseFloat(document.getElementById('budget').value);

  if (!source || !destination || !travelDate || isNaN(budget) || selectedPreferences.length === 0) {
    alert('Please fill in all fields and select at least one preference.');
    return;
  }

  const payload = {
    source,
    destination,
    travel_date: travelDate,
    budget,
    preferences: selectedPreferences
  };

  // Show agent progress
  setLoading(true);
  showSection(agentProgressSection);

  // Run agent progress simulation while API call is in flight
  const apiPromise = fetch(`${API_BASE_URL}/plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const agentPromise = simulateAgentProgress();

  try {
    const [response] = await Promise.all([apiPromise, agentPromise]);

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Server error: ${response.status}`);
    }

    const data = await response.json();
    displayResults(data);
  } catch (err) {
    errorMessage.textContent = err.message || 'Failed to connect to the server. Make sure the backend is running.';
    showSection(errorSection);
  } finally {
    setLoading(false);
  }
});

// ===== Button Handlers =====
document.getElementById('retry-btn').addEventListener('click', () => {
  showSection(formSection);
});

document.getElementById('plan-another-btn').addEventListener('click', () => {
  form.reset();
  selectedPreferences = [];
  renderChips();
  document.querySelectorAll('.tag').forEach(tag => tag.classList.remove('selected'));
  showSection(formSection);
  formSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
});

// ===== Initial State =====
showSection(formSection);
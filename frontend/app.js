const opts = (arr) => arr.map((t, i) => [i, t]);
const FIELDS = [
  { k: 'age', l: 'Age (years)', t: 'number', min: 1, max: 120, v: 55 },
  { k: 'sex', l: 'Sex', o: [[0, 'Female'], [1, 'Male']] },
  { k: 'cp', l: 'Chest pain type', o: opts(['Typical angina', 'Atypical angina', 'Non-anginal pain', 'Asymptomatic']) },
  { k: 'trestbps', l: 'Resting blood pressure (mm Hg)', t: 'number', min: 50, max: 250, v: 130 },
  { k: 'chol', l: 'Cholesterol (mg/dl)', t: 'number', min: 80, max: 700, v: 240 },
  { k: 'fbs', l: 'Fasting blood sugar > 120 mg/dl', o: [[0, 'No'], [1, 'Yes']] },
  { k: 'restecg', l: 'Resting ECG', o: opts(['Normal', 'ST-T abnormality', 'LV hypertrophy']) },
  { k: 'thalach', l: 'Max heart rate achieved', t: 'number', min: 40, max: 250, v: 150 },
  { k: 'exang', l: 'Exercise-induced angina', o: [[0, 'No'], [1, 'Yes']] },
  { k: 'oldpeak', l: 'ST depression (oldpeak)', t: 'number', min: 0, max: 10, step: 0.1, v: 1 },
  { k: 'slope', l: 'ST slope', o: opts(['Upsloping', 'Flat', 'Downsloping']) },
  { k: 'ca', l: 'Major vessels colored (0-4)', o: opts(['0', '1', '2', '3', '4']) },
  { k: 'thal', l: 'Thalassemia', o: opts(['Unknown', 'Fixed defect', 'Normal', 'Reversible defect']) },
];

const form = document.getElementById('form');
form.innerHTML = FIELDS.map((f) => {
  const input = f.o
    ? `<select name="${f.k}">${f.o.map(([v, t]) => `<option value="${v}">${t}</option>`).join('')}</select>`
    : `<input name="${f.k}" type="number" min="${f.min}" max="${f.max}" step="${f.step || 1}" value="${f.v}" required>`;
  return `<label>${f.l}${input}</label>`;
}).join('') + '<button type="submit">Predict risk</button>';

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = form.querySelector('button');
  const err = document.getElementById('error');
  err.hidden = true;
  btn.disabled = true;
  const body = {};
  new FormData(form).forEach((v, k) => (body[k] = Number(v)));
  try {
    const r = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!r.ok) throw new Error('Request failed (' + r.status + '): ' + (await r.text()));
    show(await r.json());
  } catch (ex) {
    err.textContent = ex.message;
    err.hidden = false;
  } finally {
    btn.disabled = false;
  }
});

function show(d) {
  const pct = (d.probability * 100).toFixed(1);
  const high = d.prediction === 1;
  document.getElementById('result').hidden = false;
  const label = document.getElementById('label');
  label.textContent = d.label;
  label.className = high ? 'high' : 'low';
  const fill = document.getElementById('fill');
  fill.style.width = pct + '%';
  fill.style.background = high ? '#b3202e' : '#1d7a3a';
  document.getElementById('prob').textContent = 'Model probability of heart disease: ' + pct + '%';
  document.getElementById('factors').innerHTML = d.top_factors
    .map((f) => `<li>${f.feature} (${(f.importance * 100).toFixed(1)}%)</li>`).join('');
}

// script.js (frontend)
const PREDICT_URL = "http://127.0.0.1:8000/predict";
const RECEIPT_URL_BASE = "http://127.0.0.1:8000/receipt/";

const submitBtn = document.getElementById('submitBtn');
const csvInput = document.getElementById('csvFile');
const pdfFileInput = document.getElementById('pdfFile');
const wordInput = document.getElementById('wordFile');
const resultsBody = document.getElementById('resultsBody');

submitBtn.addEventListener('click', async (e) => {
  e.preventDefault();
  const scheme = submitBtn.dataset.scheme;
  if (!scheme || scheme === '') {
    alert('దయచేసి పథకాన్ని ఎంచుకోండి (Please select a scheme).');
    return;
  }
  if (!csvInput || !csvInput.files || csvInput.files.length === 0) {
    alert('దయచేసి CSV ఫైల్ ఎంచుకోండి (Please choose a CSV file).');
    return;
  }

  const fd = new FormData();
  fd.append('file', csvInput.files[0]);
  fd.append('scheme', scheme);

  submitBtn.disabled = true;
  const orig = submitBtn.innerText;
  submitBtn.innerText = 'Generating...';

  try {
    const resp = await fetch(PREDICT_URL, { method: 'POST', body: fd });
    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(text || 'Server error');
    }
    const data = await resp.json();
    renderResults(data.results);
  } catch (err) {
    alert('Error: ' + err.message);
    console.error(err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerText = orig;
  }
});

function renderResults(results) {
  if (!resultsBody) return;
  resultsBody.innerHTML = '';
  results.forEach((r, idx) => {
    const tr = document.createElement('tr');

    const nameTd = document.createElement('td');
    nameTd.textContent = r.applicant_name || '';

    const statusTd = document.createElement('td');
    // Telugu status with English in brackets
    if (r.qualified) {
      statusTd.innerHTML = `పాత్రత (Qualified)`;
      statusTd.className = 'status-approved';
    } else {
      statusTd.innerHTML = `అర్హత లేదు (Not Qualified)`;
      statusTd.className = 'status-rejected';
    }

    const probTd = document.createElement('td');
    probTd.textContent = (r.probability !== null && r.probability !== undefined) ? r.probability : '-';

    const reasonTd = document.createElement('td');
    // reasons are supplied as "Telugu; Telugu (English)" from backend; we will display as-is
    reasonTd.innerHTML = (r.reason_tel_en || '').replace(/\n/g, '<br>');

    const pdfTd = document.createElement('td');
    const a = document.createElement('a');
    a.href = RECEIPT_URL_BASE + idx;
    a.target = '_blank';
    a.textContent = 'Download PDF';
    pdfTd.appendChild(a);

    tr.appendChild(nameTd);
    tr.appendChild(statusTd);
    tr.appendChild(probTd);
    tr.appendChild(reasonTd);
    tr.appendChild(pdfTd);

    resultsBody.appendChild(tr);
  });
}

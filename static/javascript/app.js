function runQuery(queryId) {
  // Show the spinner and reset th e UI
  document.getElementById('spinner').classList.remove('d-none');
  document.getElementById('downloadBtn').classList.add('d-none');
  const output = document.getElementById('outputArea');
  output.innerHTML = '';
  const imgEl = document.getElementById('resultImage');
  imgEl.style.display = 'none';

  fetch('/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query_id: queryId })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      displayResultsAsTable(data.data);
      showImage(queryId);
    } else {
      output.innerHTML =
        `<div class="alert alert-danger">Error: ${data.message}</div>`;
    }
  })
  .catch(() => {
    output.innerHTML =
      `<div class="alert alert-danger">Server error.</div>`;
  })
  .finally(() => {
    document.getElementById('spinner').classList.add('d-none');
  });
}

function displayResultsAsTable(result) {
  const output = document.getElementById('outputArea');
  output.classList.remove('fade-in');

  if (!result || (Array.isArray(result) && result.length === 0)) {
    output.innerHTML = '<p>No data found.</p>';
    output.classList.add('fade-in');
    return;
  }

  const rows = Array.isArray(result) ? result : [ result ];
  const keys = Object.keys(rows[0]);
  let html = '<div class="table-responsive"><table class="table table-striped">';
  html += '<thead><tr>' + keys.map(k => `<th>${k}</th>`).join('') + '</tr></thead><tbody>';
  rows.forEach(row => {
    html += '<tr>' + keys.map(k => `<td>${row[k]}</td>`).join('') + '</tr>';
  });
  html += '</tbody></table></div>';

  output.innerHTML = html;
  output.classList.add('fade-in');
  addDownloadButton(rows);
}

function addDownloadButton(data) {
  const btn = document.getElementById('downloadBtn');
  const keys = Object.keys(data[0]);
  const csv = [ keys.join(',') ].concat(
    data.map(row => keys.map(k => row[k]).join(',')) 
  ).join('\n');

  const blob = new Blob([csv], { type: 'text/csv' });
  btn.href = URL.createObjectURL(blob);
  btn.classList.remove('d-none');
}

function showImage(queryId) {
  const imageMap = {
    '1': 'smokers.jpg',            '2': 'heart_disease.jpg',
    '3': 'gender_stroke.jpg',      '4': 'smoking_habits.jpg',
    '5': 'urban_rural.jpg',        '6': 'dietary_habits.jpg',
    '7': 'hypertension_stroke.jpg','8': 'hypertension_status.jpg',
    '9': 'heart_disease_patients.jpg','10': 'descriptive_stats.jpg',
    '11': 'sleep_analysis.jpg'
  };
  const imgEl = document.getElementById('resultImage');
  const file  = imageMap[queryId];
  if (file) {
    imgEl.src = `/static/images/${file}`;
    imgEl.style.display = 'block';
    imgEl.classList.remove('fade-in');
    void imgEl.offsetWidth;  // to restart the animation
    imgEl.classList.add('fade-in');
  }
}

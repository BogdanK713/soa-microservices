

const Papa = require('papaparse');

// helper: čitanje raw tijela ako je text/plain
function readRawBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.setEncoding('utf8');
    req.on('data', chunk => (data += chunk));
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Only POST' });
  }

  // 1) uzmi CSV iz raw body-ja (text/plain) ili iz JSON-a { csv: "..." }
  let csvText = '';

  const contentType = (req.headers['content-type'] || '').toLowerCase();
  if (contentType.startsWith('text/plain')) {
    csvText = await readRawBody(req);
  } else {
    // Vercel kod JSON-a već parsira u req.body
    if (req.body && typeof req.body.csv === 'string') {
      csvText = req.body.csv;
    } else if (typeof req.body === 'string') {
      csvText = req.body; // fallback
    }
  }

  if (!csvText || !csvText.trim()) {
    return res
      .status(400)
      .json({ error: 'Provide CSV as raw text/plain body or JSON { csv: "..." }' });
  }

  // 2) Parse CSV
  const parsed = Papa.parse(csvText, { header: true, skipEmptyLines: true });
  if (parsed.errors && parsed.errors.length) {
    return res.status(400).json({
      error: 'CSV parse error',
      details: parsed.errors.slice(0, 3)
    });
  }
  const rows = parsed.data || [];

  // 3) Agregacije
  const byDate = {};
  const revenueByDate = {};
  const topLocations = {};
  const topServices = {};

  for (const r of rows) {
    const date = String(r.date || '').trim();
    const amount = parseFloat(r.amount || '0') || 0;
    const location = (r.location || 'UNKNOWN').trim() || 'UNKNOWN';
    const service = (r.service || 'UNKNOWN').trim() || 'UNKNOWN';

    if (date) {
      byDate[date] = (byDate[date] || 0) + 1;
      revenueByDate[date] = (revenueByDate[date] || 0) + amount;
    }
    topLocations[location] = (topLocations[location] || 0) + 1;
    topServices[service] = (topServices[service] || 0) + 1;
  }

  const topN = (obj, n = 5) =>
    Object.entries(obj)
      .sort((a, b) => b[1] - a[1])
      .slice(0, n)
      .map(([key, count]) => ({ key, count }));

  // 4) Odgovor
  return res.status(200).json({
    records: rows.length,
    byDate,
    revenueByDate,
    topLocations: topN(topLocations, 5),
    topServices: topN(topServices, 5)
  });
};

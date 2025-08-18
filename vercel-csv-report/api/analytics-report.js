// api/analytics-report.js
// Fetches data from Analytics service and returns CSV or JSON.
// Usage: GET /api/analytics-report?source=revenue-by-service&format=csv
// Sources: reservations-per-month | revenue-by-service | reservations-by-location | top-users

const DEFAULT_BASES = [
  process.env.ANALYTICS_BASE_URL,              // preferred (set in env)
  "http://localhost:8000/analytics",           // local dev
  "http://analytics-service:8000/analytics",   // docker internal (if ever used inside same network)
].filter(Boolean);

function pickBase() {
  return DEFAULT_BASES[0];
}

function toCSV(rows) {
  if (!Array.isArray(rows)) rows = [];
  // collect union of keys across rows
  const headers = Array.from(rows.reduce((set, row) => {
    Object.keys(row || {}).forEach(k => set.add(k));
    return set;
  }, new Set())).sort();

  const escape = (v) => {
    if (v === null || v === undefined) return "";
    const s = String(v);
    if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
    return s;
  };

  const headerLine = headers.join(",");
  const lines = rows.map(r => headers.map(h => escape(r[h])).join(","));
  return [headerLine, ...lines].join("\n");
}

module.exports = async (req, res) => {
  try {
    // CORS (handy if you call this directly from the browser)
    res.setHeader("Access-Control-Allow-Origin", "*");
    if (req.method === "OPTIONS") {
      res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS");
      res.setHeader("Access-Control-Allow-Headers", "Content-Type,Authorization");
      return res.status(204).end();
    }

    if (req.method !== "GET") {
      return res.status(405).json({ ok: false, error: "Method Not Allowed" });
    }

    const source = String(req.query.source || "").trim();
    const format = String(req.query.format || "csv").toLowerCase();

    const allowed = new Set([
      "reservations-per-month",
      "revenue-by-service",
      "reservations-by-location",
      "top-users",
    ]);
    if (!allowed.has(source)) {
      return res.status(400).json({
        ok: false,
        error: "Invalid 'source'. Allowed: reservations-per-month | revenue-by-service | reservations-by-location | top-users",
      });
    }

    const base = pickBase();
    const url = `${base.replace(/\/+$/, "")}/${source}`;
    const r = await fetch(url, { method: "GET", headers: { "Accept": "application/json" } });
    if (!r.ok) {
      const txt = await r.text().catch(() => "");
      return res.status(502).json({ ok: false, error: `Analytics upstream ${r.status}`, details: txt.slice(0, 500) });
    }
    const data = await r.json();

    if (format === "json") {
      return res.status(200).json({ ok: true, source, data });
    }

    // default: CSV
    const csv = toCSV(Array.isArray(data) ? data : []);
    const now = new Date();
    const stamp = now.toISOString().replace(/[:T]/g, "-").slice(0, 19);
    res.setHeader("Content-Type", "text/csv; charset=utf-8");
    res.setHeader("Content-Disposition", `attachment; filename="${source}-${stamp}.csv"`);
    return res.status(200).send(csv);
  } catch (e) {
    return res.status(500).json({ ok: false, error: String(e && e.message || e) });
  }
};

const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const { listEvents, createEvent, deleteEvent } = require('./google');
const path = require('path');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const app = express();

// CORS + log
app.use(cors());
app.use(morgan('tiny'));

// --- Swagger UI & OpenAPI ---
const openapi = YAML.load(path.join(__dirname, 'docs', 'openapi.yaml'));
app.use('/docs', swaggerUi.serve, swaggerUi.setup(openapi));
app.get('/openapi.yaml', (_req, res) => {
  res.type('text/yaml').send(YAML.stringify(openapi, 10, 2));
});
app.get('/openapi.json', (_req, res) => res.json(openapi));

// Uvijek popuni req.rawBody, a req.body ako je validan JSON.
app.use((req, res, next) => {
  let data = '';
  req.setEncoding('utf8');

  // samo za metode koje mogu imati tijelo
  const method = (req.method || 'GET').toUpperCase();
  const mayHaveBody = method === 'POST' || method === 'PUT' || method === 'PATCH' || method === 'DELETE';
  if (!mayHaveBody) return next();

  req.on('data', chunk => { data += chunk; });
  req.on('end', () => {
    req.rawBody = data;
    req.body = undefined;           // namjerno undefined dok ne odlučimo

    const ctype = (req.headers['content-type'] || '').toLowerCase();
    if (ctype.includes('application/json')) {
      if (data && data.trim()) {
        try {
          req.body = JSON.parse(data);
        } catch {
          // NE vraćamo 400 ovdje – rute će same validirati ili fallbackati na rawBody
          req.body = undefined;
          req.jsonParseError = true;
        }
      } else {
        req.body = {}; // prazan JSON body je ok
      }
    }
    // ako je text/plain ili nešto treće – ostavi body = undefined, rawBody je dostupan
    return next();
  });

  req.on('error', (err) => {
    // čak i u slučaju greške, nastavi – rute će znati reći korisniku šta fali
    req.rawBody = req.rawBody || '';
    req.body = req.body || undefined;
    req.bodyReadError = String(err && err.message || err);
    return next();
  });
});

// Root & health
app.get('/', (_req, res) => res.json({ ok: true, service: 'calendar-service' }));
app.get('/health', (_req, res) => res.json({ status: 'ok' }));

// Diag: vidi šta je stvarno stiglo
app.post('/echo', (req, res) => {
  res.json({
    ok: true,
    note: 'If body was invalid JSON with application/json, jsonParseError=true',
    jsonParseError: !!req.jsonParseError,
    bodyReadError: req.bodyReadError || null,
    received: req.body,
    raw: req.rawBody || null,
    headers: req.headers,
  });
});

// GET /events – lista
app.get('/events', async (req, res) => {
  try {
    const items = await listEvents({
      timeMin: req.query.timeMin,
      timeMax: req.query.timeMax,
      maxResults: req.query.maxResults ? Number(req.query.maxResults) : undefined,
      q: req.query.q,
    });
    res.json({ ok: true, items });
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

// POST /events – kreiraj
app.post('/events', async (req, res) => {
  try {
    let payload = req.body;

    // fallback: ako Content-Type nije JSON ili je parse pao, probaj rawBody kao JSON
    if (!payload || typeof payload !== 'object') {
      if (req.rawBody && req.rawBody.trim().startsWith('{')) {
        try {
          payload = JSON.parse(req.rawBody);
        } catch {
          return res.status(400).json({ ok: false, error: 'Invalid JSON in request body' });
        }
      } else {
        return res.status(400).json({ ok: false, error: 'Missing JSON body' });
      }
    }

    const data = await createEvent(payload);
    res.status(201).json({ ok: true, event: data });
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

// DELETE /events/:id – obriši
app.delete('/events/:id', async (req, res) => {
  try {
    const data = await deleteEvent(req.params.id);
    res.json(data);
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

// Uniform 404 JSON
app.use((req, res) => res.status(404).json({ ok: false, error: 'Not Found' }));

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`calendar-service listening on :${PORT}`));

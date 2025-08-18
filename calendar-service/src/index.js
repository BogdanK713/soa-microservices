// calendar-service/src/index.js
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const path = require('path');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const { listEvents, createEvent, deleteEvent } = require('./google');
const { mountGraphQL } = require('./graphql/mount');

const app = express();

// CORS + logs
app.use(cors());
app.use(morgan('tiny'));

// ---- Swagger UI & OpenAPI ----
const openapi = YAML.load(path.join(__dirname, 'docs', 'openapi.yaml'));
app.use('/docs', swaggerUi.serve, swaggerUi.setup(openapi));
app.get('/openapi.yaml', (_req, res) => {
  // yamljs stringify
  res.type('text/yaml').send(YAML.stringify(openapi, 10, 2));
});
app.get('/openapi.json', (_req, res) => res.json(openapi));

// ---- JSON body for REST (safe, standard) ----
app.use(express.json({ limit: '1mb' }));

// ---- Optional: your previous raw-body helper, but SKIP /graphql completely ----
app.use((req, res, next) => {
  // Let Apollo fully control /graphql requests (GET and POST)
  if ((req.path || '').startsWith('/graphql')) return next();

  // For other routes, retain your tolerant behavior
  let data = '';
  req.setEncoding('utf8');

  const method = (req.method || 'GET').toUpperCase();
  const mayHaveBody = method === 'POST' || method === 'PUT' || method === 'PATCH' || method === 'DELETE';
  if (!mayHaveBody) return next();

  req.on('data', chunk => { data += chunk; });
  req.on('end', () => {
    req.rawBody = data;
    // If content-type says JSON but body is invalid, leave req.body undefined;
    // downstream handlers can check req.jsonParseError and fall back to rawBody if needed.
    const ctype = (req.headers['content-type'] || '').toLowerCase();
    if (ctype.includes('application/json')) {
      if (data && data.trim()) {
        try {
          req.body = JSON.parse(data);
        } catch {
          req.body = undefined;
          req.jsonParseError = true;
        }
      } else {
        req.body = {};
      }
    }
    return next();
  });

  req.on('error', (err) => {
    req.rawBody = req.rawBody || '';
    req.body = req.body || undefined;
    req.bodyReadError = String((err && err.message) || err);
    return next();
  });
});

// Root & health
app.get('/', (_req, res) => res.json({ ok: true, service: 'calendar-service' }));
app.get('/health', (_req, res) => res.json({ status: 'ok' }));

// Diagnostics: echo back what was received
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

// ----- REST: Events -----

// GET /events – list
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

// POST /events – create
app.post('/events', async (req, res) => {
  try {
    let payload = req.body;

    // Fallback: if not parsed as JSON, try rawBody
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

// DELETE /events/:id – delete
app.delete('/events/:id', async (req, res) => {
  try {
    const data = await deleteEvent(req.params.id);
    res.json(data);
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

// ---- Bootstrap: mount GraphQL first, then listen ----
(async () => {
  await mountGraphQL(app, '/graphql'); // <- await ensures the route exists before first requests

  // Uniform 404 JSON (keep last)
  app.use((req, res) => res.status(404).json({ ok: false, error: 'Not Found' }));

  const PORT = process.env.PORT || 8080;
  app.listen(PORT, () => console.log(`calendar-service listening on :${PORT}`));
})().catch((e) => {
  console.error('[Startup] failed to start', e);
  process.exit(1);
});

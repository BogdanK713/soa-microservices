const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const { listEvents, createEvent, deleteEvent } = require('./google');

const app = express();
app.use(cors());
app.use(express.json({ limit: '1mb' }));
app.use(morgan('tiny'));

app.get('/health', (_req, res) => res.json({ status: 'ok' }));

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

app.post('/events', async (req, res) => {
  try {
    const data = await createEvent(req.body || {});
    res.status(201).json({ ok: true, event: data });
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

app.delete('/events/:id', async (req, res) => {
  try {
    const data = await deleteEvent(req.params.id);
    res.json(data);
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`calendar-service listening on :${PORT}`));

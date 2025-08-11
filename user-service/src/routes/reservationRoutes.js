const express = require('express');
const router = express.Router();
const db = require('../config/db');
const axios = require('axios');

/** ----------------- helpers ----------------- */
async function notifyCalendar(payload) {
  const base = process.env.CALENDAR_URL; // npr. http://calendar-service:8080
  if (!base) return;
  try {
    await axios.post(`${base}/events`, payload, { timeout: 2000 });
  } catch (e) {
    console.warn('Calendar notify failed:', e.message);
  }
}

/** Normalizacija polja iz baze -> API format */
function mapReservation(row) {
  return {
    id: row.id,
    userId: row.user_id,
    locationId: row.location_id,
    serviceId: row.service_id,
    createdAt: row.created_at,
  };
}

/** ----------------- ROUTES ----------------- */

/**
 * GET /api/reservations
 * Lista rezervacija
 */
router.get('/', async (_req, res) => {
  try {
    const [rows] = await db.query(
      'SELECT id, user_id, location_id, service_id, created_at FROM reservations ORDER BY id DESC'
    );
    res.json(rows.map(mapReservation));
  } catch (err) {
    console.error('GET /reservations error:', err);
    res.status(500).json({ error: 'Failed to fetch reservations' });
  }
});

/**
 * GET /api/reservations/:id
 * Detalj rezervacije
 */
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await db.query(
      'SELECT id, user_id, location_id, service_id, created_at FROM reservations WHERE id = ?',
      [req.params.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Reservation not found' });
    res.json(mapReservation(rows[0]));
  } catch (err) {
    console.error('GET /reservations/:id error:', err);
    res.status(500).json({ error: 'Failed to fetch reservation' });
  }
});

/**
 * POST /api/reservations
 * Body: { userId, locationId, serviceId, userEmail?, userName? }
 */
router.post('/', async (req, res) => {
  const { userId, locationId, serviceId, userEmail, userName } = req.body || {};
  if (!userId || !locationId || !serviceId) {
    return res.status(400).json({ error: 'userId, locationId and serviceId are required' });
  }

  try {
    const [result] = await db.query(
      'INSERT INTO reservations (user_id, location_id, service_id, created_at) VALUES (?, ?, ?, NOW())',
      [userId, locationId, serviceId]
    );

    const createdId = result.insertId;

    // fire-and-forget poziv ka calendar-service (ne blokira korisnika)
    const startISO = new Date().toISOString();
    const endISO = new Date(Date.now() + 30 * 60 * 1000).toISOString();
    notifyCalendar({
      summary: `Reservation #${createdId}`,
      description: `userId=${userId}, serviceId=${serviceId}, locationId=${locationId}`,
      start: startISO,
      end: endISO,
      attendees: userEmail ? [{ email: userEmail, name: userName || 'User' }] : [],
    }).catch(() => { /* već logujemo unutra */ });

    res.status(201).json({
      id: createdId,
      userId,
      locationId,
      serviceId,
      createdAt: startISO,
    });
  } catch (err) {
    console.error('POST /reservations error:', err);
    res.status(500).json({ error: 'Failed to create reservation' });
  }
});

/**
 * PUT /api/reservations/:id
 * Body: { userId?, locationId?, serviceId? }
 */
router.put('/:id', async (req, res) => {
  const { userId, locationId, serviceId } = req.body || {};
  if (!userId && !locationId && !serviceId) {
    return res.status(400).json({ error: 'Nothing to update' });
  }

  try {
    // build dinamički SET
    const fields = [];
    const params = [];
    if (userId) { fields.push('user_id = ?'); params.push(userId); }
    if (locationId) { fields.push('location_id = ?'); params.push(locationId); }
    if (serviceId) { fields.push('service_id = ?'); params.push(serviceId); }
    params.push(req.params.id);

    const [result] = await db.query(
      `UPDATE reservations SET ${fields.join(', ')} WHERE id = ?`,
      params
    );

    if (!result.affectedRows) {
      return res.status(404).json({ error: 'Reservation not found' });
    }

    const [rows] = await db.query(
      'SELECT id, user_id, location_id, service_id, created_at FROM reservations WHERE id = ?',
      [req.params.id]
    );
    res.json(mapReservation(rows[0]));
  } catch (err) {
    console.error('PUT /reservations/:id error:', err);
    res.status(500).json({ error: 'Failed to update reservation' });
  }
});

/**
 * DELETE /api/reservations/:id
 */
router.delete('/:id', async (req, res) => {
  try {
    const [result] = await db.query('DELETE FROM reservations WHERE id = ?', [req.params.id]);
    if (!result.affectedRows) {
      return res.status(404).json({ error: 'Reservation not found' });
    }
    // Ako kasnije budeš čuvao calendar eventId u bazi,
    // ovdje možeš pozvati DELETE /events/:eventId na calendar-service.
    res.json({ ok: true });
  } catch (err) {
    console.error('DELETE /reservations/:id error:', err);
    res.status(500).json({ error: 'Failed to delete reservation' });
  }
});

module.exports = router;

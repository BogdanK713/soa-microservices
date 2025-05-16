const express = require('express');
const router = express.Router();
const reservationModel = require('../models/reservationModel');

// GET all reservations
router.get('/', async (req, res) => {
  const reservations = await reservationModel.getAllReservations();
  res.json(reservations);
});

// GET reservation by ID
router.get('/:id', async (req, res) => {
  const reservation = await reservationModel.getReservationById(req.params.id);
  if (!reservation) return res.status(404).json({ message: 'Reservation not found' });
  res.json(reservation);
});

// POST new reservation
router.post('/', async (req, res) => {
  const newReservation = await reservationModel.createReservation(req.body);
  res.status(201).json(newReservation);
});

// PUT update reservation
router.put('/:id', async (req, res) => {
  const updatedReservation = await reservationModel.updateReservation(req.params.id, req.body);
  res.json(updatedReservation);
});

// DELETE reservation
router.delete('/:id', async (req, res) => {
  await reservationModel.deleteReservation(req.params.id);
  res.json({ message: 'Reservation deleted' });
});

module.exports = router;

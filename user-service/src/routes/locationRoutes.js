const express = require('express');
const router = express.Router();
const locationModel = require('../models/locationModel');

// GET all locations
router.get('/', async (req, res) => {
  const locations = await locationModel.getAllLocations();
  res.json(locations);
});

// GET location by ID
router.get('/:id', async (req, res) => {
  const location = await locationModel.getLocationById(req.params.id);
  if (!location) return res.status(404).json({ message: 'Location not found' });
  res.json(location);
});

// POST new location
router.post('/', async (req, res) => {
  const newLocation = await locationModel.createLocation(req.body);
  res.status(201).json(newLocation);
});

// PUT update location
router.put('/:id', async (req, res) => {
  const updatedLocation = await locationModel.updateLocation(req.params.id, req.body);
  res.json(updatedLocation);
});

// DELETE location
router.delete('/:id', async (req, res) => {
  await locationModel.deleteLocation(req.params.id);
  res.json({ message: 'Location deleted' });
});

module.exports = router;

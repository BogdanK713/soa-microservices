const express = require('express');
const router = express.Router();
const favoriteModel = require('../models/favoriteModel');

// GET all favorite companies for a user
router.get('/user/:userId', async (req, res) => {
  const favorites = await favoriteModel.getFavoritesByUser(req.params.userId);
  res.json(favorites);
});

// POST add a favorite company
router.post('/', async (req, res) => {
  const { user_id } = req.body;
  const newFavorite = await favoriteModel.addFavoriteCompany(user_id);
  res.status(201).json(newFavorite);
});

// DELETE favorite company
router.delete('/:id', async (req, res) => {
  await favoriteModel.deleteFavoriteCompany(req.params.id);
  res.json({ message: 'Favorite deleted' });
});

module.exports = router;

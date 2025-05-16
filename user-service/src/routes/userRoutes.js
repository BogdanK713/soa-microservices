const express = require('express');
const router = express.Router();
const userModel = require('../models/userModel');

// GET all users
router.get('/', async (req, res) => {
  const users = await userModel.getAllUsers();
  res.json(users);
});

// GET user by ID
router.get('/:id', async (req, res) => {
  const user = await userModel.getUserById(req.params.id);
  if (!user) return res.status(404).json({ message: 'User not found' });
  res.json(user);
});

// POST create new user
router.post('/', async (req, res) => {
  const newUser = await userModel.createUser(req.body);
  res.status(201).json(newUser);
});

// PUT update user
router.put('/:id', async (req, res) => {
  const updatedUser = await userModel.updateUser(req.params.id, req.body);
  res.json(updatedUser);
});

// DELETE user
router.delete('/:id', async (req, res) => {
  await userModel.deleteUser(req.params.id);
  res.json({ message: 'User deleted' });
});

module.exports = router;

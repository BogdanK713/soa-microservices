const express = require('express');
const router = express.Router();
const userModel = require('../models/userModel');

// GET all users
router.get('/', async (req, res) => {
  try {
    const users = await userModel.getAllUsers();
    res.json(users);
  } catch (err) {
    console.error('GET /users error:', err);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// GET user by ID
router.get('/:id', async (req, res) => {
  try {
    const user = await userModel.getUserById(req.params.id);
    if (!user) return res.status(404).json({ message: 'User not found' });
    res.json(user);
  } catch (err) {
    console.error('GET /users/:id error:', err);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// POST create new user
router.post('/', async (req, res) => {
  try {
    // pričakujemo { name, email, phone? }
    const newUser = await userModel.createUser(req.body);
    res.status(201).json(newUser);
  } catch (err) {
    console.error('POST /users error:', err);
    // Unique email itd.
    const status = err.code === 'ER_DUP_ENTRY' ? 409 : 500;
    res.status(status).json({ message: err.message || 'Internal server error' });
  }
});

// PUT update user
router.put('/:id', async (req, res) => {
  try {
    // pričakujemo { name, email, phone? }
    const updatedUser = await userModel.updateUser(req.params.id, req.body);
    if (!updatedUser) return res.status(404).json({ message: 'User not found' });
    res.json(updatedUser);
  } catch (err) {
    console.error('PUT /users/:id error:', err);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// DELETE user
router.delete('/:id', async (req, res) => {
  try {
    const ok = await userModel.deleteUser(req.params.id);
    if (!ok) return res.status(404).json({ message: 'User not found' });
    res.json({ message: 'User deleted' });
  } catch (err) {
    console.error('DELETE /users/:id error:', err);
    res.status(500).json({ message: 'Internal server error' });
  }
});

module.exports = router;

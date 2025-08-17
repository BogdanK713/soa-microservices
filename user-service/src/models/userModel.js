const db = require('../config/db');

const getAllUsers = async () => {
  // SELECT * će već vraćati i phone ako kolona postoji
  const [rows] = await db.query('SELECT * FROM user');
  return rows;
};

const getUserById = async (id) => {
  const [rows] = await db.query('SELECT * FROM user WHERE id = ?', [id]);
  return rows[0];
};

const createUser = async (user) => {
  const { first_name, last_name, email, oauth_id, location_id, phone } = user;
  const [result] = await db.query(
    'INSERT INTO user (first_name, last_name, email, oauth_id, location_id, phone) VALUES (?, ?, ?, ?, ?, ?)',
    [first_name, last_name, email, oauth_id, location_id, phone]
  );
  return { id: result.insertId, ...user };
};

const updateUser = async (id, user) => {
  const { first_name, last_name, email, oauth_id, location_id, phone } = user;
  await db.query(
    'UPDATE user SET first_name = ?, last_name = ?, email = ?, oauth_id = ?, location_id = ?, phone = ? WHERE id = ?',
    [first_name, last_name, email, oauth_id, location_id, phone, id]
  );
  return { id, ...user };
};

const deleteUser = async (id) => {
  await db.query('DELETE FROM user WHERE id = ?', [id]);
};

module.exports = {
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser
};

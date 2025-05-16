const db = require('../config/db');

const getFavoritesByUser = async (userId) => {
  const [rows] = await db.query('SELECT * FROM favorite_companies WHERE user_id = ?', [userId]);
  return rows;
};

const addFavoriteCompany = async (userId) => {
  const [result] = await db.query('INSERT INTO favorite_companies (user_id) VALUES (?)', [userId]);
  return { id: result.insertId, user_id: userId };
};

const deleteFavoriteCompany = async (id) => {
  await db.query('DELETE FROM favorite_companies WHERE id = ?', [id]);
};

module.exports = {
  getFavoritesByUser,
  addFavoriteCompany,
  deleteFavoriteCompany
};

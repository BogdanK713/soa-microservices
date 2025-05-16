const db = require('../config/db');

const getAllLocations = async () => {
  const [rows] = await db.query('SELECT * FROM location');
  return rows;
};

const getLocationById = async (id) => {
  const [rows] = await db.query('SELECT * FROM location WHERE id = ?', [id]);
  return rows[0];
};

const createLocation = async (location) => {
  const { postal_code, city, country } = location;
  const [result] = await db.query(
    'INSERT INTO location (postal_code, city, country) VALUES (?, ?, ?)',
    [postal_code, city, country]
  );
  return { id: result.insertId, ...location };
};

const updateLocation = async (id, location) => {
  const { postal_code, city, country } = location;
  await db.query(
    'UPDATE location SET postal_code = ?, city = ?, country = ? WHERE id = ?',
    [postal_code, city, country, id]
  );
  return { id, ...location };
};

const deleteLocation = async (id) => {
  await db.query('DELETE FROM location WHERE id = ?', [id]);
};

module.exports = {
  getAllLocations,
  getLocationById,
  createLocation,
  updateLocation,
  deleteLocation
};

const db = require('../config/db');

const getAllReservations = async () => {
  const [rows] = await db.query('SELECT * FROM reservations');
  return rows;
};

const getReservationById = async (id) => {
  const [rows] = await db.query('SELECT * FROM reservations WHERE id = ?', [id]);
  return rows[0];
};

const createReservation = async (reservation) => {
  const { reservation_code, user_id } = reservation;
  const [result] = await db.query(
    'INSERT INTO reservations (reservation_code, user_id) VALUES (?, ?)',
    [reservation_code, user_id]
  );
  return { id: result.insertId, ...reservation };
};

const updateReservation = async (id, reservation) => {
  const { reservation_code, user_id } = reservation;
  await db.query(
    'UPDATE reservations SET reservation_code = ?, user_id = ? WHERE id = ?',
    [reservation_code, user_id, id]
  );
  return { id, ...reservation };
};

const deleteReservation = async (id) => {
  await db.query('DELETE FROM reservations WHERE id = ?', [id]);
};

module.exports = {
  getAllReservations,
  getReservationById,
  createReservation,
  updateReservation,
  deleteReservation
};

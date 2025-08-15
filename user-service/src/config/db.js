// user-service/src/config/db.js
const mysql = require('mysql2/promise');
require('dotenv').config();

const runningInDocker = process.env.DB_HOST && process.env.DB_HOST !== 'localhost';
const host =
  process.env.DB_HOST ||
  (process.env.NODE_ENV === 'production' ? 'user-mysql' : '127.0.0.1');

const port = process.env.DB_PORT
  ? Number(process.env.DB_PORT)
  : (!runningInDocker ? 3307 : 3306);

const pool = mysql.createPool({
  host,
  port,
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'root',
  database: process.env.DB_NAME || 'user_service_db',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

module.exports = pool;

const { GraphQLScalarType, Kind } = require('graphql');
const db = require('../config/db');

const DateScalar = new GraphQLScalarType({
  name: 'Date',
  parseValue: (value) => new Date(value),
  serialize: (value) => new Date(value).toISOString(),
  parseLiteral: (ast) => (ast.kind === Kind.STRING ? new Date(ast.value) : null),
});

module.exports = {
  Date: DateScalar,

  Query: {
    async users() {
      const [rows] = await db.query('SELECT id, name, email FROM users');
      return rows;
    },
    async reservationsByUser(_, { userId }) {
      const [rows] = await db.query(
        'SELECT id, user_id AS userId, location_id AS locationId, service_id AS serviceId, created_at AS createdAt FROM reservations WHERE user_id = ?',
        [userId]
      );
      return rows;
    },
  },

  Reservation: {
    async user(parent) {
      const [rows] = await db.query('SELECT id, name, email FROM users WHERE id = ?', [parent.userId]);
      return rows[0] || null;
    },
    async location(parent) {
      const [rows] = await db.query('SELECT id, name, address FROM locations WHERE id = ?', [parent.locationId]);
      return rows[0] || null;
    },
  },
};

// user-service/src/graphql/resolvers.js
const db = require('../config/db');
const Users = require('../models/userModel');
const Locations = require('../models/locationModel');
const Reservations = require('../models/reservationModel');

module.exports = {
  Query: {
    // USERS
    users: () => Users.getAllUsers(),
    user: (_p, { id }) => Users.getUserById(id),

    // RESERVATIONS
    reservations: () => Reservations.getAllReservations(),
    reservation: (_p, { id }) => Reservations.getReservationById(id),
    reservationsByUser: (_p, { userId }) => Reservations.getReservationsByUser(userId),
  },

  User: {
    // napravi "First Last" iz first_name/last_name (ili vrati name ako je već spojeno)
    name: (u) => {
      const f = u.first_name || u.firstName || '';
      const l = u.last_name || u.lastName || '';
      return [f, l].filter(Boolean).join(' ').trim() || u.name || '';
    },
  },

  Reservation: {
    // alias za kompatibilnost – pretvori createdAt u ISO string
    date: (r) => (r.createdAt ? new Date(r.createdAt).toISOString() : null),

    user: (r) => Users.getUserById(r.userId),
    location: async (r) => {
      if (!r.locationId) return null;
      // prilagodi prema tvom locationModel-u (ako već imaš getLocationById)
      return Locations.getLocationById
        ? Locations.getLocationById(r.locationId)
        : null;
    },

    // amount: vrati broj ili null (ako kolona ne postoji)
    amount: (r) => (r.amount != null ? Number(r.amount) : null),
  },
};

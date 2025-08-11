const { gql } = require('apollo-server-express');

module.exports = gql`
  scalar Date

  type User {
    id: ID!
    name: String!
    email: String!
  }

  type Location {
    id: ID!
    name: String!
    address: String!
  }

  type Reservation {
    id: ID!
    userId: ID!
    locationId: ID!
    serviceId: ID!
    createdAt: Date!
    user: User
    location: Location
  }

  type Query {
    users: [User!]!
    reservationsByUser(userId: ID!): [Reservation!]!
  }
`;

const { gql } = require('apollo-server-express');

module.exports = gql`
  scalar Date

  type User {
    id: ID!
    first_name: String
    last_name: String
    email: String!
    name: String!          # computed "First Last"
    phone: String          # NOVO
  }

  type Location {
    id: ID!
    city: String
    country: String
    postal_code: String
  }

  type Service {
    id: ID!
    name: String
    price: Float
  }

  type Reservation {
    id: ID!
    userId: ID!
    serviceId: ID
    locationId: ID

    createdAt: Date!
    date: Date
    amount: Float

    user: User
    location: Location
    service: Service
  }

  type Query {
    # USERS
    users: [User!]!
    user(id: ID!): User

    # RESERVATIONS
    reservations: [Reservation!]!
    reservation(id: ID!): Reservation
    reservationsByUser(userId: ID!): [Reservation!]!

    # SERVICES (če jih uporabljaš)
    services: [Service!]!
    service(id: ID!): Service
  }
`;

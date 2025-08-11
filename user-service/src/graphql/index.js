const { ApolloServer } = require('apollo-server-express');
const typeDefs = require('./schema');
const resolvers = require('./resolvers');

async function startGraphQL(app, path = '/api/graphql') {
  const server = new ApolloServer({ typeDefs, resolvers });
  await server.start();
  server.applyMiddleware({ app, path });
  // GraphQL Playground: http://localhost:3000/api/graphql
}

module.exports = { startGraphQL };

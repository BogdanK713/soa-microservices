// user-service/src/graphql/index.js
const { ApolloServer } = require('apollo-server-express');
const typeDefs = require('./schema');
const resolvers = require('./resolvers');

async function startGraphQL(app, path = '/api/graphql') {
  const server = new ApolloServer({ typeDefs, resolvers });
  await server.start();
  server.applyMiddleware({ app, path });
  console.log(`GraphQL ready at ${path}`);
}

module.exports = { startGraphQL };

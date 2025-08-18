// calendar-service/graphql/mount.js
// Mount Apollo Server v4 on an existing Express app at /graphql

const { ApolloServer } = require("@apollo/server");
const { expressMiddleware } = require("@apollo/server/express4");
const { ApolloServerPluginLandingPageLocalDefault } = require("@apollo/server/plugin/landingPage/default");
const bodyParser = require("body-parser");
const cors = require("cors");
const { typeDefs, resolvers } = require("./schema");

/**
 * Mounts GraphQL middleware at the given path.
 * IMPORTANT: call and await this before app.listen()
 */
async function mountGraphQL(app, path = "/graphql") {
  const server = new ApolloServer({
    typeDefs,
    resolvers,
    plugins: [ApolloServerPluginLandingPageLocalDefault()],
  });

  await server.start();

  // CORS + JSON body parser only for /graphql
  app.use(path, cors(), bodyParser.json(), expressMiddleware(server));

  console.log(`[GraphQL] mounted at ${path}`);
}

module.exports = { mountGraphQL };

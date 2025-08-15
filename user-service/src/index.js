const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const YAML = require('yamljs');
const swaggerUi = require('swagger-ui-express');
const path = require('path');

// idi jedan folder gore iz src/ pa u docs/
const swaggerPath = path.resolve(__dirname, '..', 'docs', 'swagger.yaml');
const swaggerDocument = YAML.load(swaggerPath);

dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;

// REST routes
const userRoutes = require('./routes/userRoutes');
const locationRoutes = require('./routes/locationRoutes');
const favoriteRoutes = require('./routes/favoriteRoutes');
const reservationRoutes = require('./routes/reservationRoutes');

app.use(cors());
app.use(express.json());

app.use('/api/users', userRoutes);
app.use('/api/locations', locationRoutes);
app.use('/api/favorites', favoriteRoutes);
app.use('/api/reservations', reservationRoutes);
app.get('/api/health', (_req, res) => res.json({ status: 'ok' }));

app.use('/api/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// GraphQL
const { startGraphQL } = require('./graphql');
(async () => {
  await startGraphQL(app, '/api/graphql');
})();

app.listen(PORT, () => {
  console.log(`User Service running at http://localhost:${PORT}`);
});

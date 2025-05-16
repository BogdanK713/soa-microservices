const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const YAML = require('yamljs');
const swaggerUi = require('swagger-ui-express');
const path = require('path');

dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;

// Route imports
const userRoutes = require('./routes/userRoutes');
const locationRoutes = require('./routes/locationRoutes');
const favoriteRoutes = require('./routes/favoriteRoutes');
const reservationRoutes = require('./routes/reservationRoutes');
const swaggerDocument = YAML.load(path.join(__dirname, '..', 'docs', 'swagger.yaml'));

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/users', userRoutes);
app.use('/api/locations', locationRoutes);
app.use('/api/favorites', favoriteRoutes);
app.use('/api/reservations', reservationRoutes);
app.get('/api/health', (req, res) => res.json({ status: 'ok' }));

// Swagger docs
app.use('/api/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Start server
app.listen(PORT, () => {
  console.log(`User Service running at http://localhost:${PORT}`);
});

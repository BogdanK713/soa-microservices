# --- build stage (samo ako radiš transpile/ts – inače se preskače) ---
# FROM node:18-alpine AS build
# WORKDIR /app
# COPY package*.json ./
# RUN npm ci --only=production
# COPY . .
# # ako koristiš TypeScript: RUN npm run build

# --- runtime stage ---
FROM node:18-alpine
WORKDIR /app

# Manje slojeva i keširanje: prvo samo deps
COPY package*.json ./
RUN npm ci --only=production --no-audit --no-fund

# Kopiraj ostatak koda
COPY . .

# Bez cache-a i nepotrebnih paketa u alpine
RUN apk add --no-cache tini

ENV NODE_ENV=production \
    PORT=3000

EXPOSE 3000

# Ako imaš start scriptu u package.json -> "start": "node src/index.js"
ENTRYPOINT ["/sbin/tini","--"]
CMD ["npm","start"]

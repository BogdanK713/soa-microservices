FROM node:18-alpine

WORKDIR /app

# Ako nemaš package-lock.json, koristimo npm install
COPY package*.json ./
RUN npm install --omit=dev --no-audit --no-fund

COPY src ./src

ENV NODE_ENV=production
ENV PORT=8080
EXPOSE 8080

CMD ["npm","start"]

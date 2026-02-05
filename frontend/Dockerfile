# Multi-stage build for SvelteKit frontend
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with legacy peer deps
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Build arguments for environment variables
ARG API_ENDPOINT=http://localhost:9000
ARG PUBLIC_API_URL=http://localhost:9000

# Set environment variables for build
ENV API_ENDPOINT=${API_ENDPOINT}
ENV PUBLIC_API_URL=${PUBLIC_API_URL}

# Build the application (OpenAPI client should be pre-generated)
RUN npm run build

# Production stage
FROM node:22-alpine AS production

WORKDIR /app

# Copy built assets and dependencies
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Runtime environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start the application
CMD ["node", "build"]
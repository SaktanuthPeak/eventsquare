FROM node:22-alpine AS deploy-node

WORKDIR /app
COPY ["package.json", "package-lock.json*", "./"]
COPY . .
RUN npm install
RUN npm run build --clean

ENV NODE_ENV=production

EXPOSE 3000
ENV PORT 3000
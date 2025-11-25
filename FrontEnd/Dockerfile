
FROM node:20-alpine AS builder
WORKDIR /app

# Install build dependencies
COPY package.json package-lock.json* ./
RUN npm install


COPY . .
RUN mkdir -p public
RUN if [ -f words.txt ]; then cp words.txt public/words.txt; fi
RUN npm run build


FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production


COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public


COPY package.json ./
COPY next.config.mjs ./

RUN npm install --production --omit=dev

EXPOSE 3000
CMD ["npm","run","start"]

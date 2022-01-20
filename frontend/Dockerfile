FROM node:17-alpine as builder

RUN npm install -g npm@latest

WORKDIR /app/frontend
COPY ./frontend/package*.json ./
RUN npm i

COPY ./frontend/ ./

RUN npm run build

FROM nginx:stable-alpine

COPY --from=builder /app/frontend/build/ /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]

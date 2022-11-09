FROM node:13.12.0-alpine as builder
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

WORKDIR /app

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 3000
ENTRYPOINT ["nginx", "-g", "daemon off;"]
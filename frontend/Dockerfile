# Stage 1: build the Angular application
FROM node:20 AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY angular.json tsconfig*.json karma.conf.js .browserslistrc ./
COPY src ./src

RUN npm run build -- --configuration production

# Stage 2: serve with Nginx
FROM nginx:1.25-alpine

COPY --from=build /app/dist/smartimmo /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

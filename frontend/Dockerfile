# Build stage
FROM node:20-alpine as build
WORKDIR /app
# Copy manifest; lockfiles are optional. Docker can't ignore missing files, so copy the known ones.
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Serve stage
FROM nginx:1.25-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

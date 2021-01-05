FROM node:10.16.1-alpine as build-step
RUN mkdir /app
WORKDIR /app
EXPOSE 8080
RUN export PORT=8080
COPY package.json /app
RUN npm install
COPY /src /app/src
RUN npm run build
 CMD ["node", "/app/src/index.js"]
# FROM nginx:1.17.1-alpine
# COPY --from=build-step /app/build /usr/share/nginx/html


# FROM node:10.16.1-alpine as ui

# WORKDIR /app

# COPY ./package.json ./package-lock.json ./

# RUN npm install

# COPY . ./

# RUN npm run build

# EXPOSE 3000

# CMD ["node", "index.js"]
FROM node:15-alpine3.10 as builder
WORKDIR /app
COPY package.json /app/package.json
RUN npm install
COPY . /app
RUN npm run build

FROM nginx:1.19-alpine
RUN apk --no-cache add curl
COPY --from=builder /app/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
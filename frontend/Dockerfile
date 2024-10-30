FROM node:23

LABEL authors="reloia"

WORKDIR /app

COPY package.json package.json
RUN npm install

COPY . /app

RUN npm run build

RUN npm install -g serve

EXPOSE 8104

CMD ["serve", "-s", "build", "-l", "8104"]
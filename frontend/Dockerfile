FROM node:23

LABEL authors="reloia"

WORKDIR /app

COPY package.json package.json
RUN npm install

COPY . /app

EXPOSE 5173

CMD ["npm", "run", "dev"]
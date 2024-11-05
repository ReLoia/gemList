FROM node:23

LABEL authors="reloia"

WORKDIR /app

COPY package.json package.json
RUN npm install

COPY . /app

EXPOSE 4173

#CMD ["npm", "run", "dev"]

CMD /bin/sh -c "npm run build --base=/${BASE_URL}"

CMD ["npm", "run", "preview"]


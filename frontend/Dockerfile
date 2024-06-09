FROM node:14

WORKDIR /app

COPY package.json .

RUN npm install
RUN npm install --save-dev @types/uuid

COPY . /app

CMD ["npm", "start"]

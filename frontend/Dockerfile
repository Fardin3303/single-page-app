FROM node:14

WORKDIR /frontend

COPY package.json .

RUN npm install
RUN npm i leaflet
RUN npm install axios --save

RUN npm install --save-dev @types/uuid

COPY . /frontend

CMD ["npm", "start"]

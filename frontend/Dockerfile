FROM node:14

WORKDIR /frontend

COPY package.json .

RUN npm install
RUN npm i leaflet
RUN npm install axios --save

COPY . /frontend

CMD ["npm", "start"]

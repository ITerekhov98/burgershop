FROM node:latest
ENV NODE_ENV=development

WORKDIR /code/
COPY package.json /code/
COPY package-lock.json /code/

RUN npm install -g npm && npm install --dev && npm install -g parcel-bundler

COPY . /code/




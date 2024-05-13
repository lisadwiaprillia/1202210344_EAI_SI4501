# base image
FROM node:14

# set working dir
WORKDIR /app

# copy package .json
COPY package*.json /app

#install dependencies
RUN npm install

# copy app.js
COPY app.js /app

# expose port
EXPOSE 5000

# run app
CMD ["node", "app.js"]
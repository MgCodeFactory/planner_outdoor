# Node.js LTS lightweight image
FROM node:lts-slim
# Set the working directory
WORKDIR /po_vue
# copy dependencies
COPY po_vue/package*.json ./
# install dependencies
RUN npm install
# Copy the project code
COPY po_vue/. .
# Expose the port for vue.js
EXPOSE 8080
# Command to run frontend move to docker-compose
#CMD ["npm", "run", "serve"]
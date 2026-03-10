FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV PORT=8787
EXPOSE 8787
CMD ["npm", "start"]

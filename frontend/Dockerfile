FROM node:16

RUN apt-get update && \
    apt-get install -y libgl1 libxi6 && \
    rm -rf /var/lib/apt/lists/*  # Чистим кэш APT для уменьшения размера образа

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

# Запускаем сервер разработки
CMD ["npm", "run", "dev"]

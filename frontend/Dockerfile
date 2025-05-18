# Используем официальный nginx образ с лёгким Alpine Linux
FROM nginx:alpine

# Копируем собранные файлы React в папку nginx
COPY . /usr/share/nginx/html

# Запускаем nginx в фоновом режиме
CMD ["nginx", "-g", "daemon off;"]
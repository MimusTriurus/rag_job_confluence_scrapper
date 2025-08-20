# Используем официальный образ Python-slim
FROM python:3.11-slim AS base

# Рабочая директория внутри контейнера
WORKDIR /app

# Отключаем буферизацию вывода Python для мгновенного логирования
ENV PYTHONUNBUFFERED=1

# Копируем файл зависимостей и устанавливаем их без кеша
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .
#CMD ["sh", "-c", "echo '🚀 Контейнер запущен!' && exec your_app_command"]
# Точка входа — запуск вашего main.py
#CMD ["mkdir", "confluence_md"]
CMD ["python", "main.py"]
#ENTRYPOINT echo "🚀 Контейнер запущен!" && ls
#CMD ["pwd"]
#CMD ["ls"]
#CMD ["cd app"]

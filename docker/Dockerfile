# Версия базового образа, версия и название, рабочий каталог
FROM python:3.14.4-slim
LABEL version="1.0" description="Agent"
WORKDIR /agent

# Установите зависимости приложения
COPY docker/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
	sudo \
	ufw \
	iproute2 \
	docker.io \
	&& rm -rf /var/lib/apt/lists/*


# Копируем исходный код и указываем порт на котором будет работать контейнер
COPY agent/checks /agent/checks
COPY cli /agent/cli/
# EXPOSE 8080

# # Настройте пользователя приложения, чтобы контейнер не запускался от имени пользователя root
# RUN useradd agent
# USER agent

# Указываем команду по умолчанию, которое выполняет контейнер
CMD [ "python3", "cli/main.py", "full"]
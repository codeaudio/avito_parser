FROM python:3.8.5
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ../../requirements.txt ./
RUN pip install -r requirements.txt
COPY ../.. ./
ENV PYTHONPATH /code
CMD [ "python", "/code/bot/bot.py" ]

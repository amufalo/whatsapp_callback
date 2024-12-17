FROM python:3.13-alpine

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add ffmpeg shared-mime-info

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app
RUN mkdir /app/media

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

RUN pip config --user set global.progress_bar off

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "-k", "uvicorn.workers.UvicornWorker", "app:app","--timeout","600","--workers=3"]

FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
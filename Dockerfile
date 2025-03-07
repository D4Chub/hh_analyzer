FROM python:3.11-slim-bullseye

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONPATH=/src

COPY ./requirements.txt /src
COPY . /src

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

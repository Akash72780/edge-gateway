FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /edgeGateway-ui
ADD . /edgeGateway-ui
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /edgeGateway-ui
CMD python manage.py runserver 0.0.0.0:80
From python:3.7.4

ENV HOME /root
WORKDIR /root

COPY . .

EXPOSE 8000


RUN pip install flask
RUN pip install Flask-SQLAlchemy
RUN pip install Flask-Login
RUN pip install Flask-SocketIO
Run pip install Flask-Migrate

CMD export FLASK_APP=server && flask run --port=8000 --host=0.0.0.0

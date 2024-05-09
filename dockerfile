FROM python:3-alpine3.18

WORKDIR /home/app
COPY requirements.txt /home/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/app
RUN pip install uvicorn


COPY prometheus.yml /etc/prometheus/


CMD [ "uvicorn","main:app","--host","0.0.0.0","--port", "8001" ]

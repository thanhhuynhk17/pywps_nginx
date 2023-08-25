FROM python:3.8

#For Gunicorn
ARG GU_WORKERS=5
ENV GU_WORKERS=${GU_WORKERS}

RUN apt-get update
RUN apt-get install -y libgdal-dev
RUN pip install GDAL==3.2.2.1

WORKDIR /pywps

COPY requirements.txt /pywps/
RUN pip install -r requirements.txt

COPY . .


# RUN ln -s /pywps/wsgi/pywps.wsgi /pywps/wsgi/pywps_app.py

CMD gunicorn -b 0.0.0.0:5000  --log-syslog --reload --pythonpath /pywps wsgi.pywps_app:application
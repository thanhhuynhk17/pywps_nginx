FROM python:3.8

#For Gunicorn
ARG GU_WORKERS=5
ENV GU_WORKERS=${GU_WORKERS}

WORKDIR /pywps

COPY . .

RUN pip install -r requirements.txt

# RUN ln -s /pywps/wsgi/pywps.wsgi /pywps/wsgi/pywps_app.py

CMD gunicorn -b 0.0.0.0:5000  --log-syslog --reload --pythonpath /pywps wsgi.pywps_app:application
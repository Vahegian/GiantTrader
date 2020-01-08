FROM python:3.7.5-buster

# Environment variables
ENV PYTHON_VERSION=3
ENV ENTRY=start.py
ENV ENTRY_PATH=/usr/src/app
# \Environment variables

# Working directory
RUN mkdir ${ENTRY_PATH}
WORKDIR ${ENTRY_PATH}
# \Working directory

EXPOSE 5000/tcp

# Software b1
#RUN apt-get update && \
#    apt-get install -y tzdata && \
#    apt-get install -y python${PYTHON_VERSION} && \
#    apt-get install -y python${PYTHON_VERSION}-pip && \
#    apt-get install -y iputils-ping && \
#    apt-get install -y libpq-dev && \
#    rm -rf /var/lib/apt/lists/*
# \Software b1

# Python libs b1
RUN pip${PYTHON_VERSION} install numpy && \
    pip${PYTHON_VERSION} install pandas && \
    pip${PYTHON_VERSION} install SQLAlchemy && \
    pip${PYTHON_VERSION} install psycopg2 && \
    pip${PYTHON_VERSION} install flask-restful && \
    pip${PYTHON_VERSION} install flask_cors && \
    pip${PYTHON_VERSION} install pika && \
    pip${PYTHON_VERSION} install tensorflow==1.13.1 && \
    pip${PYTHON_VERSION} install keras
# \Python libs b1

# Running script
#RUN cd ${ENTRY_PATH}
CMD python${PYTHON_VERSION} ./${ENTRY}
# \Running script


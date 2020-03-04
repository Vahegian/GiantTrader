FROM ubuntu:18.04

# Environment variables
ENV PYTHON_VERSION=3
ENV ENTRY=start.py
ENV ENTRY_PATH=/usr/src/app
# \Environment variables

EXPOSE 5000/tcp

# Working directory
RUN mkdir ${ENTRY_PATH}
WORKDIR ${ENTRY_PATH}
# \Working directory

# Software b1
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y tzdata && \
    apt-get install -y python${PYTHON_VERSION} && \
    apt-get install -y python${PYTHON_VERSION}-pip && \
    apt-get install -y iputils-ping && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*
# \Software b1

COPY ./requirements.txt ./

# Python libs b1
RUN pip${PYTHON_VERSION} install -r ./requirements.txt 
# \Python libs b1

# Running script
#RUN cd ${ENTRY_PATH}
CMD python${PYTHON_VERSION} ./${ENTRY}
# \Running script


FROM ubuntu:18.04

# Environment variables
ENV PYTHON_VERSION=3
ENV ENTRY=start.py
ENV ENTRY_PATH=/usr/src/app
# \Environment variables

# Working directory
RUN mkdir ${ENTRY_PATH}
WORKDIR ${ENTRY_PATH}
# \Working directory

# Software b1
RUN apt-get update
RUN apt-get install -y tzdata 
RUN apt-get install -y python${PYTHON_VERSION}
RUN apt-get install -y python${PYTHON_VERSION}-pip
RUN apt-get install -y python${PYTHON_VERSION}-opencv
# \Software b1

# Python libs b1
RUN pip${PYTHON_VERSION} install python-binance
RUN pip${PYTHON_VERSION} install numpy
RUN pip${PYTHON_VERSION} install pandas
RUN pip${PYTHON_VERSION} install SQLAlchemy
# \Python libs b1

# Software b2
RUN apt-get install -y iputils-ping
#RUN apt-get install -y python-psycopg2
RUN apt-get install -y libpq-dev
# Software b2

# Python libs b2
RUN pip${PYTHON_VERSION} install psycopg2
# \Python libs b2

# Running script
RUN cd ${ENTRY_PATH}
#CMD ["ls", "-l"]
CMD python${PYTHON_VERSION} ./${ENTRY}
# \Running script


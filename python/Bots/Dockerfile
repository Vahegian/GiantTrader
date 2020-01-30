FROM python:3.7.5-buster

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

COPY ./requirements.txt ./

# Python libs b1
RUN pip${PYTHON_VERSION} install -r ./requirements.txt 
# \Python libs b1

COPY ./ ./

# Running script
#RUN cd ${ENTRY_PATH}
CMD python${PYTHON_VERSION} ./${ENTRY}
# \Running script


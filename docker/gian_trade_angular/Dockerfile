FROM node

# Environment variables
ENV ENTRY_PATH=/usr/src/app
# \Environment variables

# Working directory
RUN mkdir ${ENTRY_PATH}
WORKDIR ${ENTRY_PATH}
# \Working directory

EXPOSE 4200/tcp

# Software b1
RUN npm install -g @angular/cli && \ 
    rm -rf /var/lib/apt/lists/*
# \Software b1

# Running script
#RUN cd ${ENTRY_PATH}
CMD ng serve --host 0.0.0.0
# \Running script


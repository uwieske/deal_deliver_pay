FROM python:3.9.13-slim-bullseye

RUN apt update && \
    apt install -y wget && \
    mkdir /tmp/installation-miniconda && \
    cd /tmp/installation-miniconda && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /usr/local/miniconda && \
    echo "export PATH=/usr/local/miniconda/bin:$PATH" >> ~/.bashrc    

RUN export PATH=/usr/local/miniconda/bin/:$PATH && conda install -q -y pandas flask    
RUN mkdir /data
COPY data-output /data/data-output
COPY ups-api /data/ups-api
WORKDIR /data/ups-api 
ENV PATH=/usr/local/miniconda/bin:$PATH
ENV FLASK_APP=ups_api
EXPOSE 5000
CMD  ["flask", "run", "--host=0.0.0.0"]
#FROM python:3
FROM python:TODO_PROJECT_PYTHON_VERSION-slim

RUN apt update -q -y && apt autoremove && apt clean

WORKDIR /app

# INSTALL PYTHON DEPENDENCIES #################################################

COPY . ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# INSTALL THE PROJECT #########################################################

RUN pip install .

#CMD pytest

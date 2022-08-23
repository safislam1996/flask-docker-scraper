FROM python:3.8
ADD . /scraper
WORKDIR /scraper
RUN pip install -r requirements.txt



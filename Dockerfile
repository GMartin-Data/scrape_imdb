FROM python:3.10-bookworm

WORKDIR /scraper

RUN apt-get update

COPY requirements.txt .

RUN python -m venv venv

ENV PATH="opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
pip install -r requirements.txt

ENV PYTHONBUFFERED 1

COPY . .

RUN chmod + x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
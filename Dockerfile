FROM python:3.10-bookworm

WORKDIR /scraper

# You need netcat to check database availability when deploying
RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt .

RUN python -m venv venv

# Forces the use of venv's python binary
ENV PATH="opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
pip install -r requirements.txt

# Allows logs to be displayed within the container
ENV PYTHONBUFFERED 1

COPY . .

RUN chmod + x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
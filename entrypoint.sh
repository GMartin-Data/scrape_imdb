#!/bin/sh

# Wait for Database host availability
# This is only required when deploying on Azure
# Otherwise docker compose will manage it with depends_on clause
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "En attente de la disponibilité de Postgres..."
  sleep 1
done

cd imdbscraper && python -m scrapy crawl filmspider
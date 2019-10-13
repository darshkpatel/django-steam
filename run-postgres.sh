#!/bin/bash
sudo docker run -v $(pwd)/postgres-data:/var/lib/postgresql/data -p 5432:5432 --rm postgres

psql -h localhost -U django django_steam

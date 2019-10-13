CREATE DATABASE django_steam;
CREATE USER django with password 'passpass';
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_steam TO django;
ALTER DATABASE django_steam SET log_statement = 'all';


INSERT INTO "marketplace_game" ("name", "price", "timesBought", "releaseDate", "description", "ageRating") VALUES ('Counter Strike', '600.0',

INSERT INTO "marketplace_dlc" ("name", "ageRating", "description") VALUES ('Need for Speed: Sea World Map', 12, 'All new sea world exclusive map')
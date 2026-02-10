-- init-db.sql
-- Создание БД с правильным collation

-- Сначала создаем БД с явными параметрами
CREATE DATABASE rest
WITH
ENCODING = 'UTF8'
LC_COLLATE = 'C'           -- ⬅️ Явно указываем collation
LC_CTYPE = 'C'             -- ⬅️ Явно указываем ctype
TEMPLATE = template0       -- ⬅️ Используем чистый template0
CONNECTION LIMIT = -1
ALLOW_CONNECTIONS = true;

-- Создаем пользователя
CREATE USER homework WITH PASSWORD 'skypro';

-- Даем права
GRANT ALL PRIVILEGES ON DATABASE rest TO homework;
ALTER DATABASE rest OWNER TO homework;

-- Подключаемся и создаем расширения
\c rest
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Устанавливаем правильный collation для БД
ALTER DATABASE rest SET lc_collate = 'C';
ALTER DATABASE rest SET lc_ctype = 'C';
-- Подключаемся к новой БД
\c rest

-- Создаем расширения
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Настраиваем БД
ALTER DATABASE rest SET timezone TO 'Europe/Moscow';
ALTER DATABASE rest SET default_text_search_config TO 'simple';

-- Проверка
SELECT current_database(), current_user, version();
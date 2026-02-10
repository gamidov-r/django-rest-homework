#!/bin/bash
set -e

echo "=== ВЫПОЛНЕНИЕ FORCE INIT СКРИПТА ==="

# Этот скрипт выполнится даже если база уже существует

# Подключаемся к PostgreSQL и создаем/пересоздаем БД
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
    -- Останавливаем все подключения к БД 'rest'
    UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'rest';

    -- Завершаем все активные подключения
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = 'rest'
      AND pid <> pg_backend_pid();

    -- Ждем завершения
    SELECT pg_sleep(2);

    -- Удаляем старую БД
    DROP DATABASE IF EXISTS rest;

    -- Создаем новую БД с правильными параметрами
    CREATE DATABASE rest
    WITH
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TEMPLATE = template0
    CONNECTION LIMIT = -1;

    -- Создаем пользователя если его нет
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'homework') THEN
            CREATE USER homework WITH PASSWORD 'skypro';
        ELSE
            -- Обновляем пароль
            ALTER USER homework WITH PASSWORD 'skypro';
        END IF;
    END
    \$\$;

    -- Даем все права
    GRANT ALL PRIVILEGES ON DATABASE rest TO homework;
    ALTER DATABASE rest OWNER TO homework;

    -- Создаем базу 'ruslan' если система требует
    CREATE DATABASE IF NOT EXISTS ruslan WITH OWNER homework;
EOSQL

echo "✅ База данных 'rest' принудительно пересоздана"
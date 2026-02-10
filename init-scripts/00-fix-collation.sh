#!/bin/bash
set -e

echo "=== Исправление collation при инициализации ==="

# Выполняем после создания БД
psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    -- Сначала создаем/проверяем БД
    \c rest

    -- Исправляем collation если нужно
    DO \$\$
    BEGIN
        -- Проверяем есть ли запись о версии collation
        IF EXISTS (
            SELECT 1 FROM pg_database
            WHERE datname = 'rest'
            AND datcollversion IS NOT NULL
        ) THEN
            -- Сбрасываем версию collation
            UPDATE pg_database
            SET datcollversion = NULL
            WHERE datname = 'rest';

            RAISE NOTICE 'Collation version reset for database: rest';
        END IF;
    END
    \$\$;

    -- Также для template1
    \c template1
    UPDATE pg_database
    SET datcollversion = NULL
    WHERE datname = 'template1';

    -- Возвращаемся в rest
    \c rest

    -- Проверяем
    SELECT datname, datcollversion IS NULL as "collation_ok"
    FROM pg_database
    WHERE datname IN ('rest', 'template1');
EOSQL

echo "✅ Collation исправлен при инициализации"
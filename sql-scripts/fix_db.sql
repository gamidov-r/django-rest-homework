DO $$
BEGIN
    -- Исправляем collation для базы 'rest'
    UPDATE pg_database
    SET datcollversion = NULL
    WHERE datname = 'rest'
      AND datcollversion IS NOT NULL;

    -- Исправляем для template1
    UPDATE pg_database
    SET datcollversion = NULL
    WHERE datname = 'template1'
      AND datcollversion IS NOT NULL;

    -- Обновляем версию
    PERFORM pg_collation_actual_version(oid)
    FROM pg_collation
    WHERE collname = 'C';

    RAISE NOTICE 'Collation fixed for databases: rest, template1';
END
$$;
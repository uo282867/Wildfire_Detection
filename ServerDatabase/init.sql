ALTER SYSTEM SET timezone TO 'Europe/Madrid';
SELECT pg_reload_conf();


CREATE TABLE IF NOT EXISTS camera_data (
    time        TIMESTAMPTZ     PRIMARY KEY,
    id          VARCHAR(40)     UNIQUE NOT NULL,
    alert       TEXT,
    seen        BOOLEAN
);

SELECT create_hypertable('camera_data', 'time', if_not_exists => TRUE);

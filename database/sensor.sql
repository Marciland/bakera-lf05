CREATE TABLE IF NOT EXISTS public."Sensor" (
    uuid uuid NOT NULL,
    sensor_id numeric NOT NULL,
    sensor_type text COLLATE pg_catalog."default" NOT NULL,
    latitude numeric NOT NULL,
    longitude numeric NOT NULL,
    location numeric NOT NULL,
    CONSTRAINT "Sensor_pkey" PRIMARY KEY (uuid)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public."Sensor" OWNER to admin;
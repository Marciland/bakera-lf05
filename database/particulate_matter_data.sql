CREATE TABLE IF NOT EXISTS public."ParticulateMatterData" (
    id serial NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "P1" numeric,
    "durP1" numeric,
    "ratioP1" numeric,
    "P2" numeric,
    "durP2" numeric,
    "ratioP2" numeric,
    sensor_id numeric NOT NULL,
    sensor_type text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "ParticulateMatterData_pkey" PRIMARY KEY (id),
    CONSTRAINT "ParticulateMatterData_sensor_id_sensor_type_fkey" FOREIGN KEY (sensor_id, sensor_type) REFERENCES public."Sensor" (sensor_id, sensor_type) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public."ParticulateMatterData" OWNER to admin;
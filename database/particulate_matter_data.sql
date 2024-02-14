CREATE TABLE IF NOT EXISTS public."ParticulateMatterData" (
    id serial NOT NULL,
    sensor_uuid uuid NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "P1" numeric,
    "durP1" numeric,
    "ratioP1" numeric,
    "P2" numeric,
    "durP2" numeric,
    "ratioP2" numeric,
    CONSTRAINT "ParticulateMatterData_pkey" PRIMARY KEY (id),
    CONSTRAINT sensor_uuid FOREIGN KEY (sensor_uuid) REFERENCES public."Sensor" (uuid) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public."ParticulateMatterData" OWNER to admin;
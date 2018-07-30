BEGIN TRANSACTION;
CREATE TABLE arboles (
        clave INTEGER PRIMARY KEY NOT NULL,
        latitud TEXT NOT NULL,
        longitud TEXT NOT NULL,
        arbolIzq TEXT NOT NULL,
        arbolDer TEXT NOT NULL,
        areaCopa TEXT NOT NULL,
        primero TEXT NOT NULL,
        id_parcelas INTEGER NOT NULL,
        id_arboles_faltanes INTEGER NOT NULL,
        id_surcos_detectados INTEGER NOT NULL,
        FOREIGN KEY(id_parcelas) REFERENCES parcelas(clave),
        FOREIGN KEY(id_arboles_faltanes) REFERENCES arboles_faltanes(clave),
        FOREIGN KEY(id_surcos_detectados) REFERENCES surcos_detectados(clave));
CREATE TABLE arboles_faltantes (
        clave INTEGER PRIMARY KEY NOT NULL,
        id_imagenes INTEGER NOT NULL,
        id_arboles INTEGER NOT NULL,
        FOREIGN KEY(id_imagenes) REFERENCES imagenes(clave),
        FOREIGN KEY(id_arboles) REFERENCES arboles(clave));
CREATE TABLE bloques (
        clave INTEGER PRIMARY KEY NOT NULL,
        color TEXT NOT NULL,
        tipoSuelo TEXT NOT NULL,
        id_repeticiones INTEGER NOT NULL,
        FOREIGN KEY(id_repeticiones) REFERENCES repeticiones(clave));
INSERT INTO "bloques" VALUES(1,'831','888',1);
INSERT INTO "bloques" VALUES(2,'335','218',1);
INSERT INTO "bloques" VALUES(3,'535','682',1);
INSERT INTO "bloques" VALUES(4,'311','379',2);
INSERT INTO "bloques" VALUES(5,'205','685',2);
INSERT INTO "bloques" VALUES(6,'366','717',2);
INSERT INTO "bloques" VALUES(7,'239','314',3);
INSERT INTO "bloques" VALUES(8,'735','298',3);
INSERT INTO "bloques" VALUES(9,'938','160',3);
CREATE TABLE clones (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL);
CREATE TABLE ensayos (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL,
        establecimiento TEXT NOT NULL,
        nroCuadro TEXT NOT NULL,
        suelo TEXT NOT NULL,
        espaciamientoX TEXT NOT NULL,
        espaciamientoY TEXT NOT NULL,
        plantasHa TEXT NOT NULL,
        fechaPlantacion TEXT NOT NULL,
        nroTratamientos TEXT NOT NULL,
        totalPlantas TEXT NOT NULL,
        totalHas TEXT NOT NULL,
        plantasParcela TEXT NOT NULL,
        tipoClonal TEXT NOT NULL,
        nroRepeticiones TEXT NOT NULL);
INSERT INTO "ensayos" VALUES(1,'665','528','837','701','517','751','780','170','699','837','587','799','273','176');
CREATE TABLE imagenes (
        clave INTEGER PRIMARY KEY NOT NULL,
        etapa TEXT NOT NULL,
        fecha TEXT NOT NULL,
        url TEXT NOT NULL,
        largo TEXT NOT NULL,
        ancho TEXT NOT NULL,
        latitud TEXT NOT NULL,
        longitud TEXT NOT NULL,
        altitud TEXT NOT NULL,
        latitudCono1 TEXT NOT NULL,
        longitudCono1 TEXT NOT NULL,
        latitudCono2 TEXT NOT NULL,
        longitudCono2 TEXT NOT NULL);
CREATE TABLE parcelas (
        clave INTEGER PRIMARY KEY NOT NULL,
        fila TEXT NOT NULL,
        columna TEXT NOT NULL,
        id_bloques INTEGER NOT NULL,
        id_clones INTEGER NOT NULL,
        FOREIGN KEY(id_bloques) REFERENCES bloques(clave),
        FOREIGN KEY(id_clones) REFERENCES clones(clave));
CREATE TABLE repeticiones (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL,
        nroFilas TEXT NOT NULL,
        nroColumnas TEXT NOT NULL,
        id_ensayos INTEGER NOT NULL, 
        FOREIGN KEY(id_ensayos) REFERENCES ensayos(clave));
INSERT INTO "repeticiones" VALUES(1,'808','558','423',1);
INSERT INTO "repeticiones" VALUES(2,'749','783','322',1);
INSERT INTO "repeticiones" VALUES(3,'815','252','860',1);
CREATE TABLE surcos_detectados (
        clave INTEGER PRIMARY KEY NOT NULL,
        distanciaMedia TEXT NOT NULL,
        anguloMedio TEXT NOT NULL);
COMMIT;

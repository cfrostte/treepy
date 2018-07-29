BEGIN TRANSACTION;
CREATE TABLE ensayos (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL);
INSERT INTO "ensayos" VALUES(1,'717');
INSERT INTO "ensayos" VALUES(2,'356');
INSERT INTO "ensayos" VALUES(3,'179');
INSERT INTO "ensayos" VALUES(4,'493');
INSERT INTO "ensayos" VALUES(5,'720');
INSERT INTO "ensayos" VALUES(6,'141');
INSERT INTO "ensayos" VALUES(7,'510');
INSERT INTO "ensayos" VALUES(8,'188');
INSERT INTO "ensayos" VALUES(9,'574');
CREATE TABLE repeticiones (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL,
        id_ensayos INTEGER, 
        FOREIGN KEY(id_ensayos) REFERENCES ensayos(clave));
INSERT INTO "repeticiones" VALUES(1,'632',1);
INSERT INTO "repeticiones" VALUES(2,'313',1);
INSERT INTO "repeticiones" VALUES(3,'302',1);
INSERT INTO "repeticiones" VALUES(4,'801',2);
INSERT INTO "repeticiones" VALUES(5,'861',2);
INSERT INTO "repeticiones" VALUES(6,'248',2);
INSERT INTO "repeticiones" VALUES(7,'402',3);
INSERT INTO "repeticiones" VALUES(8,'384',3);
INSERT INTO "repeticiones" VALUES(9,'690',3);
INSERT INTO "repeticiones" VALUES(10,'558',4);
INSERT INTO "repeticiones" VALUES(11,'199',4);
INSERT INTO "repeticiones" VALUES(12,'597',4);
INSERT INTO "repeticiones" VALUES(13,'331',5);
INSERT INTO "repeticiones" VALUES(14,'768',5);
INSERT INTO "repeticiones" VALUES(15,'255',5);
INSERT INTO "repeticiones" VALUES(16,'935',6);
INSERT INTO "repeticiones" VALUES(17,'884',6);
INSERT INTO "repeticiones" VALUES(18,'243',6);
INSERT INTO "repeticiones" VALUES(19,'264',7);
INSERT INTO "repeticiones" VALUES(20,'265',7);
INSERT INTO "repeticiones" VALUES(21,'434',7);
INSERT INTO "repeticiones" VALUES(22,'828',8);
INSERT INTO "repeticiones" VALUES(23,'659',8);
INSERT INTO "repeticiones" VALUES(24,'209',8);
INSERT INTO "repeticiones" VALUES(25,'198',9);
INSERT INTO "repeticiones" VALUES(26,'530',9);
INSERT INTO "repeticiones" VALUES(27,'544',9);
COMMIT;

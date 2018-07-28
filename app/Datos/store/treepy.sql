BEGIN TRANSACTION;
CREATE TABLE ensayos (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL);
INSERT INTO "ensayos" VALUES(1,'456');
INSERT INTO "ensayos" VALUES(2,'852');
INSERT INTO "ensayos" VALUES(3,'471');
INSERT INTO "ensayos" VALUES(4,'937');
INSERT INTO "ensayos" VALUES(5,'603');
INSERT INTO "ensayos" VALUES(6,'551');
INSERT INTO "ensayos" VALUES(7,'709');
INSERT INTO "ensayos" VALUES(8,'552');
INSERT INTO "ensayos" VALUES(9,'649');
CREATE TABLE repeticiones (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL,
        id_ensayos INTEGER, 
        FOREIGN KEY(id_ensayos) REFERENCES ensayos(clave));
INSERT INTO "repeticiones" VALUES(1,'748',1);
INSERT INTO "repeticiones" VALUES(2,'866',1);
INSERT INTO "repeticiones" VALUES(3,'488',1);
INSERT INTO "repeticiones" VALUES(4,'676',2);
INSERT INTO "repeticiones" VALUES(5,'269',2);
INSERT INTO "repeticiones" VALUES(6,'578',2);
INSERT INTO "repeticiones" VALUES(7,'852',3);
INSERT INTO "repeticiones" VALUES(8,'153',3);
INSERT INTO "repeticiones" VALUES(9,'572',3);
INSERT INTO "repeticiones" VALUES(10,'233',4);
INSERT INTO "repeticiones" VALUES(11,'610',4);
INSERT INTO "repeticiones" VALUES(12,'396',4);
INSERT INTO "repeticiones" VALUES(13,'488',5);
INSERT INTO "repeticiones" VALUES(14,'808',5);
INSERT INTO "repeticiones" VALUES(15,'652',5);
INSERT INTO "repeticiones" VALUES(16,'182',6);
INSERT INTO "repeticiones" VALUES(17,'744',6);
INSERT INTO "repeticiones" VALUES(18,'628',6);
INSERT INTO "repeticiones" VALUES(19,'898',7);
INSERT INTO "repeticiones" VALUES(20,'292',7);
INSERT INTO "repeticiones" VALUES(21,'574',7);
INSERT INTO "repeticiones" VALUES(22,'473',8);
INSERT INTO "repeticiones" VALUES(23,'571',8);
INSERT INTO "repeticiones" VALUES(24,'987',8);
INSERT INTO "repeticiones" VALUES(25,'869',9);
INSERT INTO "repeticiones" VALUES(26,'328',9);
INSERT INTO "repeticiones" VALUES(27,'683',9);
COMMIT;

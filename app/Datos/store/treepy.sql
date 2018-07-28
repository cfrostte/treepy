BEGIN TRANSACTION;
CREATE TABLE ensayos (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL);
INSERT INTO "ensayos" VALUES(1,'845');
INSERT INTO "ensayos" VALUES(2,'874');
INSERT INTO "ensayos" VALUES(3,'862');
INSERT INTO "ensayos" VALUES(4,'879');
INSERT INTO "ensayos" VALUES(5,'890');
INSERT INTO "ensayos" VALUES(6,'274');
INSERT INTO "ensayos" VALUES(7,'339');
INSERT INTO "ensayos" VALUES(8,'466');
INSERT INTO "ensayos" VALUES(9,'563');
INSERT INTO "ensayos" VALUES(10,'522');
INSERT INTO "ensayos" VALUES(11,'859');
INSERT INTO "ensayos" VALUES(12,'567');
INSERT INTO "ensayos" VALUES(13,'754');
INSERT INTO "ensayos" VALUES(14,'784');
INSERT INTO "ensayos" VALUES(15,'344');
INSERT INTO "ensayos" VALUES(16,'854');
INSERT INTO "ensayos" VALUES(17,'270');
INSERT INTO "ensayos" VALUES(18,'727');
CREATE TABLE repeticiones (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL,
        id_ensayos INTEGER, 
        FOREIGN KEY(id_ensayos) REFERENCES ensayos(clave));
INSERT INTO "repeticiones" VALUES(1,'155',NULL);
INSERT INTO "repeticiones" VALUES(2,'918',NULL);
INSERT INTO "repeticiones" VALUES(3,'388',NULL);
INSERT INTO "repeticiones" VALUES(4,'717',10);
INSERT INTO "repeticiones" VALUES(5,'754',10);
INSERT INTO "repeticiones" VALUES(6,'325',10);
INSERT INTO "repeticiones" VALUES(7,'647',11);
INSERT INTO "repeticiones" VALUES(8,'322',11);
INSERT INTO "repeticiones" VALUES(9,'335',11);
INSERT INTO "repeticiones" VALUES(10,'227',12);
INSERT INTO "repeticiones" VALUES(11,'873',12);
INSERT INTO "repeticiones" VALUES(12,'945',12);
INSERT INTO "repeticiones" VALUES(13,'322',13);
INSERT INTO "repeticiones" VALUES(14,'284',13);
INSERT INTO "repeticiones" VALUES(15,'421',13);
INSERT INTO "repeticiones" VALUES(16,'793',14);
INSERT INTO "repeticiones" VALUES(17,'185',14);
INSERT INTO "repeticiones" VALUES(18,'806',14);
INSERT INTO "repeticiones" VALUES(19,'504',15);
INSERT INTO "repeticiones" VALUES(20,'781',15);
INSERT INTO "repeticiones" VALUES(21,'157',15);
INSERT INTO "repeticiones" VALUES(22,'450',16);
INSERT INTO "repeticiones" VALUES(23,'696',16);
INSERT INTO "repeticiones" VALUES(24,'695',16);
INSERT INTO "repeticiones" VALUES(25,'869',17);
INSERT INTO "repeticiones" VALUES(26,'565',17);
INSERT INTO "repeticiones" VALUES(27,'360',17);
INSERT INTO "repeticiones" VALUES(28,'396',18);
INSERT INTO "repeticiones" VALUES(29,'402',18);
INSERT INTO "repeticiones" VALUES(30,'728',18);
COMMIT;

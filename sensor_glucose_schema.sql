BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `sensor_glucose` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`datetime`	DATE NOT NULL UNIQUE,
	`value`	INTEGER NOT NULL,
	`ISIG`	INTEGER
);
CREATE TABLE IF NOT EXISTS `gmi_reference_values` (
	`mean_glucose_mg_dl`	INTEGER NOT NULL CHECK(mean_glucose_mg_dl > 0),
	`up_to`	INTEGER NOT NULL,
	`gmi_x10`	INTEGER NOT NULL CHECK(gmi_x10 > 0),
	PRIMARY KEY(`mean_glucose_mg_dl`)
);
INSERT INTO `gmi_reference_values` (mean_glucose_mg_dl,up_to,gmi_x10) VALUES (100,124,57),
 (125,149,63),
 (150,174,69),
 (175,199,75),
 (200,224,81),
 (225,249,87),
 (250,274,93),
 (275,299,99),
 (300,349,105),
 (350,700,117);
CREATE VIEW last_6months as select avg(value) from sensor_glucose where date(datetime) >= date("now", "-6 months");
CREATE VIEW gmi_prediction as select cast(gmi_x10 as float) / 10 as GMI from gmi_reference_values where (select * from last_6months) between mean_glucose_mg_dl and up_to;
COMMIT;

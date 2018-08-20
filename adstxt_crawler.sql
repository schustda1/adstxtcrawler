BEGIN TRANSACTION;
DROP TABLE IF EXISTS reference.adstxt;

CREATE TABLE reference.adstxt(
       SITE_DOMAIN                  nvarchar(255)    NOT NULL,
       EXCHANGE_DOMAIN              nvarchar(255)    NOT NULL,
       -- ADSYSTEM_DOMAIN	       	    INT     NOT NULL,
       SELLER_ACCOUNT_ID            nvarchar(255)    NOT NULL,
       ACCOUNT_TYPE                 nvarchar(255)    NOT NULL,
       TAG_ID                       nvarchar(255)    NOT NULL,
       ENTRY_COMMENT                nvarchar(255)    NOT NULL,
       UPDATED                      DATE    DEFAULT GETDATE(),
    PRIMARY KEY (SITE_DOMAIN,EXCHANGE_DOMAIN,SELLER_ACCOUNT_ID)
);

-- Contribution by Ian Trider
DROP TABLE IF EXISTS reference.reference.reference.adsystem_domain;

CREATE TABLE "reference.adsystem_domain" (
	DOMAIN	TEXT,
	ID	INTEGER,
	PRIMARY KEY(DOMAIN,ID)
);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('adtech.com',11);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('aolcloud.net',11);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('appnexus.com',84);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('districtm.io',96);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('google.com',8);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('indexechange.com',48);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('indexexchange.com',48);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('indexexchnage.com',48);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('openx.com',4);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('pubmatic.com',3);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('rubicon.com',1);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('rubiconproject.com',1);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('spotx.tv',44);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('spotxchange.com',44);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('spx.smaato.com',17);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('teads.tv',94);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('pulsepoint.com',95);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('aol.com',15);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('liveintent.com',12);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('triplelift.com',83);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('teads.com',94);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('contextweb.com',95);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('sharethrough.com',97);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('districtm.ca',96);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('sovrn.com',23);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('smaato.com',17);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('coxmt.com',86);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('lijit.com',23);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('www.indexexchange.com',48);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('tremorhub.com',77);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('appnexus',84);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('advertising.com',88);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('fastlane.rubiconproject.com',1);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('33across.com',2);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('facebook.com',5);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('gumgum.com',6);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('kargo.com',7);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('brealtime.com',9);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('c.amazon-reference.adsystem.com',10);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('yieldmo.com',13);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('taboola.com',18);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('sofia.trustx.org',19);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('a9.com',10);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('amazon.com',10);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('lkqd.com',20);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('criteo.com',21);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('exponential.com',22);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('yldbt.com',25);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('rhythmone.com',24);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('technorati.com',26);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('bidfluence.com',27);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('switch.com',28);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('amazon-reference.adsystem.com',10);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('conversantmedia.com',30);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('sonobi.com',31);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('spoutable.com',32);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('trustx.org',19);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('freewheel.tv',33);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('connatix.com',34);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('lkqd.net',20);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('positivemobile.com',36);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('memeglobal.com',37);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('kixer.com',38);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('sekindo.com',39);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('360yield.com',40);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('cdn.stickyadstv.com',33);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('adform.com',41);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('streamrail.net',45);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('mathtag.com',46);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('adyoulike.com',47);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('kiosked.com',50);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('video.unrulymedia.com',51);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('meridian.sovrn.com',23);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('brightcom.com',52);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('smartadserver.com',64);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('apnexus.com',84);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('jadserve.postrelease.com',56);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('rs-stripe.com',53);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('fyber.com',54);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('inner-active.com',43);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('tidaltv.com',55);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('critero.com',21);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('advertising.amazon.com',10);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('nativo.com',56);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('media.net',57);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('www.yumenetworks.com',58);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('revcontent.com',59);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('adtech.net',11);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('go.sonobi.com',31);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('outbrain.com',60);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('ib.adnxs.com',84);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('freeskreen.com',62);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('bidtellect.com',63);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('loopme.com',65);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('vidazoo.com',66);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('videoflare.com',67);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('yahoo.com',68);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('yume.com',58);
INSERT INTO `reference.reference.adsystem_domain` VALUES ('pixfuture.com',69);

DROP TABLE IF EXISTS reference.reference.adsystem;
CREATE TABLE "reference.reference.adsystem" (
	ID	INTEGER,
	NAME	TEXT,
	CANONICAL_DOMAIN	TEXT,
	PRIMARY KEY(ID)
);
INSERT INTO `reference.adsystem` VALUES (1,'Rubicon',NULL);
INSERT INTO `reference.adsystem` VALUES (2,'33Across',NULL);
INSERT INTO `reference.adsystem` VALUES (3,'PubMatic','pubmatic.com');
INSERT INTO `reference.adsystem` VALUES (4,'OpenX','openx.com');
INSERT INTO `reference.adsystem` VALUES (5,'Facebook',NULL);
INSERT INTO `reference.adsystem` VALUES (6,'GumGum',NULL);
INSERT INTO `reference.adsystem` VALUES (7,'Kargo',NULL);
INSERT INTO `reference.adsystem` VALUES (8,'Google','google.com');
INSERT INTO `reference.adsystem` VALUES (9,'bRealtime',NULL);
INSERT INTO `reference.adsystem` VALUES (10,'Amazon',NULL);
INSERT INTO `reference.adsystem` VALUES (11,'One by AOL: Display',NULL);
INSERT INTO `reference.adsystem` VALUES (12,'LiveIntent',NULL);
INSERT INTO `reference.adsystem` VALUES (13,'Yieldmo',NULL);
INSERT INTO `reference.adsystem` VALUES (14,'MoPub',NULL);
INSERT INTO `reference.adsystem` VALUES (15,'One by AOL: Mobile','aol.com');
INSERT INTO `reference.adsystem` VALUES (17,'Smaato',NULL);
INSERT INTO `reference.adsystem` VALUES (18,'Taboola',NULL);
INSERT INTO `reference.adsystem` VALUES (19,'TrustX',NULL);
INSERT INTO `reference.adsystem` VALUES (20,'LKQD',NULL);
INSERT INTO `reference.adsystem` VALUES (21,'Criteo',NULL);
INSERT INTO `reference.adsystem` VALUES (22,'Exponential',NULL);
INSERT INTO `reference.adsystem` VALUES (23,'Sovrn',NULL);
INSERT INTO `reference.adsystem` VALUES (24,'RhythmOne',NULL);
INSERT INTO `reference.adsystem` VALUES (25,'Yieldbot',NULL);
INSERT INTO `reference.adsystem` VALUES (26,'Technorati',NULL);
INSERT INTO `reference.adsystem` VALUES (27,'Bidfluence',NULL);
INSERT INTO `reference.adsystem` VALUES (28,'Switch Concepts',NULL);
INSERT INTO `reference.adsystem` VALUES (29,'BrightRoll Exchange',NULL);
INSERT INTO `reference.adsystem` VALUES (30,'Conversant',NULL);
INSERT INTO `reference.adsystem` VALUES (31,'Sonobi',NULL);
INSERT INTO `reference.adsystem` VALUES (32,'Spoutable',NULL);
INSERT INTO `reference.adsystem` VALUES (33,'FreeWheel',NULL);
INSERT INTO `reference.adsystem` VALUES (34,'Connatix',NULL);
INSERT INTO `reference.adsystem` VALUES (35,'Centro Brand Exchange',NULL);
INSERT INTO `reference.adsystem` VALUES (36,'Positive Mobile',NULL);
INSERT INTO `reference.adsystem` VALUES (37,'MemeGlobal',NULL);
INSERT INTO `reference.adsystem` VALUES (38,'Kixer',NULL);
INSERT INTO `reference.adsystem` VALUES (39,'Sekindo',NULL);
INSERT INTO `reference.adsystem` VALUES (40,'Improve Digital','improvedigital.com');
INSERT INTO `reference.adsystem` VALUES (41,'AdForm',NULL);
INSERT INTO `reference.adsystem` VALUES (42,'MADS',NULL);
INSERT INTO `reference.adsystem` VALUES (43,'Inneractive','inner-active.com');
INSERT INTO `reference.adsystem` VALUES (44,'SpotX',NULL);
INSERT INTO `reference.adsystem` VALUES (45,'StreamRail',NULL);
INSERT INTO `reference.adsystem` VALUES (46,'MediaMath',NULL);
INSERT INTO `reference.adsystem` VALUES (47,'AdYouLike',NULL);
INSERT INTO `reference.adsystem` VALUES (48,'Index Exchange','indexexchange.com');
INSERT INTO `reference.adsystem` VALUES (49,'e-Planning',NULL);
INSERT INTO `reference.adsystem` VALUES (50,'Kiosked',NULL);
INSERT INTO `reference.adsystem` VALUES (51,'UnrulyX',NULL);
INSERT INTO `reference.adsystem` VALUES (52,'Brightcom',NULL);
INSERT INTO `reference.adsystem` VALUES (53,'PowerInbox',NULL);
INSERT INTO `reference.adsystem` VALUES (54,'Fyber','fyber.com');
INSERT INTO `reference.adsystem` VALUES (55,'TidalTV',NULL);
INSERT INTO `reference.adsystem` VALUES (56,'Nativo',NULL);
INSERT INTO `reference.adsystem` VALUES (57,'Media.net',NULL);
INSERT INTO `reference.adsystem` VALUES (58,'YuMe',NULL);
INSERT INTO `reference.adsystem` VALUES (59,'RevContent',NULL);
INSERT INTO `reference.adsystem` VALUES (60,'Outbrain',NULL);
INSERT INTO `reference.adsystem` VALUES (61,'Zedo',NULL);
INSERT INTO `reference.adsystem` VALUES (62,'SlimCut Media',NULL);
INSERT INTO `reference.adsystem` VALUES (63,'Bidtellect',NULL);
INSERT INTO `reference.adsystem` VALUES (64,'Smart RTB+',NULL);
INSERT INTO `reference.adsystem` VALUES (65,'LoopMe',NULL);
INSERT INTO `reference.adsystem` VALUES (66,'Vidazoo',NULL);
INSERT INTO `reference.adsystem` VALUES (67,'Videoflare',NULL);
INSERT INTO `reference.adsystem` VALUES (68,'Yahoo Ad Exchange',NULL);
INSERT INTO `reference.adsystem` VALUES (69,'PixFuture',NULL);
INSERT INTO `reference.adsystem` VALUES (77,'Tremor',NULL);
INSERT INTO `reference.adsystem` VALUES (83,'TripleLift',NULL);
INSERT INTO `reference.adsystem` VALUES (84,'AppNexus','appnexus.com');
INSERT INTO `reference.adsystem` VALUES (86,'COMET',NULL);
INSERT INTO `reference.adsystem` VALUES (88,'One by AOL: Video','advertising.com');
INSERT INTO `reference.adsystem` VALUES (94,'Teads','teads.tv');
INSERT INTO `reference.adsystem` VALUES (95,'PulsePoint',NULL);
INSERT INTO `reference.adsystem` VALUES (96,'District M',NULL);
INSERT INTO `reference.adsystem` VALUES (97,'Sharethrough',NULL);
COMMIT;

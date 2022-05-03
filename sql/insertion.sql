INSERT INTO library.users VALUES (1, "JAKE", "MASON", 5732025625);
INSERT INTO library.users VALUES (2, "JOHN", "DOE", 5554206969);
INSERT INTO library.users VALUES (3, "ELON", "MUSK", 3103636000);
INSERT INTO library.users VALUES (4, "BOB", "SMITH", 5739992718);

INSERT INTO library.authors VALUES (1, "CL", "RS");
INSERT INTO library.authors VALUES (2, "DOCTOR", "SEUSS");
INSERT INTO library.authors VALUES (3, "RAMEZ", "ELMASRI"); 
INSERT INTO library.authors VALUES (4, "JK", "ROWLING");
INSERT INTO library.authors VALUES (5, "JRR", "TOLKIEN");

INSERT INTO library.books VALUES ("9780262046305", 1, 1990, 3, "Aisle 2", "Algorithms");
INSERT INTO library.books VALUES ("0400307299532", 2, 1957, 3, "Asile 1", "Cat in the Hat");
INSERT INTO library.books VALUES ("9780007355914", 2, 1960, 3, "Asile 1", "Green Eggs and Ham");
INSERT INTO library.books VALUES ("9780394800790", 2, 1957, 2, "Aisle 1", "How the Grinch Stole Christmas");
INSERT INTO library.books VALUES ("9780133970777", 3, 2015, 1, "Aisle 2", "Database Systems");
INSERT INTO library.books VALUES ("9780747532743", 4, 1997, 2, "Aisle 3", "Harry Potter and the Sorcerer's Stone");
INSERT INTO library.books VALUES ("9780439064873", 4, 1998, 2, "Aisle 3", "Harry Potter and the Chamber of Secrets");
INSERT INTO library.books VALUES ("9780439136358", 4, 1999, 2, "Aisle 3", "Harry Potter and the Prisoner of Azkaban");
INSERT INTO library.books VALUES ("9780439231947", 4, 2000, 2, "Aisle 3", "Harry Potter and the Goblet of Fire");
INSERT INTO library.books VALUES ("9780439358064", 4, 2003, 2, "Aisle 3", "Harry Potter and the Order of the Phoenix");
INSERT INTO library.books VALUES ("9780439784542", 4, 2005, 2, "Aisle 3", "Harry Potter and the Half-Blood Prince");
INSERT INTO library.books VALUES ("9780545139700", 4, 2009, 2, "Aisle 3", "Harry Potter and the Deathly Hallows");
INSERT INTO library.books VALUES ("9780547928227", 5, 1937, 1, "Aisle 3", "The Hobbit");
INSERT INTO library.books VALUES ("9780345339706", 5, 1954, 1, "Aisle 3", "LTR The Fellowship of the Ring");
INSERT INTO library.books VALUES ("9780547928203", 5, 1954, 1, "Aisle 3", "LTR The Two Towers");
INSERT INTO library.books VALUES ("9780547928197", 5, 1955, 1, "Aisle 3", "LTR The Return of the King");

INSERT INTO library.computers VALUES (21, "2nd Floor");
INSERT INTO library.computers VALUES (22, "2nd Floor");
INSERT INTO library.computers VALUES (23, "2nd Floor");
INSERT INTO library.computers VALUES (24, "2nd Floor");
INSERT INTO library.computers VALUES (25, "2nd Floor");
INSERT INTO library.computers VALUES (11, "1st Floor");
INSERT INTO library.computers VALUES (12, "1st Floor");
INSERT INTO library.computers VALUES (13, "1st Floor");
INSERT INTO library.computers VALUES (14, "1st Floor");

INSERT INTO library.apps VALUES (1, "Adobe Photoshop");
INSERT INTO library.apps VALUES (2, "MATLAB");
INSERT INTO library.apps VALUES (3, "MS Paint");
INSERT INTO library.apps VALUES (4, "Google Chrome");
INSERT INTO library.apps VALUES (5, "Audacity");
INSERT INTO library.apps VALUES (6, "AutoCAD");
INSERT INTO library.apps VALUES (7, "Code::Blocks");
INSERT INTO library.apps VALUES (8, "QT Creator");
INSERT INTO library.apps VALUES (9, "Eclipse IDE");
INSERT INTO library.apps VALUES (10, "Python3");
INSERT INTO library.apps VALUES (11, "Snake");
INSERT INTO library.apps VALUES (12, "Minesweeper");
INSERT INTO library.apps VALUES (13, "TeX");

INSERT INTO library.rooms VALUES (101, 1);
INSERT INTO library.rooms VALUES (102, 1);
INSERT INTO library.rooms VALUES (103, 1);
INSERT INTO library.rooms VALUES (104, 1);
INSERT INTO library.rooms VALUES (105, 1);
INSERT INTO library.rooms VALUES (201, 2);
INSERT INTO library.rooms VALUES (202, 2);
INSERT INTO library.rooms VALUES (203, 2);

INSERT INTO library.familymembers VALUES (5732222222, 2);
INSERT INTO library.familymembers VALUES (5738885555, 4);
INSERT INTO library.familymembers VALUES (5731119876, 2);

INSERT INTO library.computeruse VALUES (1, 21);
INSERT INTO library.computeruse VALUES (2, 23);
INSERT INTO library.roomuse VALUES (2, 101);
INSERT INTO library.roomuse VALUES (1, 203);
INSERT INTO library.checkout VALUES (1, "9780262046305", str_to_date('5/28/2022', '%m/%d/%Y'));
INSERT INTO library.checkout VALUES (1, "0400307299532", str_to_date('9/14/2022', '%m/%d/%Y'));
INSERT INTO library.checkout VALUES (1, "9780133970777", str_to_date('1/14/2022', '%m/%d/%Y'));

SELECT * FROM users
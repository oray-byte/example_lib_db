CREATE SCHEMA library;

CREATE TABLE library.users (
	uid INT NOT NULL AUTO_INCREMENT,
    fname VARCHAR(80) NOT NULL,
    lname VARCHAR(80) NOT NULL,
    phone BIGINT NOT NULL,
    PRIMARY KEY (uid)
);

CREATE TABLE library.authors (
	aid INT NOT NULL AUTO_INCREMENT,
    afname VARCHAR(80) NOT NULL,
    alname VARCHAR(80) NOT NULL,
    PRIMARY KEY (aid)
);

CREATE TABLE library.books (
	isbn VARCHAR(13) NOT NULL,
    baid INT NOT NULL,
    pub_date INT NOT NULL,
    stock INT NOT NULL,
    location VARCHAR(80) NOT NULL,
    title VARCHAR(80) NOT NULL,
    PRIMARY KEY (isbn),
    FOREIGN KEY (baid) REFERENCES library.authors (aid)
    ON DELETE CASCADE,
    CONSTRAINT CHECK (stock >= 0)
);

CREATE TABLE library.checkout (
	c_uid INT NOT NULL,
    c_isbn VARCHAR(13) NOT NULL,
    due_date DATE NOT NULL,
    PRIMARY KEY (c_uid, c_isbn),
    FOREIGN KEY (c_uid) REFERENCES library.users (uid)
    ON DELETE CASCADE,
    FOREIGN KEY (c_isbn) REFERENCES library.books (isbn)
    ON DELETE CASCADE
);

CREATE TABLE library.apps (
	app_id INT NOT NULL,
    app_name VARCHAR(80) NOT NULL,
    PRIMARY KEY (app_id)
);
    
CREATE TABLE library.computers (
	comp_id INT NOT NULL,
    comp_loc VARCHAR(80) NOT NULL,
    PRIMARY KEY (comp_id)
);

CREATE TABLE library.familymembers (
	fam_phone BIGINT NOT NULL,
    fam_id INT NOT NULL,
    PRIMARY KEY (fam_phone),
    FOREIGN KEY (fam_id) REFERENCES library.users (uid)
    ON DELETE CASCADE
);

CREATE TABLE library.rooms (
	room_num INT NOT NULL,
    floor INT NOT NULL,
    PRIMARY KEY (room_num)
);

CREATE TABLE library.computeruse (
	c_uid INT NOT NULL,
    c_comp_id INT NOT NULL,
    PRIMARY KEY (c_uid, c_comp_id),
    FOREIGN KEY (c_uid) REFERENCES library.users (uid)
    ON DELETE CASCADE,
    FOREIGN KEY (c_comp_id) REFERENCES library.computers (comp_id)
    ON DELETE CASCADE
);

CREATE TABLE library.roomuse (
	r_uid INT NOT NULL,
    r_room_num INT NOT NULL,
    PRIMARY KEY (r_uid, r_room_num),
    FOREIGN KEY (r_uid) REFERENCES library.users (uid)
    ON DELETE CASCADE,
    FOREIGN KEY (r_room_num) REFERENCES library.rooms (room_num)
    ON DELETE CASCADE
);
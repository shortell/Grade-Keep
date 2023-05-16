-- teachers
INSERT INTO teachers (first_name, last_name, username, password) -- id: 1, password: password
VALUES ('Sidney', 'Velazquez', 'sv123', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'); 
INSERT INTO teachers (first_name, last_name, username, password) -- id: 2, password: password
VALUES ('Frances', 'Mccann', 'fm456', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'); 
INSERT INTO teachers (first_name, last_name, username, password) -- id: 3, password: password
VALUES ('Neo', 'Brewer', 'nb789', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'); 

-- classes
INSERT INTO classes (title, teacher_id) -- id: 1
VALUES ('Algebra I section 01', 1);

INSERT INTO classes (title, teacher_id) -- id: 2
VALUES ('Algebra I section 02', 1);

INSERT INTO classes (title, teacher_id) -- id: 3
VALUES ('AP U.S. History', 2);

INSERT INTO classes (title, teacher_id) -- id: 4
VALUES ('AP US History', 3);

INSERT INTO classes (title, teacher_id) -- id: 5
VALUES ('Global Studies', 3);
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

-- assignments
INSERT INTO assignments (title, instructions, class_id) -- id: 1
VALUES ('Essay #1', 'Write an essay on Ancient Greece and explain...', 5);

INSERT INTO assignments (title, instructions, class_id) -- id: 2
VALUES ('HW#1', 'Graph the following equations f(x)=x^2...', 1);

INSERT INTO assignments (title, instructions, class_id) -- id: 3
VALUES ('HW#1', 'Graph the following equations 1. f(x)=x^2...', 2);

INSERT INTO assignments (title, instructions, class_id) -- id: 4
VALUES ('HW#5', 'Explain how the World War I affected...', 5);

INSERT INTO assignments (title, instructions, class_id) -- id: 5
VALUES ('HW#2', 'How did John D. Rockefeller contribute too...', 4);
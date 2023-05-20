-- teachers
INSERT INTO teachers (first_name, last_name, username, password) -- id: 1, password: password
VALUES ('Sidney', 'Velazquez', 'sv123', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'); 
INSERT INTO teachers (first_name, last_name, username, password) -- id: 2, password: password
VALUES ('Frances', 'Mccann', 'fm456', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'); 
INSERT INTO teachers (first_name, last_name, username, password) -- id: 3, password: password
VALUES ('Neo', 'Brewer', 'nb789', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'); 

-- courses
INSERT INTO courses (title, teacher_id) -- id: 1
VALUES ('Algebra I section 01', 1);
INSERT INTO courses (title, teacher_id) -- id: 2
VALUES ('Algebra I section 02', 1);
INSERT INTO courses (title, teacher_id) -- id: 3
VALUES ('AP U.S. History', 2);
INSERT INTO courses (title, teacher_id) -- id: 4
VALUES ('AP US History', 3);
INSERT INTO courses (title, teacher_id) -- id: 5
VALUES ('Global Studies', 3);

-- assignments
INSERT INTO assignments (title, instructions, due, course_id) -- id: 1
VALUES ('Essay #1', 'Write an essay on Ancient Greece and explain...', '2004-10-19 10:23:54', 5);
INSERT INTO assignments (title, instructions, due, course_id) -- id: 2
VALUES ('HW#1', 'Graph the following equations f(x)=x^2...', '2004-10-19 10:23:54', 1);
INSERT INTO assignments (title, instructions, due, course_id) -- id: 3
VALUES ('HW#1', 'Graph the following equations 1. f(x)=x^2...', '2004-10-19 10:23:54', 2);
INSERT INTO assignments (title, instructions, due, course_id) -- id: 4
VALUES ('HW#5', 'Explain how the World War I affected...', '2004-10-19 10:23:54', 5);
INSERT INTO assignments (title, instructions, due, course_id) -- id: 5
VALUES ('HW#2', 'How did John D. Rockefeller contribute too...', '2004-10-19 10:23:54', 4);

-- students
INSERT INTO students (first_name, last_name, username, password) -- id: 1
VALUES ('Xanthe', 'Lawson', 'xl123', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');
INSERT INTO students (first_name, last_name, username, password) -- id: 2
VALUES ('Valentina', 'Norman', 'vn456', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');
INSERT INTO students (first_name, last_name, username, password) -- id: 3
VALUES ('Amie', 'Stanton', 'as789', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

-- submissions
INSERT INTO submissions (response, turned_in, assignment_id, student_id) -- id: 1
VALUES ('Lorem ipsum...', '2004-10-19 10:23:54', 1, 1);
INSERT INTO submissions (response, turned_in, assignment_id, student_id) -- id: 2
VALUES ('Lorem ipsum...', '2004-10-19 10:23:54', 1, 2);
INSERT INTO submissions (response, turned_in, assignment_id, student_id) -- id: 3
VALUES ('Lorem ipsum...', '2004-10-19 10:23:54', 1, 3);
INSERT INTO submissions (response, turned_in, assignment_id, student_id) -- id: 4
VALUES ('U', '2004-10-19 10:23:54', 2, 1);
INSERT INTO submissions (response, turned_in, assignment_id, student_id) -- id: 5
VALUES ('U', '2004-10-19 10:23:54', 2, 2);
INSERT INTO submissions (response, turned_in, assignment_id, student_id) -- id: 6
VALUES ('U', '2004-10-19 10:23:54', 2, 3);

-- enrollments
INSERT INTO enrollments (student_id, course_id) -- id: 1
VALUES (1, 1);
INSERT INTO enrollments (student_id, course_id) -- id: 2
VALUES (3, 1);
INSERT INTO enrollments (student_id, course_id) -- id: 3
VALUES (1, 2);
INSERT INTO enrollments (student_id, course_id) -- id: 4
VALUES (2, 2);

-- grades
INSERT INTO grades (title, total_points, course_id) -- id: 1
VALUES ('HW#1', 100, 1);
INSERT INTO grades (title, total_points, course_id) -- id: 2
VALUES ('HW#2', 100, 1);
INSERT INTO grades (title, total_points, course_id) -- id: 3
VALUES ('HW#3', 100, 1);
INSERT INTO grades (title, total_points, course_id) -- id: 4
VALUES ('HW#4', 100, 1);
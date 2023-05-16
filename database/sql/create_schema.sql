CREATE TABLE teachers (
    id SERIAL NOT NULL PRIMARY KEY,
    first_name text DEFAULT '',
    last_name text DEFAULT '',
    username text NOT NULL,
    password text NOT NULL
);

CREATE TABLE students (
    id SERIAL NOT NULL PRIMARY KEY,
    first_name text NOT NULL DEFAULT '',
    last_name text NOT NULL DEFAULT '',
    username text NOT NULL,
    password text NOT NULL
);

CREATE TABLE classes (
    id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    teacher_id integer NOT NULL 
);

CREATE TABLE enrollments (
    id SERIAL NOT NULL PRIMARY KEY,
    student_id integer NOT NULL,
    class_id integer NOT NULL
);

CREATE TABLE assignments (
    id SERIAL NOT NULL,
    title text NOT NULL,
    instructions text NOT NULL,
    class_id integer NOT NULL
);

CREATE TABLE submissions (
    id SERIAL NOT NULL,
    response text,
    assignment_id integer NOT NULL,
    student_id integer NOT NULL
);

CREATE TABLE grades (
    id SERIAL NOT NULL PRIMARY KEY,
    points_earned integer DEFAULT NULL,
    total_points integer NOT NULL,
    enrollment_id integer NOT NULL references enrollments(id)
);
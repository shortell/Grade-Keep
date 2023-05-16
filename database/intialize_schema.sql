CREATE TABLE teachers (
    id SERIAL NOT NULL PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    username text NOT NULL,
    password text NOT NULL
);

CREATE TABLE students (
    id SERIAL NOT NULL PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    username text NOT NULL,
    password text NOT NULL
);

CREATE TABLE classes (
    id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    teacher_id integer NOT NULL references teachers(id)
);

CREATE TABLE enrollments (
    id SERIAL NOT NULL PRIMARY KEY,
    student_id integer NOT NULL references students(id),
    class_id integer NOT NULL references classes(id)
);

CREATE TABLE assignments (
    id SERIAL NOT NULL,
    title text NOT NULL,
    instructions text NOT NULL,
    class_id integer NOT NULL references classes(id)
);

CREATE TABLE submissions (
    id SERIAL NOT NULL,
    response text,
    assignment_id integer NOT NULL references assignments(id),
    student_id integer NOT NULL references students(id)
);

CREATE TABLE grades (
    id SERIAL NOT NULL PRIMARY KEY,
    points_earned integer,
    total_points integer NOT NULL,
    enrollment_id integer NOT NULL references enrollments(id)
);
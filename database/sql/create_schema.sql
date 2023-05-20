CREATE TABLE teachers (
    id SERIAL NOT NULL PRIMARY KEY,
    first_name text DEFAULT '',
    last_name text DEFAULT '',
    username text NOT NULL,
    password text NOT NULL,
    UNIQUE(username)
);

CREATE TABLE students (
    id SERIAL NOT NULL PRIMARY KEY,
    first_name text NOT NULL DEFAULT '',
    last_name text NOT NULL DEFAULT '',
    username text NOT NULL,
    password text NOT NULL,
    UNIQUE(username)
);

CREATE TABLE courses (
    id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    teacher_id integer NOT NULL references teachers(id) ON DELETE CASCADE
);

CREATE TABLE enrollments (
    id SERIAL NOT NULL PRIMARY KEY,
    student_id integer NOT NULL references students(id) ON DELETE CASCADE,
    course_id integer NOT NULL references courses(id) ON DELETE CASCADE
);

CREATE TABLE assignments (
    id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    instructions text NOT NULL,
    due TIMESTAMP NOT NULL,
    course_id integer NOT NULL references courses(id) ON DELETE CASCADE
);

CREATE TABLE submissions (
    id SERIAL NOT NULL PRIMARY KEY,
    response text,
    turned_in TIMESTAMP NOT NULL,
    assignment_id integer NOT NULL references assignments(id) ON DELETE CASCADE,
    student_id integer NOT NULL references students(id) ON DELETE CASCADE
);

CREATE TABLE grades (
    id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    total_points decimal NOT NULL,
    course_id integer NOT NULL references courses(id) ON DELETE CASCADE
);

CREATE TABLE scores (
    id SERIAL NOT NULL PRIMARY KEY,
    points_earned decimal,
    grade_id integer NOT NULL references grades(id) ON DELETE CASCADE,
    student_id integer NOT NULL references students(id) ON DELETE CASCADE
);
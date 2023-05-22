CREATE TABLE teachers (
    id SERIAL NOT NULL PRIMARY KEY,
    first_name text,
    last_name text,
    username text NOT NULL,
    password text NOT NULL,
    UNIQUE(username)
);

CREATE TABLE students (
    id SERIAL NOT NULL PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    UNIQUE(username)
);

CREATE TABLE courses (
    id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    summary text DEFAULT '',
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
    posted TIMESTAMP NOT NULL,
    course_id integer NOT NULL references courses(id) ON DELETE CASCADE,
    UNIQUE(title, course_id)
);

CREATE TABLE scores (
    id SERIAL NOT NULL PRIMARY KEY,
    points_earned decimal DEFAULT NULL,
    grade_id integer NOT NULL references grades(id) ON DELETE CASCADE,
    student_id integer NOT NULL references students(id) ON DELETE CASCADE
);
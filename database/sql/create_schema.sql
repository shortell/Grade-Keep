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

CREATE TABLE classes (
    id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    teacher_id integer NOT NULL 
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
    due_date_time TIMESTAMP NOT NULL,
    class_id integer NOT NULL references classes(id)
    
);

CREATE TABLE submissions (
    id SERIAL NOT NULL,
    response text,
    assignment_id integer NOT NULL references assignments(id),
    student_id integer NOT NULL references students(id),
    submitted_date_time TIMESTAMP NOT NULL
);

CREATE TABLE grades (
    id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    total_points decimal NOT NULL,
    class_id integer NOT NULL references classes(id)
);

CREATE TABLE scores (
    id SERIAL NOT NULL PRIMARY KEY,
    points_earned decimal,
    grade_id integer NOT NULL references grades(id),
    student_id integer NOT NULL references students(id)
)
PRAGMA foreign_keys = ON;

drop table if exists admin;
create table admin (
 password text);

drop table if exists assignment;
create table assignment (
 id INTEGER PRIMARY KEY,
 title text,
 description text,
 state text,
 startdatetime text
);

drop table if exists essay;
create table essay(
 id INTEGER PRIMARY KEY,
 assignment_id INTEGER REFERENCES assignment(id) ON DELETE CASCADE,
 student_name text,
 essay_text text, 
 submitteddatetime text,
 score real);

drop table if exists essay_eval;
create table essay_eval(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 assignment_id INTEGER REFERENCES assignment(id) ON DELETE CASCADE,
 student_name text,
 essay1_id integer,
 essay2_id integer,
 essay3_id integer,
 score1 real,
 score2 real,
 score3 real 
);

# DB Lab 2 - Login & To-Do Application

## Team Members
* Salma Khaled - ID : 2304099

## Tech Stack
* Back-end: Python (Flask)
* Front-end: HTML5 / CSS3
* Database: MySQL

## How to Run
1. Install requirements: pip install flask pymysql bcrypt python-dotenv
2. Run database script: execute database/schema.sql in MySQL / DBeaver
3. Copy .env.example to .env and set your MySQL password
4. Start the server: python app.py
5. Open http://127.0.0.1:5000 in your browser

## Features & Bonus
- R1-R3: Registration, Login, Logout, Session management.
- R4-R7: To-Do list CRUD (Add, Edit, Toggle, Delete with confirmation).
- R8-R10: Dual validation, parameterized queries, responsive UI.
- Bonus:  Open tasks counter .

## Conceptual Questions & Answers
### (a) Why do UPDATE and DELETE contain AND user_id = ? and what changes if you remove it?
- Answer: It ensures database-level authorization. Without it, any user could modify or delete other users' tasks by guessing their todo_id.

### (b) What happens if you insert a to-do for a user_id that does not exist, and which constraint of the lecture is that?
- Answer: MySQL rejects it with a Foreign Key error, which enforces the Referential Integrity Constraint.

### (c) Why do you store a hash and not the password?
- Answer: To protect user security during database breaches using one-way salted hashes like bcrypt.

### (d) The name column is NOT NULL: why did you still need your own check for an empty name?
- Answer: Because NOT NULL accepts empty strings "" or spaces " ", so application checks are needed to ensure valid text.
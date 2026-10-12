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
- <img width="1920" height="823" alt="Screenshot (331)" src="https://github.com/user-attachments/assets/25c5506f-a9c1-4a39-aac2-6fc0aabd9bf9" />
<img width="1920" height="766" alt="Screenshot (333)" src="https://github.com/user-attachments/assets/59ad4989-140e-481e-9ef9-183fec2514cb" />
<img width="1920" height="813" alt="Screenshot (335)" src="https://github.com/user-attachments/assets/d68d11ed-43b1-4f55-ac3e-1eb44f2abe0d" />
<img width="942" height="767" alt="Screenshot (337)" src="https://github.com/user-attachments/assets/61825b00-f7fa-4d42-9b91-8b33c7775ebb" />

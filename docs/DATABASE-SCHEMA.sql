CREATE TABLE Admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR(255)
);

CREATE TABLE Student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    domain VARCHAR(100),
    start_date DATE,
    end_date DATE
);

CREATE TABLE Certificate (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    certificate_id VARCHAR(100) UNIQUE,
    pdf_path TEXT,
    qr_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE EmailLog (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    status VARCHAR(50),
    sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
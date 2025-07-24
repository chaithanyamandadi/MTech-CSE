CREATE DATABASE library_db;
USE library_db;
CREATE TABLE Students (
    student_id INT PRIMARY KEY NOT NULL,
    student_name VARCHAR(50) NOT NULL,
    roll_no VARCHAR(10) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    dept VARCHAR(20) NOT NULL
);
CREATE TABLE Books (
    book_id INT PRIMARY KEY NOT NULL,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(50) NOT NULL,
    pub_year INT NOT NULL,
    genre VARCHAR(50),
    total_copies INT NOT NULL,
    available_copies INT NOT NULL
);
CREATE TABLE Loans (
    loan_id INT PRIMARY KEY NOT NULL,
    student_id INT NOT NULL,
    book_id INT NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);
INSERT INTO Students (student_id, student_name, roll_no, phone, dept) VALUES
(1, 'Aarav Reddy', '21A91A001', '9876543210', 'CSE'),
(2, 'Bhavya Shah', '21A91A002', '9876543211', 'ECE'),
(3, 'Charan Verma', '21A91A003', '9876543212', 'EEE'),
(4, 'Diya Nair', '21A91A004', '9876543213', 'MECH'),
(5, 'Eshan Rao', '21A91A005', '9876543214', 'CIVIL'),
(6, 'Farhan Ali', '21A91A006', '9876543215', 'IT'),
(7, 'Gauri Iyer', '21A91A007', '9876543216', 'CSE'),
(8, 'Harshit Mehta', '21A91A008', '9876543217', 'ECE'),
(9, 'Isha Jain', '21A91A009', '9876543218', 'CSE'),
(10, 'Jayant Patil', '21A91A010', '9876543219', 'EEE');
INSERT INTO Books (book_id, title, author, publisher, pub_year, genre, total_copies, available_copies) VALUES
(101, 'Operating Systems', 'William Stallings', 'Pearson', 2018, 'Computer Science', 5, 3),
(102, 'Artificial Intelligence', 'Stuart Russell', 'Pearson', 2016, 'AI', 4, 2),
(103, 'Data Structures', 'Seymour Lipschutz', 'McGraw-Hill', 2014, 'Programming', 6, 4),
(104, 'Digital Logic Design', 'M. Morris Mano', 'Pearson', 2017, 'Electronics', 5, 5),
(105, 'Strength of Materials', 'R. K. Bansal', 'Laxmi Publications', 2015, 'Mechanical', 3, 2),
(106, 'Surveying Vol I', 'B. C. Punmia', 'Laxmi Publications', 2012, 'Civil', 4, 3),
(107, 'Object-Oriented Programming', 'E. Balagurusamy', 'McGraw-Hill', 2020, 'Programming', 6, 5),
(108, 'Database System Concepts', 'Silberschatz', 'McGraw-Hill', 2020, 'Database', 5, 4),
(109, 'Engineering Mathematics', 'B. S. Grewal', 'Khanna Publishers', 2019, 'Mathematics', 5, 1),
(110, 'Signals and Systems', 'Alan V. Oppenheim', 'PHI Learning', 2013, 'Electronics', 4, 3);
INSERT INTO Loans (loan_id, student_id, book_id, issue_date, due_date, return_date) VALUES
(1, 1, 101, '2025-05-01', '2025-05-15', NULL),
(2, 2, 103, '2025-05-02', '2025-05-16', '2025-05-14'),
(3, 3, 105, '2025-05-03', '2025-05-17', NULL),
(4, 4, 102, '2025-05-04', '2025-05-18', '2025-05-18'),
(5, 5, 106, '2025-05-05', '2025-05-19', NULL),
(6, 6, 107, '2025-05-06', '2025-05-20', NULL),
(7, 7, 108, '2025-05-07', '2025-05-21', '2025-05-20'),
(8, 8, 109, '2025-05-08', '2025-05-22', NULL),
(9, 9, 104, '2025-05-09', '2025-05-23', '2025-05-22'),
(10, 10, 110, '2025-05-10', '2025-05-24', NULL);
SELECT * FROM Students;
SELECT * FROM Books;
SELECT * FROM Loans;
SELECT s.student_name, b.title, l.issue_date, l.due_date 
FROM Loans l 
JOIN Students s ON l.student_id = s.student_id 
JOIN Books b ON l.book_id = b.book_id;
SELECT title, available_copies 
FROM Books WHERE available_copies > 0;
SELECT s.student_name, b.title, l.due_date
FROM Loans l
JOIN Students s ON l.student_id = s.student_id
JOIN Books b ON l.book_id = b.book_id
WHERE l.return_date IS NULL AND l.due_date < CURDATE();
SELECT * FROM Books;
UPDATE Books
SET available_copies = available_copies + 1
WHERE book_id = 101;
SELECT * FROM Books;
-- ============================================================
-- UPDATE CREDENTIALS FOR TESTING
-- ============================================================
-- Use these SQL statements to update the test credentials in the database
-- with the new passwords provided by the user

-- IMPORTANT: These password hashes correspond to the following credentials:
-- admin : Admin@123
-- worker1 : Worker@123  
-- officer1 : Officer@123
-- citizen1 : Citizen@123

-- ============================================================
-- EMPLOYEE CREDENTIALS UPDATES
-- ============================================================

UPDATE employees 
SET password_hash = '$2b$12$wKdxJyGHhJ0/KjL/iWkQwO9fpVh2wM.NL3Nia8iRDLP3cmfjZEji2'
WHERE username = 'admin';

UPDATE employees 
SET password_hash = '$2b$12$YAeYgiTr0fQj64.oPshk0./lQzpdqtIC3eqwtRKNmDsGa8C9Dnt76'
WHERE username = 'worker1';

UPDATE employees 
SET password_hash = '$2b$12$7ps17MQi.Yi/YAZ6f1nwfOU00P2fQzFHNk4q7AG0V7ork82vGbNHK'
WHERE username = 'officer1';

-- ============================================================
-- CITIZEN CREDENTIALS UPDATE
-- ============================================================

UPDATE citizens 
SET password_hash = '$2b$12$0l3XGXbQMMxDSD3Q7wsQS.1PSkdfc0hBE2Phz3IdaxMsa6B3eC1.2'
WHERE username = 'citizen1';

-- ============================================================
-- VERIFY UPDATES
-- ============================================================

SELECT emp_id, username, role, password_hash 
FROM employees 
WHERE username IN ('admin', 'worker1', 'officer1');

SELECT citizen_id, username, full_name, password_hash 
FROM citizens 
WHERE username = 'citizen1';

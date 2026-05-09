-- ============================================================
-- SMART CITY MANAGEMENT SYSTEM - MS SQL SERVER SCHEMA
-- ============================================================

-- Create Database
-- CREATE DATABASE SmartCityDB;
-- USE SmartCityDB;

-- ============================================================
-- CORE TABLES
-- ============================================================
CREATE DATABASE SmartCityDB;
USE SmartCityDB;

CREATE TABLE departments (
    dept_id      INT IDENTITY(1,1) PRIMARY KEY,
    dept_name    VARCHAR(100) NOT NULL UNIQUE,
    dept_code    VARCHAR(20)  NOT NULL UNIQUE,
    description  VARCHAR(500),
    head_name    VARCHAR(100),
    phone        VARCHAR(20),
    email        VARCHAR(100),
    created_at   DATETIME DEFAULT GETDATE(),
    is_active    BIT DEFAULT 1
);

CREATE TABLE employees (
    emp_id       INT IDENTITY(1,1) PRIMARY KEY,
    dept_id      INT REFERENCES departments(dept_id),
    username     VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    full_name    VARCHAR(100) NOT NULL,
    role         VARCHAR(30)  NOT NULL CHECK(role IN ('admin','officer','worker','emergency')),
    email        VARCHAR(100) UNIQUE,
    phone        VARCHAR(20),
    address      VARCHAR(300),
    hire_date    DATE DEFAULT GETDATE(),
    is_active    BIT DEFAULT 1,
    last_login   DATETIME
);

CREATE TABLE citizens (
    citizen_id   INT IDENTITY(1,1) PRIMARY KEY,
    username     VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    full_name    VARCHAR(100) NOT NULL,
    cnic         VARCHAR(15)  UNIQUE,
    email        VARCHAR(100) UNIQUE,
    phone        VARCHAR(20),
    address      VARCHAR(300),
    zone         VARCHAR(50),
    registered_at DATETIME DEFAULT GETDATE(),
    is_active    BIT DEFAULT 1
);

CREATE TABLE services (
    service_id   INT IDENTITY(1,1) PRIMARY KEY,
    dept_id      INT REFERENCES departments(dept_id),
    service_name VARCHAR(100) NOT NULL,
    description  VARCHAR(500),
    is_active    BIT DEFAULT 1
);

-- ============================================================
-- COMPLAINTS & TASKS
-- ============================================================

CREATE TABLE complaints (
    complaint_id INT IDENTITY(1,1) PRIMARY KEY,
    citizen_id   INT REFERENCES citizens(citizen_id),
    dept_id      INT REFERENCES departments(dept_id),
    title        VARCHAR(200) NOT NULL,
    description  VARCHAR(1000),
    category     VARCHAR(50),
    priority     VARCHAR(20) DEFAULT 'Normal' CHECK(priority IN ('Low','Normal','High','Critical')),
    status       VARCHAR(30) DEFAULT 'Submitted' 
                   CHECK(status IN ('Submitted','Assigned','In Progress','Resolved','Closed')),
    location     VARCHAR(200),
    submitted_at DATETIME DEFAULT GETDATE(),
    resolved_at  DATETIME,
    citizen_rating INT CHECK(citizen_rating BETWEEN 1 AND 5)
);

CREATE TABLE tasks (
    task_id      INT IDENTITY(1,1) PRIMARY KEY,
    complaint_id INT REFERENCES complaints(complaint_id),
    dept_id      INT REFERENCES departments(dept_id),
    assigned_to  INT REFERENCES employees(emp_id),
    assigned_by  INT REFERENCES employees(emp_id),
    title        VARCHAR(200) NOT NULL,
    description  VARCHAR(1000),
    priority     VARCHAR(20) DEFAULT 'Normal',
    status       VARCHAR(30) DEFAULT 'Pending'
                   CHECK(status IN ('Pending','In Progress','Completed','Cancelled')),
    due_date     DATETIME,
    created_at   DATETIME DEFAULT GETDATE(),
    completed_at DATETIME
);

-- ============================================================
-- TRAFFIC MANAGEMENT
-- ============================================================

CREATE TABLE sensors (
    sensor_id    INT IDENTITY(1,1) PRIMARY KEY,
    sensor_type  VARCHAR(50) NOT NULL,
    location     VARCHAR(200),
    zone         VARCHAR(50),
    latitude     DECIMAL(10,6),
    longitude    DECIMAL(10,6),
    status       VARCHAR(20) DEFAULT 'Active',
    installed_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE traffic_data (
    data_id      INT IDENTITY(1,1) PRIMARY KEY,
    sensor_id    INT REFERENCES sensors(sensor_id),
    intersection VARCHAR(100),
    zone         VARCHAR(50),
    vehicle_count INT DEFAULT 0,
    congestion_level VARCHAR(20) CHECK(congestion_level IN ('Low','Moderate','High','Critical')),
    signal_timing_ns INT DEFAULT 30,
    signal_timing_ew INT DEFAULT 30,
    recorded_at  DATETIME DEFAULT GETDATE()
);

-- ============================================================
-- WASTE MANAGEMENT
-- ============================================================

CREATE TABLE vehicles (
    vehicle_id   INT IDENTITY(1,1) PRIMARY KEY,
    dept_id      INT REFERENCES departments(dept_id),
    vehicle_no   VARCHAR(20) NOT NULL UNIQUE,
    vehicle_type VARCHAR(50),
    capacity_kg  INT,
    driver_name  VARCHAR(100),
    driver_phone VARCHAR(20),
    status       VARCHAR(20) DEFAULT 'Available' CHECK(status IN ('Available','On Route','Maintenance','Inactive')),
    last_service DATE
);

CREATE TABLE waste_collection (
    collection_id INT IDENTITY(1,1) PRIMARY KEY,
    vehicle_id   INT REFERENCES vehicles(vehicle_id),
    zone         VARCHAR(50),
    route_info   VARCHAR(500),
    bins_collected INT DEFAULT 0,
    weight_kg    DECIMAL(10,2),
    status       VARCHAR(30) DEFAULT 'Scheduled'
                   CHECK(status IN ('Scheduled','In Progress','Completed','Cancelled')),
    scheduled_at DATETIME,
    completed_at DATETIME,
    created_at   DATETIME DEFAULT GETDATE()
);

-- ============================================================
-- UTILITIES
-- ============================================================

CREATE TABLE utilities (
    utility_id   INT IDENTITY(1,1) PRIMARY KEY,
    citizen_id   INT REFERENCES citizens(citizen_id),
    utility_type VARCHAR(30) CHECK(utility_type IN ('Electricity','Water','Gas')),
    meter_no     VARCHAR(30) UNIQUE,
    prev_reading DECIMAL(10,2) DEFAULT 0,
    curr_reading DECIMAL(10,2) DEFAULT 0,
    units_consumed DECIMAL(10,2) DEFAULT 0,
    rate_per_unit DECIMAL(10,4) DEFAULT 0,
    reading_date DATE DEFAULT GETDATE(),
    zone         VARCHAR(50)
);

-- ============================================================
-- BILLING & PAYMENTS
-- ============================================================

CREATE TABLE payments (
    payment_id   INT IDENTITY(1,1) PRIMARY KEY,
    citizen_id   INT REFERENCES citizens(citizen_id),
    utility_id   INT REFERENCES utilities(utility_id),
    payment_type VARCHAR(30),
    amount       DECIMAL(10,2) NOT NULL,
    tax_amount   DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    status       VARCHAR(20) DEFAULT 'Pending' CHECK(status IN ('Pending','Paid','Overdue','Cancelled')),
    due_date     DATE,
    paid_at      DATETIME,
    payment_method VARCHAR(50),
    transaction_ref VARCHAR(100),
    bill_month   VARCHAR(20),
    created_at   DATETIME DEFAULT GETDATE()
);

-- ============================================================
-- INCIDENTS & ALERTS
-- ============================================================

CREATE TABLE incidents (
    incident_id  INT IDENTITY(1,1) PRIMARY KEY,
    reported_by  INT,
    dept_id      INT REFERENCES departments(dept_id),
    incident_type VARCHAR(50),
    title        VARCHAR(200),
    description  VARCHAR(1000),
    severity     VARCHAR(20) CHECK(severity IN ('Low','Medium','High','Critical')),
    status       VARCHAR(30) DEFAULT 'Open'
                   CHECK(status IN ('Open','Assigned','Responding','Resolved','Closed')),
    location     VARCHAR(200),
    latitude     DECIMAL(10,6),
    longitude    DECIMAL(10,6),
    reported_at  DATETIME DEFAULT GETDATE(),
    resolved_at  DATETIME
);

CREATE TABLE alerts (
    alert_id     INT IDENTITY(1,1) PRIMARY KEY,
    alert_type   VARCHAR(50),
    title        VARCHAR(200),
    message      VARCHAR(1000),
    severity     VARCHAR(20) DEFAULT 'Info' CHECK(severity IN ('Info','Warning','Critical')),
    target_role  VARCHAR(30),
    is_read      BIT DEFAULT 0,
    created_at   DATETIME DEFAULT GETDATE(),
    expires_at   DATETIME
);

-- ============================================================
-- INFRASTRUCTURE ASSETS
-- ============================================================

CREATE TABLE infrastructure_assets (
    asset_id     INT IDENTITY(1,1) PRIMARY KEY,
    asset_name   VARCHAR(200) NOT NULL,
    asset_type   VARCHAR(50),
    location     VARCHAR(200),
    zone         VARCHAR(50),
    status       VARCHAR(30) DEFAULT 'Operational'
                   CHECK(status IN ('Operational','Under Maintenance','Damaged','Decommissioned')),
    condition_score INT CHECK(condition_score BETWEEN 0 AND 100),
    installed_date DATE,
    last_maintained DATE,
    next_maintenance DATE,
    estimated_cost DECIMAL(12,2),
    notes        VARCHAR(500)
);

-- ============================================================
-- TRANSPORT
-- ============================================================

CREATE TABLE transport_routes (
    route_id     INT IDENTITY(1,1) PRIMARY KEY,
    route_name   VARCHAR(100),
    route_type   VARCHAR(30) CHECK(route_type IN ('Bus','Train','Metro')),
    start_point  VARCHAR(100),
    end_point    VARCHAR(100),
    stops        VARCHAR(500),
    distance_km  DECIMAL(8,2),
    fare         DECIMAL(8,2),
    frequency_min INT,
    is_active    BIT DEFAULT 1
);

CREATE TABLE tickets (
    ticket_id    INT IDENTITY(1,1) PRIMARY KEY,
    citizen_id   INT REFERENCES citizens(citizen_id),
    route_id     INT REFERENCES transport_routes(route_id),
    journey_date DATE,
    fare_paid    DECIMAL(8,2),
    seat_no      VARCHAR(10),
    status       VARCHAR(20) DEFAULT 'Active' CHECK(status IN ('Active','Used','Cancelled')),
    booked_at    DATETIME DEFAULT GETDATE(),
    transaction_ref VARCHAR(50)
);

-- ============================================================
-- ACTIVITY LOGS
-- ============================================================

CREATE TABLE activity_logs (
    log_id       INT IDENTITY(1,1) PRIMARY KEY,
    user_type    VARCHAR(20),
    user_id      INT,
    username     VARCHAR(100),
    action       VARCHAR(200),
    module       VARCHAR(50),
    details      VARCHAR(500),
    ip_address   VARCHAR(50),
    logged_at    DATETIME DEFAULT GETDATE()
);

-- ============================================================
-- STORED PROCEDURES
-- ============================================================

GO
CREATE PROCEDURE sp_submit_complaint
    @citizen_id INT, @dept_id INT, @title VARCHAR(200),
    @description VARCHAR(1000), @category VARCHAR(50),
    @priority VARCHAR(20), @location VARCHAR(200)
AS BEGIN
    INSERT INTO complaints(citizen_id,dept_id,title,description,category,priority,location)
    VALUES(@citizen_id,@dept_id,@title,@description,@category,@priority,@location);
    SELECT SCOPE_IDENTITY() AS complaint_id;
END
GO

CREATE PROCEDURE sp_assign_task
    @complaint_id INT, @dept_id INT, @assigned_to INT,
    @assigned_by INT, @title VARCHAR(200), @priority VARCHAR(20), @due_date DATETIME
AS BEGIN
    INSERT INTO tasks(complaint_id,dept_id,assigned_to,assigned_by,title,priority,due_date)
    VALUES(@complaint_id,@dept_id,@assigned_to,@assigned_by,@title,@priority,@due_date);
    UPDATE complaints SET status='Assigned' WHERE complaint_id=@complaint_id;
END
GO

CREATE PROCEDURE sp_generate_utility_bill
    @citizen_id INT, @utility_type VARCHAR(30), @meter_no VARCHAR(30),
    @curr_reading DECIMAL(10,2), @rate_per_unit DECIMAL(10,4), @bill_month VARCHAR(20)
AS BEGIN
    DECLARE @prev DECIMAL(10,2), @utility_id INT, @units DECIMAL(10,2);
    DECLARE @amount DECIMAL(10,2), @tax DECIMAL(10,2), @total DECIMAL(10,2);
    SELECT @utility_id=utility_id, @prev=curr_reading FROM utilities WHERE meter_no=@meter_no;
    SET @units = @curr_reading - @prev;
    SET @amount = @units * @rate_per_unit;
    SET @tax = @amount * 0.16;
    SET @total = @amount + @tax;
    UPDATE utilities SET prev_reading=@prev, curr_reading=@curr_reading,
        units_consumed=@units, rate_per_unit=@rate_per_unit, reading_date=GETDATE()
    WHERE utility_id=@utility_id;
    INSERT INTO payments(citizen_id,utility_id,payment_type,amount,tax_amount,total_amount,
        due_date,bill_month)
    VALUES(@citizen_id,@utility_id,@utility_type,@amount,@tax,@total,
        DATEADD(day,30,GETDATE()),@bill_month);
END
GO

CREATE PROCEDURE sp_get_dashboard_stats AS BEGIN
    SELECT
        (SELECT COUNT(*) FROM citizens WHERE is_active=1) AS total_citizens,
        (SELECT COUNT(*) FROM complaints WHERE CAST(submitted_at AS DATE)=CAST(GETDATE() AS DATE)) AS today_complaints,
        (SELECT COUNT(*) FROM complaints WHERE status NOT IN ('Resolved','Closed')) AS open_complaints,
        (SELECT COUNT(*) FROM incidents WHERE status='Open') AS open_incidents,
        (SELECT COUNT(*) FROM employees WHERE is_active=1) AS total_employees,
        (SELECT ISNULL(SUM(total_amount),0) FROM payments WHERE status='Paid'
         AND MONTH(paid_at)=MONTH(GETDATE())) AS monthly_revenue,
        (SELECT COUNT(*) FROM tasks WHERE status='Pending') AS pending_tasks,
        (SELECT COUNT(*) FROM vehicles WHERE status='On Route') AS active_vehicles;
END
GO

-- ============================================================
-- TRIGGERS
-- ============================================================

CREATE TRIGGER trg_task_completed
ON tasks AFTER UPDATE AS BEGIN
    IF UPDATE(status) BEGIN
        UPDATE complaints SET status='In Progress', resolved_at=NULL
        FROM complaints c INNER JOIN inserted i ON c.complaint_id=i.complaint_id
        WHERE i.status='In Progress';
        UPDATE complaints SET status='Resolved', resolved_at=GETDATE()
        FROM complaints c INNER JOIN inserted i ON c.complaint_id=i.complaint_id
        WHERE i.status='Completed';
    END
END
GO

CREATE TRIGGER trg_log_payment
ON payments AFTER UPDATE AS BEGIN
    IF UPDATE(status) BEGIN
        INSERT INTO activity_logs(user_type,action,module,details,logged_at)
        SELECT 'system','Payment status updated','Billing',
            'Payment #'+CAST(payment_id AS VARCHAR)+' -> '+status, GETDATE()
        FROM inserted;
    END
END
GO

-- ============================================================
-- SEED DATA
-- ============================================================

INSERT INTO departments(dept_name,dept_code,description) VALUES
('Traffic Management','TRAFFIC','Manages city traffic signals and flow'),
('Waste Management','WASTE','Handles garbage collection and disposal'),
('Utility Services','UTILITY','Manages electricity, water, gas'),
('Public Safety','SAFETY','CCTV, crime tracking, public security'),
('Emergency Services','EMERGENCY','Police, ambulance, fire brigade'),
('Transport Authority','TRANSPORT','Public buses and trains'),
('Infrastructure','INFRA','Roads, buildings, asset management'),
('Citizen Services','CITIZEN','Citizen portal and engagement');

UPDATE employees
SET password_hash = '$2b$12$cdjQR3sKv7XFcaW.ly6HGOA1TuAAHN3qzeOPsGCOObMs0PH1m6lpqs'
WHERE username = 'admin';

-- ADMIN
INSERT INTO employees
(dept_id, username, password_hash, full_name, role, email)
VALUES
(
    1,
    'admin',
    '$2b$12$DhmcTNgWYminmilJS1hat.sZ9dybM.p8i30nCNg9BCVBopJyiWDTu',
    'System Administrator',
    'admin',
    'admin@smartcity.gov.pk'
);
UPDATE employees
SET
    password_hash = '$2b$12$DhmcTNgWYminmilJS1hat.sZ9dybM.p8i30nCNg9BCVBopJyiWDTu',
    role = 'admin',
    full_name = 'System Administrator'
WHERE username = 'admin';
-- OFFICER
INSERT INTO employees
(dept_id, username, password_hash, full_name, role, email)
VALUES
(
    2,
    'officer1',
    '$2b$12$3xgTYx5vzq66opx6Q8lFR.F39hsnuC5QO8QYLYV3ATMC3W30h1GNu',
    'Traffic Officer',
    'officer',
    'officer@smartcity.gov.pk'
);

-- WORKER
INSERT INTO employees
(dept_id, username, password_hash, full_name, role, email)
VALUES
(
    2,
    'worker1',
    '$2b$12$yE4qDP047fq12PSXOL1YkOA01251Xby5mj014nCj02RaNWD5GrWxa',
    'Field Worker',
    'worker',
    'worker@smartcity.gov.pk'
);

-- EMERGENCY
INSERT INTO employees
(dept_id, username, password_hash, full_name, role, email)
VALUES
(
    5,
    'emergency1',
    '$2b$12$WlMrbyolf.5NH9.mEdzuC.ARxAt9WXVbwYiCZ/yVcm46ZmF.O2ApO',
    'Emergency Responder',
    'emergency',
    'emergency@smartcity.gov.pk'
);

-- CITIZEN
INSERT INTO citizens
(username, password_hash, full_name, cnic, email)
VALUES
(
    'citizen1',
    '$2b$12$DyqEBPS8GWGU790YAv8dtOGu6WIJb6gI2ssFLkyQ9KzuGCElDIv6C',
    'Ali Khan',
    '42101-1234567-1',
    'citizen@smartcity.pk'
);
UPDATE citizens
SET
    username = 'citizen1',
    password_hash = '$2b$12$DyqEBPS8GWGU790YAv8dtOGu6WIJb6gI2ssFLkyQ9KzuGCElDIv6C',
    full_name = 'Ali Khan',
    email = 'citizen@smartcity.pk'
WHERE cnic = '42101-1234567-1';

SELECT emp_id, username, role, password_hash
FROM employees
WHERE username = 'admin';

INSERT INTO tasks
(
    complaint_id,
    dept_id,
    assigned_to,
    assigned_by,
    title,
    description,
    priority,
    status
)
VALUES
(
    NULL,
    1,
    8,   -- ✅ worker1
    2,   -- admin assigned it
    'Fix street lights',
    'Repair broken street lights in Block A',
    'High',
    'Pending'
);
SELECT emp_id, username, role
FROM employees;

INSERT INTO tasks
(
    complaint_id,
    dept_id,
    assigned_to,
    assigned_by,
    title,
    description,
    priority,
    status
)
VALUES
(
    NULL,
    1,
    8,
    2,
    'Repair Traffic Signal',
    'Fix malfunctioning traffic signal at Clifton Bridge',
    'High',
    'Pending'
);

INSERT INTO tasks
(
    complaint_id,
    dept_id,
    assigned_to,
    assigned_by,
    title,
    description,
    priority,
    status
)
VALUES
(
    NULL,
    2,
    8,
    2,
    'Garbage Collection Route',
    'Clear waste bins in Gulshan Block 10 route',
    'Normal',
    'In Progress'
);
INSERT INTO tasks
(
    complaint_id,
    dept_id,
    assigned_to,
    assigned_by,
    title,
    description,
    priority,
    status
)
VALUES
(
    NULL,
    7,
    8,
    2,
    'Inspect Road Damage',
    'Survey potholes on Shahrah-e-Faisal section B',
    'Medium',
    'Pending'
);
"""Sample medical database schema (simplified MIMIC-like structure)."""

# SQL script to create sample medical database tables
# This is a simplified version inspired by MIMIC-III database

CREATE_TABLES_SQL = """
-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    subject_id INTEGER PRIMARY KEY,
    gender VARCHAR(1) NOT NULL,
    dob TIMESTAMP NOT NULL,
    dod TIMESTAMP,
    COMMENT '患者基本信息表'
);

COMMENT ON COLUMN patients.subject_id IS '患者唯一标识符';
COMMENT ON COLUMN patients.gender IS '性别（M/F）';
COMMENT ON COLUMN patients.dob IS '出生日期';
COMMENT ON COLUMN patients.dod IS '死亡日期';

-- Admissions table
CREATE TABLE IF NOT EXISTS admissions (
    hadm_id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL,
    admittime TIMESTAMP NOT NULL,
    dischtime TIMESTAMP,
    admission_type VARCHAR(50),
    age INTEGER,
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id),
    COMMENT '入院记录表'
);

COMMENT ON COLUMN admissions.hadm_id IS '住院唯一标识符';
COMMENT ON COLUMN admissions.subject_id IS '患者ID';
COMMENT ON COLUMN admissions.admittime IS '入院时间';
COMMENT ON COLUMN admissions.dischtime IS '出院时间';
COMMENT ON COLUMN admissions.admission_type IS '入院类型';
COMMENT ON COLUMN admissions.age IS '入院时年龄';

-- Diagnoses ICD table
CREATE TABLE IF NOT EXISTS diagnoses_icd (
    row_id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL,
    hadm_id INTEGER NOT NULL,
    icd9_code VARCHAR(10),
    seq_num INTEGER,
    long_title TEXT,
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id),
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id),
    COMMENT '诊断记录表（ICD编码）'
);

COMMENT ON COLUMN diagnoses_icd.row_id IS '记录唯一标识';
COMMENT ON COLUMN diagnoses_icd.subject_id IS '患者ID';
COMMENT ON COLUMN diagnoses_icd.hadm_id IS '住院ID';
COMMENT ON COLUMN diagnoses_icd.icd9_code IS 'ICD-9诊断代码';
COMMENT ON COLUMN diagnoses_icd.seq_num IS '诊断顺序';
COMMENT ON COLUMN diagnoses_icd.long_title IS '诊断名称';

-- Lab events table
CREATE TABLE IF NOT EXISTS labevents (
    row_id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL,
    hadm_id INTEGER,
    itemid INTEGER NOT NULL,
    charttime TIMESTAMP NOT NULL,
    valuenum DECIMAL(10,2),
    valueuom VARCHAR(20),
    flag VARCHAR(10),
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id),
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id),
    COMMENT '化验检查结果表'
);

COMMENT ON COLUMN labevents.row_id IS '记录唯一标识';
COMMENT ON COLUMN labevents.subject_id IS '患者ID';
COMMENT ON COLUMN labevents.hadm_id IS '住院ID';
COMMENT ON COLUMN labevents.itemid IS '检查项目ID';
COMMENT ON COLUMN labevents.charttime IS '检查时间';
COMMENT ON COLUMN labevents.valuenum IS '检查结果数值';
COMMENT ON COLUMN labevents.valueuom IS '单位';
COMMENT ON COLUMN labevents.flag IS '异常标记';

-- Lab items dictionary
CREATE TABLE IF NOT EXISTS d_labitems (
    itemid INTEGER PRIMARY KEY,
    label VARCHAR(100) NOT NULL,
    fluid VARCHAR(50),
    category VARCHAR(50),
    COMMENT '化验项目字典表'
);

COMMENT ON COLUMN d_labitems.itemid IS '项目ID';
COMMENT ON COLUMN d_labitems.label IS '项目名称';
COMMENT ON COLUMN d_labitems.fluid IS '样本类型';
COMMENT ON COLUMN d_labitems.category IS '项目分类';

-- ICU stays table
CREATE TABLE IF NOT EXISTS icustays (
    icustay_id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL,
    hadm_id INTEGER NOT NULL,
    intime TIMESTAMP NOT NULL,
    outtime TIMESTAMP,
    los DECIMAL(10,2),
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id),
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id),
    COMMENT 'ICU住院记录表'
);

COMMENT ON COLUMN icustays.icustay_id IS 'ICU住院唯一标识';
COMMENT ON COLUMN icustays.subject_id IS '患者ID';
COMMENT ON COLUMN icustays.hadm_id IS '住院ID';
COMMENT ON COLUMN icustays.intime IS 'ICU入院时间';
COMMENT ON COLUMN icustays.outtime IS 'ICU出院时间';
COMMENT ON COLUMN icustays.los IS 'ICU住院天数';

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_admissions_subject ON admissions(subject_id);
CREATE INDEX IF NOT EXISTS idx_admissions_time ON admissions(admittime);
CREATE INDEX IF NOT EXISTS idx_diagnoses_subject ON diagnoses_icd(subject_id);
CREATE INDEX IF NOT EXISTS idx_diagnoses_hadm ON diagnoses_icd(hadm_id);
CREATE INDEX IF NOT EXISTS idx_labevents_subject ON labevents(subject_id);
CREATE INDEX IF NOT EXISTS idx_labevents_hadm ON labevents(hadm_id);
CREATE INDEX IF NOT EXISTS idx_labevents_time ON labevents(charttime);
CREATE INDEX IF NOT EXISTS idx_icustays_subject ON icustays(subject_id);
"""

# MySQL version (without COMMENT ON syntax)
CREATE_TABLES_SQL_MYSQL = """
-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    subject_id INTEGER PRIMARY KEY,
    gender VARCHAR(1) NOT NULL COMMENT '性别（M/F）',
    dob TIMESTAMP NOT NULL COMMENT '出生日期',
    dod TIMESTAMP COMMENT '死亡日期'
) COMMENT='患者基本信息表';

-- Admissions table
CREATE TABLE IF NOT EXISTS admissions (
    hadm_id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL COMMENT '患者ID',
    admittime TIMESTAMP NOT NULL COMMENT '入院时间',
    dischtime TIMESTAMP COMMENT '出院时间',
    admission_type VARCHAR(50) COMMENT '入院类型',
    age INTEGER COMMENT '入院时年龄',
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id)
) COMMENT='入院记录表';

-- Diagnoses ICD table
CREATE TABLE IF NOT EXISTS diagnoses_icd (
    row_id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL COMMENT '患者ID',
    hadm_id INTEGER NOT NULL COMMENT '住院ID',
    icd9_code VARCHAR(10) COMMENT 'ICD-9诊断代码',
    seq_num INTEGER COMMENT '诊断顺序',
    long_title TEXT COMMENT '诊断名称',
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id),
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id)
) COMMENT='诊断记录表（ICD编码）';

-- Lab events table
CREATE TABLE IF NOT EXISTS labevents (
    row_id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL COMMENT '患者ID',
    hadm_id INTEGER COMMENT '住院ID',
    itemid INTEGER NOT NULL COMMENT '检查项目ID',
    charttime TIMESTAMP NOT NULL COMMENT '检查时间',
    valuenum DECIMAL(10,2) COMMENT '检查结果数值',
    valueuom VARCHAR(20) COMMENT '单位',
    flag VARCHAR(10) COMMENT '异常标记',
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id),
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id)
) COMMENT='化验检查结果表';

-- Lab items dictionary
CREATE TABLE IF NOT EXISTS d_labitems (
    itemid INTEGER PRIMARY KEY,
    label VARCHAR(100) NOT NULL COMMENT '项目名称',
    fluid VARCHAR(50) COMMENT '样本类型',
    category VARCHAR(50) COMMENT '项目分类'
) COMMENT='化验项目字典表';

-- ICU stays table
CREATE TABLE IF NOT EXISTS icustays (
    icustay_id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL COMMENT '患者ID',
    hadm_id INTEGER NOT NULL COMMENT '住院ID',
    intime TIMESTAMP NOT NULL COMMENT 'ICU入院时间',
    outtime TIMESTAMP COMMENT 'ICU出院时间',
    los DECIMAL(10,2) COMMENT 'ICU住院天数',
    FOREIGN KEY (subject_id) REFERENCES patients(subject_id),
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id)
) COMMENT='ICU住院记录表';

-- Create indexes for better query performance
CREATE INDEX idx_admissions_subject ON admissions(subject_id);
CREATE INDEX idx_admissions_time ON admissions(admittime);
CREATE INDEX idx_diagnoses_subject ON diagnoses_icd(subject_id);
CREATE INDEX idx_diagnoses_hadm ON diagnoses_icd(hadm_id);
CREATE INDEX idx_labevents_subject ON labevents(subject_id);
CREATE INDEX idx_labevents_hadm ON labevents(hadm_id);
CREATE INDEX idx_labevents_time ON labevents(charttime);
CREATE INDEX idx_icustays_subject ON icustays(subject_id);
"""

# Sample data insertion script
INSERT_SAMPLE_DATA = """
-- Insert sample patients
INSERT INTO patients (subject_id, gender, dob, dod) VALUES
(1, 'M', '1960-05-15 00:00:00', NULL),
(2, 'F', '1975-08-22 00:00:00', NULL),
(3, 'M', '1988-03-10 00:00:00', NULL);

-- Insert sample admissions
INSERT INTO admissions (hadm_id, subject_id, admittime, dischtime, admission_type, age) VALUES
(101, 1, '2024-01-15 10:30:00', '2024-01-22 14:00:00', 'EMERGENCY', 63),
(102, 2, '2024-02-10 08:00:00', '2024-02-12 16:30:00', 'ELECTIVE', 48),
(103, 3, '2024-03-05 14:20:00', NULL, 'EMERGENCY', 35);

-- Insert sample diagnoses
INSERT INTO diagnoses_icd (row_id, subject_id, hadm_id, icd9_code, seq_num, long_title) VALUES
(1, 1, 101, '250.00', 1, 'Diabetes mellitus without mention of complication'),
(2, 1, 101, '401.9', 2, 'Essential hypertension'),
(3, 2, 102, '486', 1, 'Pneumonia, organism unspecified'),
(4, 3, 103, 'U07.1', 1, 'COVID-19');

-- Insert sample lab items
INSERT INTO d_labitems (itemid, label, fluid, category) VALUES
(50809, 'Glucose', 'Blood', 'Chemistry'),
(50912, 'Creatinine', 'Blood', 'Chemistry'),
(51221, 'Hematocrit', 'Blood', 'Hematology');

-- Insert sample lab events
INSERT INTO labevents (row_id, subject_id, hadm_id, itemid, charttime, valuenum, valueuom, flag) VALUES
(1, 1, 101, 50809, '2024-01-15 12:00:00', 8.5, 'mmol/L', 'abnormal'),
(2, 1, 101, 50912, '2024-01-15 12:00:00', 1.2, 'mg/dL', 'normal'),
(3, 2, 102, 50809, '2024-02-10 09:00:00', 5.5, 'mmol/L', 'normal');

-- Insert sample ICU stays
INSERT INTO icustays (icustay_id, subject_id, hadm_id, intime, outtime, los) VALUES
(1001, 1, 101, '2024-01-15 11:00:00', '2024-01-18 09:00:00', 2.92),
(1002, 3, 103, '2024-03-05 15:00:00', NULL, NULL);
"""

"""Few-shot examples for medical Text-to-SQL."""

# Sample few-shot examples in Chinese for medical domain
FEWSHOT_EXAMPLES = [
    {
        "question": "统计2024年住院超过7天的成年患者人数。",
        "sql": """SELECT COUNT(DISTINCT a.hadm_id)
FROM admissions a
WHERE a.admittime >= '2024-01-01'
  AND a.admittime < '2025-01-01'
  AND EXTRACT(DAY FROM (a.dischtime - a.admittime)) > 7
  AND a.age >= 18;"""
    },
    {
        "question": "查询最近30天内有新冠肺炎诊断的患者数量。",
        "sql": """SELECT COUNT(DISTINCT d.subject_id)
FROM diagnoses_icd d
INNER JOIN admissions a ON d.hadm_id = a.hadm_id
WHERE d.long_title LIKE '%COVID%' OR d.long_title LIKE '%coronavirus%'
  AND a.admittime >= CURRENT_DATE - INTERVAL '30 day';"""
    },
    {
        "question": "统计糖尿病患者的平均年龄。",
        "sql": """SELECT AVG(a.age) as avg_age
FROM admissions a
INNER JOIN diagnoses_icd d ON a.hadm_id = d.hadm_id
WHERE d.long_title LIKE '%diabetes%';"""
    },
    {
        "question": "查询住院时间最长的前10位患者的基本信息。",
        "sql": """SELECT 
  a.subject_id,
  a.hadm_id,
  a.admittime,
  a.dischtime,
  EXTRACT(DAY FROM (a.dischtime - a.admittime)) as stay_days
FROM admissions a
WHERE a.dischtime IS NOT NULL
ORDER BY stay_days DESC
LIMIT 10;"""
    },
    {
        "question": "统计每种诊断类型的患者数量，按数量降序排列。",
        "sql": """SELECT 
  d.long_title as diagnosis,
  COUNT(DISTINCT d.subject_id) as patient_count
FROM diagnoses_icd d
GROUP BY d.long_title
ORDER BY patient_count DESC
LIMIT 20;"""
    },
    {
        "question": "查询血糖检验结果异常（大于7.0）的患者记录。",
        "sql": """SELECT 
  l.subject_id,
  l.hadm_id,
  l.charttime,
  l.valuenum as glucose_value
FROM labevents l
WHERE l.itemid IN (SELECT itemid FROM d_labitems WHERE label LIKE '%glucose%')
  AND l.valuenum > 7.0
ORDER BY l.charttime DESC;"""
    },
    {
        "question": "统计男性和女性患者的住院次数。",
        "sql": """SELECT 
  p.gender,
  COUNT(a.hadm_id) as admission_count
FROM patients p
INNER JOIN admissions a ON p.subject_id = a.subject_id
GROUP BY p.gender;"""
    },
    {
        "question": "查询在ICU住院的患者平均住院天数。",
        "sql": """SELECT AVG(EXTRACT(DAY FROM (i.outtime - i.intime))) as avg_icu_days
FROM icustays i
WHERE i.outtime IS NOT NULL;"""
    }
]


# Medical terminology mappings
MEDICAL_TERMINOLOGY = {
    "糖尿病": ["diabetes", "DM"],
    "新冠肺炎": ["COVID", "COVID-19", "coronavirus"],
    "高血压": ["hypertension", "HTN"],
    "心脏病": ["heart disease", "cardiac"],
    "肺炎": ["pneumonia"],
    "血糖": ["glucose", "blood sugar"],
    "血压": ["blood pressure", "BP"],
    "化验": ["lab", "laboratory"],
    "检验": ["test", "exam"]
}

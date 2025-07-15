from faker import Faker
import pandas as pd
import random
fake = Faker()

num_records = 500

# Student IDs from 1 to 500
student_ids = list(range(1, num_records + 1))

soft_skills_data = []

for soft_skill_id, student_id in enumerate(student_ids, start=1):
    soft_skills_data.append({
        "SOFT_SKILL_ID": soft_skill_id,
        "STUDENT_ID": student_id,
        "COMMUNICATION_SKILLS_SCORE": random.randint(1, 100),
        "TEAMWORK_SKILLS_SCORE": random.randint(1, 100),
        "PRESENTATION_SKILLS_SCORE": random.randint(1, 100),
        "LEADERSHIP_SKILLS_SCORE": random.randint(1, 100),
        "CRITICAL_THINKING_SKILLS": random.randint(1, 100),
        "INTERPERSONAL_SKILLS_SCORE": random.randint(1, 100)
    })

df_soft_skills = pd.DataFrame(soft_skills_data)
df_soft_skills.to_csv("soft_skills_data.csv", index=False)
print("✅ soft_skills_data.csv file with 500 records has been created.")


import mysql.connector


# Load CSV
df = pd.read_csv("soft_skills_data.csv")

vp=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
user="2Bn9GPDTn4d78GT.root",password="WADB5559BSuHEttL",
port=4000, database="placement_eligibility_app")

cursor =vp.cursor()

# Insert each row
for _, row in df.iterrows():
    sql = """
    INSERT IGNORE INTO soft_skills (
        SOFT_SKILL_ID, STUDENT_ID,
        COMMUNICATION_SKILLS_SCORE, TEAMWORK_SKILLS_SCORE,
        PRESENTATION_SKILLS_SCORE, LEADERSHIP_SKILLS_SCORE,
        CRITICAL_THINKING_SKILLS, INTERPERSONAL_SKILLS_SCORE
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        int(row["SOFT_SKILL_ID"]),
        int(row["STUDENT_ID"]),
        int(row["COMMUNICATION_SKILLS_SCORE"]),
        int(row["TEAMWORK_SKILLS_SCORE"]),
        int(row["PRESENTATION_SKILLS_SCORE"]),
        int(row["LEADERSHIP_SKILLS_SCORE"]),
        int(row["CRITICAL_THINKING_SKILLS"]),
        int(row["INTERPERSONAL_SKILLS_SCORE"])
    )
    cursor.execute(sql, values)

# Commit & close
vp.commit()
print("✅ Data inserted into soft_skills table successfully.")
cursor.close()
vp.close()
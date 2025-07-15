import pandas as pd
from faker import Faker
import random

fake = Faker()
data = []

student_ids = list(range(1, 501))  # Assumes student IDs from 1 to 500

for i, student_id in enumerate(student_ids):
    placement_status = random.choice(['Placed', 'NotPlaced'])
    company_name = fake.company() if placement_status == 'Placed' else ''
    placement_package = random.randint(400000, 1500000) if placement_status == 'Placed' else 0
    placement_date = fake.date_between(start_date='-1y', end_date='today') if placement_status == 'Placed' else None
    
    data.append({
        "PLACEMENT_ID": i + 1,
        "STUDENT_ID": student_id,
        "MOCK_INTERVIEW_SCORE": random.randint(40, 100),
        "INTERNSHIPS_COMPLETED": random.randint(0, 3),
        "PLACEMENT_STATUS": placement_status,
        "COMPANY_NAME": company_name,
        "PLACEMENT_PACKAGE": placement_package,
        "INTERVIEW_ROUNDS_CLEARED": random.randint(0, 5),
        "PLACEMENT_DATE": placement_date
    })

df = pd.DataFrame(data)
df.to_csv("placement_table_data.csv", index=False)
print("✅ placement_table_data.csv created with 500 records.")





import mysql.connector


# Read CSV file
df = pd.read_csv("placement_table_data.csv")
df = df.where(pd.notnull(df), None)

# Connect to MySQL
vp=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
user="2Bn9GPDTn4d78GT.root",password="WADB5559BSuHEttL",
port=4000, database="placement_eligibility_app")

cursor =vp.cursor()

# Insert records
query = """
    INSERT IGNORE INTO placement_table (
        PLACEMENT_ID, STUDENT_ID, MOCK_INTERVIEW_SCORE,
        INTERNSHIPS_COMPLETED, PLACEMENT_STATUS,
        COMPANY_NAME, PLACEMENT_PACKAGE,
        INTERVIEW_ROUNDS_CLEARED, PLACEMENT_DATE
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    # Convert NaN or empty date to None
    placement_date = row['PLACEMENT_DATE'] if pd.notna(row['PLACEMENT_DATE']) else None

    cursor.execute(query, (
        int(row['PLACEMENT_ID']),
        int(row['STUDENT_ID']),
        int(row['MOCK_INTERVIEW_SCORE']),
        int(row['INTERNSHIPS_COMPLETED']),
        row['PLACEMENT_STATUS'],
        row['COMPANY_NAME'],
        int(row['PLACEMENT_PACKAGE']),
        int(row['INTERVIEW_ROUNDS_CLEARED']),
        placement_date
    ))

# Commit and close
vp.commit()
cursor.close()
vp.close()
print("✅ Data inserted into MySQL from placement_table_data.csv")
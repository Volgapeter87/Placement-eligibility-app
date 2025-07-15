import streamlit as st
import pandas as pd
import numpy as np


from faker import Faker
import random
import csv
fake=Faker()




languages = ['Python', 'Java', 'C++', 'JavaScript', 'Go', 'Rust', 'C#', 'Ruby']

# Open input student data CSV
with open('student_data.csv', 'r', encoding='utf-8') as student_file:
    student_reader = csv.DictReader(student_file)

    # Open output CSV file
    with open('programming_data.csv', 'w', newline='', encoding='utf-8') as prog_file:
        writer = csv.writer(prog_file)

        # Write header
        writer.writerow([
            'PROGRAMMING_ID',
            'STUDENT_ID',
            'LANGUAGE',
            'PROBLEMS_SOLVED',
            'ASSESMENTS_COMPLETED',
            'MINI_PROJECTS_COMPLETED',
            'CERTIFICATIONS_EARNED',
            'LATEST_PROJECT_SCORE'
        ])

        # Loop through each student and write programming data
        programming_id = 1
        for row in student_reader:
            student_id = row['Student_ID']
            language = random.choice(languages)
            problems_solved = random.randint(10, 500)
            assessments_completed = random.randint(1, 20)
            mini_projects_completed = random.randint(0, 5)
            certifications_earned = random.randint(0, 3)
            latest_project_score = round(random.uniform(50.0, 100.0), 2)

            writer.writerow([
                programming_id,
                student_id,
                language,
                problems_solved,
                assessments_completed,
                mini_projects_completed,
                certifications_earned,
                latest_project_score
            ])

            programming_id += 1

print("✅ 'programming_data.csv' created with 500 records.")





cursor = vp.cursor()

# Step 2: Open and insert CSV data
with open('programming_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header

    for row in reader:
        cursor.execute("""
            INSERT IGNORE INTO programming 
            (PROGRAMMING_ID, STUDENT_ID, `LANGUAGE`, PROBLEMS_SOLVED, ASSESMENTS_COMPLETED, MINI_PROJECTS_COMPLETED, CERTIFICATIONS_EARNED, LATEST_PROJECT_SCORE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, row)

# Step 3: Commit & close
vp.commit()
cursor.close()
vp.close()

print("✅ Data inserted into 'programming' table successfully.")

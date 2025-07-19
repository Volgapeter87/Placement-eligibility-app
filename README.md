Placement Eligibility App

This project is a web-based dashboard built using Streamlit,Python and MySQL to track student progress and determine their placement eligibility based on various academic and soft skill metrics.

Features:
✅ Student data management
✅ Programming & soft skills assessment tracking
✅ Placement performance visualization
✅ Eligibility filtering by custom criteria
✅ Dashboard with top performers and placement summaries

Database Schema:
The database used is placement_eligibility_app and includes the following tables:
students: Basic student details
programming: Coding skills and project performance
soft_skills: Communication and interpersonal skills
placement_table: Placement history and status

Insertion:
Generate data using Faker library.
Insert the data to the tables 

How to Run the App:
Requirements
Python 3.9+
MySQL Server (or TiDB Cloud)
Streamlit
Pandas
mysql-connector-python


Install Dependencies:
pip install streamlit pandas mysql-connector-python faker
Run the Streamlit App
streamlit run Placement_eligibility_app.py

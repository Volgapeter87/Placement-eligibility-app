import streamlit as st
import pandas as pd
import mysql.connector




# --- Database Handler Class ---
class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def fetch_eligible_students(self, filters):
        query = f'''
        SELECT 
            s.STUDENT_ID, s.NAME, s.EMAIL, s.COURSE_BATCH, s.GRADUATION_YEAR,
            p.PROBLEMS_SOLVED, p.ASSESMENTS_COMPLETED, p.LATEST_PROJECT_SCORE,
            pt.MOCK_INTERVIEW_SCORE, pt.PLACEMENT_STATUS, pt.COMPANY_NAME
        FROM students s
        JOIN programming p ON s.STUDENT_ID = p.STUDENT_ID
        JOIN placement_table pt ON s.STUDENT_ID = pt.STUDENT_ID
        WHERE p.PROBLEMS_SOLVED >= {filters['problems_solved']}
          AND p.ASSESMENTS_COMPLETED >= {filters['assessments_completed']}
          AND p.LATEST_PROJECT_SCORE >= {filters['latest_project_score']}
          AND pt.MOCK_INTERVIEW_SCORE >= {filters['mock_interview_score']}
        '''
        df = pd.read_sql(query, self.connection)
        return df

    def run_query(self, query):
        return pd.read_sql(query, self.connection)

    def close_connection(self):
        self.connection.close()


# --- Streamlit App Class ---
class PlacementEligibilityApp:
    def __init__(self):
        self.db = DatabaseHandler(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            user="2Bn9GPDTn4d78GT.root",
            password="WADB5559BSuHEttL",
            database="placement_eligibility_app"
        )

    def run(self):
        st.set_page_config(page_title="Placement Eligibility App", layout="wide")
        st.title("🎯 Placement Eligibility Checker")

        st.sidebar.header("📋 Filter Criteria")
        filters = {
            "problems_solved": st.sidebar.slider("Min Problems Solved", 0, 500, 100),
            "assessments_completed": st.sidebar.slider("Min Assessments Completed", 0, 100, 10),
            "latest_project_score": st.sidebar.slider("Min Project Score", 0, 100, 60),
            "mock_interview_score": st.sidebar.slider("Min Mock Interview Score", 0, 100, 50)
        }

        try:
            df = self.db.fetch_eligible_students(filters)
            st.subheader("🧑‍🎓 Eligible Students")
            if not df.empty:
                st.dataframe(df)
                st.success(f"{len(df)} students match your criteria.")
            else:
                st.warning("No students match the criteria.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            self.db.close_connection()


# ---------- Dashboard Class ----------
class PlacementDashboard:
    def __init__(self):
        self.db = DatabaseHandler(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            user="2Bn9GPDTn4d78GT.root",
            password="WADB5559BSuHEttL",
            database="placement_eligibility_app"
        )
        self.query_options = {
            "1. Top 5 best performers in the current year": """
                SELECT s.STUDENT_ID, s.NAME, s.GRADUATION_YEAR, p.LATEST_PROJECT_SCORE
                FROM students s
                JOIN programming p ON s.STUDENT_ID = p.STUDENT_ID
                WHERE s.GRADUATION_YEAR = YEAR(CURDATE())
                ORDER BY p.LATEST_PROJECT_SCORE DESC
                LIMIT 5
            """,
            "2. Who are all placed candidates": """
                SELECT s.STUDENT_ID, s.NAME, pt.COMPANY_NAME, pt.PLACEMENT_DATE
                FROM students s
                JOIN placement_table pt ON s.STUDENT_ID = pt.STUDENT_ID
                WHERE pt.PLACEMENT_STATUS = 'Placed'
            """,
            "3. Top 5 performers in communication": """
                SELECT s.STUDENT_ID, s.NAME, ss.COMMUNICATION_SKILLS_SCORE
                FROM students s
                JOIN soft_skills ss ON s.STUDENT_ID = ss.STUDENT_ID
                ORDER BY ss.COMMUNICATION_SKILLS_SCORE DESC
                LIMIT 5
            """,
            "4. Top 5 performers in teamwork": """
                SELECT s.STUDENT_ID, s.NAME, ss.TEAMWORK_SKILLS_SCORE
                FROM students s
                JOIN soft_skills ss ON s.STUDENT_ID = ss.STUDENT_ID
                ORDER BY ss.TEAMWORK_SKILLS_SCORE DESC
                LIMIT 5
            """,
            "5. Top 5 performers in presentation": """
                SELECT s.STUDENT_ID, s.NAME, ss.PRESENTATION_SKILLS_SCORE
                FROM students s
                JOIN soft_skills ss ON s.STUDENT_ID = ss.STUDENT_ID
                ORDER BY ss.PRESENTATION_SKILLS_SCORE DESC
                LIMIT 5
            """,
            "6. Top 5 performers in critical thinking": """
                SELECT s.STUDENT_ID, s.NAME, ss.CRITICAL_THINKING_SKILLS
                FROM students s
                JOIN soft_skills ss ON s.STUDENT_ID = ss.STUDENT_ID
                ORDER BY ss.CRITICAL_THINKING_SKILLS DESC
                LIMIT 5
            """,
            "7. Top 5 performers in leadership skills": """
                SELECT s.STUDENT_ID, s.NAME, ss.LEADERSHIP_SKILLS_SCORE
                FROM students s
                JOIN soft_skills ss ON s.STUDENT_ID = ss.STUDENT_ID
                ORDER BY ss.LEADERSHIP_SKILLS_SCORE DESC
                LIMIT 5
            """,
            "8. Top 5 performers in interpersonal skills": """
                SELECT s.STUDENT_ID, s.NAME, ss.INTERPERSONAL_SKILLS_SCORE
                FROM students s
                JOIN soft_skills ss ON s.STUDENT_ID = ss.STUDENT_ID
                ORDER BY ss.INTERPERSONAL_SKILLS_SCORE DESC
                LIMIT 5
            """,
            "9. Least scored candidates (last 10 by project score)": """
                SELECT s.STUDENT_ID, s.NAME, p.LATEST_PROJECT_SCORE
                FROM students s
                JOIN programming p ON s.STUDENT_ID = p.STUDENT_ID
                ORDER BY p.LATEST_PROJECT_SCORE ASC
                LIMIT 10
            """,
            "10. Top 10 eligible candidates for placement": """
                SELECT s.STUDENT_ID, s.NAME, p.LATEST_PROJECT_SCORE, pt.MOCK_INTERVIEW_SCORE
                FROM students s
                JOIN programming p ON s.STUDENT_ID = p.STUDENT_ID
                JOIN placement_table pt ON s.STUDENT_ID = pt.STUDENT_ID
                WHERE p.LATEST_PROJECT_SCORE > 70 AND pt.MOCK_INTERVIEW_SCORE > 60
                ORDER BY p.LATEST_PROJECT_SCORE DESC, pt.MOCK_INTERVIEW_SCORE DESC
                LIMIT 10
            """
        }

    def run(self):
        st.set_page_config(page_title="Placement Dashboard", layout="wide")
        st.title("📊 Placement Insights - Dashboard")

        selected_query = st.selectbox("📌 Select a query to view results:", list(self.query_options.keys()))

        if selected_query:
            sql = self.query_options[selected_query]
            try:
                df = self.db.run_query(sql)
                st.dataframe(df)
                st.success(f"✅ Query executed successfully. {len(df)} records found.")
            except Exception as e:
                st.error(f"❌ Error executing query: {e}")

        self.db.close_connection()


# ---------- Main Runner ----------
if __name__ == "__main__":
    tab = st.sidebar.radio("Select Mode", ["Eligibility Checker", "Placement Dashboard"])

    if tab == "Eligibility Checker":
        app = PlacementEligibilityApp()
        app.run()
    else:
        dash = PlacementDashboard()
        dash.run()
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Student Result Analyzer", layout="centered")

# Title
st.title("🎓 Student Result Analyzer")
st.write("Upload a CSV file containing student marks to analyze results.")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Data")
    st.dataframe(df)

    # Required columns check
    required_columns = {"Name", "Maths", "Science", "English", "History", "Computer"}
    if not required_columns.issubset(df.columns):
        st.error("❌ CSV must contain columns: Name, Maths, Science, English, History, Computer")
    else:
        # ---------------- DATA PROCESSING ----------------
        df["Total"] = df.iloc[:, 1:].sum(axis=1)
        df["Percentage"] = df["Total"] / (len(df.columns) - 1)

        def grade(p):
            if p >= 90:
                return "A+"
            elif p >= 80:
                return "A"
            elif p >= 70:
                return "B"
            elif p >= 60:
                return "C"
            else:
                return "Fail"

        df["Grade"] = df["Percentage"].apply(grade)

        # ---------------- FINAL RESULTS ----------------
        st.subheader("📊 Final Results")
        st.dataframe(df)

        # ---------------- TOPPER ----------------
        topper = df.loc[df["Percentage"].idxmax()]
        st.success(f"🏆 Class Topper: {topper['Name']} ({topper['Percentage']:.2f}%)")

        # ---------------- SUBJECT AVERAGE ----------------
        subject_avg = df.iloc[:, 1:6].mean()

        # ---------------- DOWNLOAD FINAL CSV ----------------
        st.subheader("⬇️ Download Final Result (CSV)")
        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Final Results",
            data=csv_data,
            file_name="final_student_results.csv",
            mime="text/csv"
        )

        # ---------------- SUMMARY REPORT (TEXT) ----------------
        st.subheader("📝 Result Summary Report")

        summary_text = f"""
STUDENT RESULT SUMMARY REPORT
-----------------------------
Total Students: {len(df)}

Class Topper:
Name: {topper['Name']}
Percentage: {topper['Percentage']:.2f}%

Strongest Subject:
{subject_avg.idxmax()}

Weakest Subject:
{subject_avg.idxmin()}

Grade Distribution:
{df['Grade'].value_counts().to_string()}
        """

        st.text(summary_text)

        # ---------------- DOWNLOAD SUMMARY REPORT ----------------
        st.download_button(
            label="Download Summary Report (TXT)",
            data=summary_text,
            file_name="result_summary.txt",
            mime="text/plain"
        )

        # ---------------- VISUALIZATION ----------------
        st.subheader("📈 Subject-wise Average Marks")
        fig1, ax1 = plt.subplots()
        subject_avg.plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Marks")
        st.pyplot(fig1)

        st.subheader("📉 Student Percentage Comparison")
        fig2, ax2 = plt.subplots()
        ax2.bar(df["Name"], df["Percentage"])
        ax2.set_ylabel("Percentage")
        st.pyplot(fig2)

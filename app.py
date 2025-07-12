import streamlit as st
import tempfile
import os
from src.AI_Resume_Checker.graph.graphbuilder import run_workflow
from src.AI_Resume_Checker.state.state import ResumeState

st.set_page_config(page_title="AI Resume Evaluator", layout="centered")
st.title("💼 AI Resume Evaluator")

st.markdown("Upload your **Resume**, enter your target **Job Role**,enter your **Experience** and optionally paste a **Job Description**.")

# Sidebar Info
with st.sidebar:
    st.info("This app compares your resume with job requirements and shows a skill **Match Score** and **Recommendations** based on current market where you need to focus.")

# Input fields
uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx", "txt"])
job_role = st.text_input("🧑‍💼 Job Role", placeholder="e.g., Data Scientist")
experience = st.number_input("📈 Years of Experience", min_value=0, max_value=50, value=2)
job_description = st.text_area("📋 Optional Job Description (Paste)", placeholder="Optional if not available")

# Process button
if st.button("🚀 Analyze Resume"):
    if not uploaded_file or not job_role:
        st.error("Please upload your resume and provide a job role.")
    else:
        with st.spinner("🔄Processing your resume..."):

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.read())
                resume_path = tmp.name

            # Build ResumeState for LangGraph
            state: ResumeState = {
                "path": resume_path,
                "job_role": job_role,
                "experience": experience,
            }

            if job_description.strip():
                state["job_description"] = job_description.strip()

            try:
                graph = run_workflow()
                result: ResumeState = graph.invoke(state)

                # Display results
                st.success("✅ Resume analysis complete!")

                st.markdown("### 🎯 Match Score")
                match_percent = result.get("match_percent", 0)
                st.metric("Skill Match %", f"{match_percent:.2f}%")


                st.markdown("### 🛠️ Recommended Skills to Learn or Add")

                recommendations = result.get("recommendations", [])

                if recommendations:
                    # Format recommendations as a bullet list with white font color
                    formatted_recommendations = "<ul style='color: white;'>"
                    for skill in recommendations[:20]:
                        formatted_recommendations += f"<li>{skill}</li>"
                    formatted_recommendations += "</ul>"

                    st.markdown(formatted_recommendations, unsafe_allow_html=True)
                else:
                    st.info("🎉 Your resume covers all the required skills!")


            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                os.unlink(resume_path)

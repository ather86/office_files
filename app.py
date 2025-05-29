import streamlit as st
from story_generator_with_nlp import smart_story

st.set_page_config(page_title="User Story Generator", layout="centered")

st.title("Technical & Functional User Story Generator")
st.markdown("""
Use natural language to describe a **feature or use case**, and get:
- Functional user story
- Technical developer story
- Gherkin-style acceptance criteria
""")

use_case = st.text_area("Enter a functional prompt or use case:", height=150)

if st.button("Generate User Stories"):
    if use_case.strip():
        user_story, dev_story, ac = smart_story(use_case)
        st.subheader("Functional User Story")
        st.success(user_story)

        st.subheader("Technical (Developer) Story")
        st.info(dev_story)

        st.subheader("Acceptance Criteria (Gherkin Style)")
        st.code(ac, language="gherkin")
    else:
        st.warning("Please enter a use case to generate stories.")
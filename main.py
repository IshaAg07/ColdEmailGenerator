# main.py
import streamlit as st
import requests
from bs4 import BeautifulSoup

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    st.title("📧 Cold Mail Generator")

    url_input = st.text_input("Enter a URL:", value="https://about.puma.com/en/jobs/analyst-it-bi-r36458")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url_input, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            title_tag = soup.find("h1") or soup.find("title")
            job_title = title_tag.get_text(strip=True) if title_tag else "Unknown Role"

            job_section = soup.find("main") or soup.find("section") or soup
            raw_text = job_section.get_text(separator=" ", strip=True)

            cleaned = clean_text(raw_text)
            cleaned = cleaned[:4000]  # safety trim

            combined_text = f"Job Title: {job_title}\n\n{cleaned}"

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(combined_text, fallback_title=job_title)

            for job in jobs:
                job["role"] = job_title  # override role to ensure accuracy
                job_role = job.get("role", "").strip()
                job_description = job.get("description", "").strip()

                # 🆕 Normalize role to general role
                general_role = portfolio.map_to_general_role(job_role)

                experience = portfolio.query_experience_by_role(general_role)
                email = llm.write_mail(job_role, job_description, experience)

                st.subheader(f"Email for Role: {job_role}")
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    import os
    print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))

    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)

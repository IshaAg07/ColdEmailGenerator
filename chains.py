import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load .env from the app root
load_dotenv(dotenv_path="app/.env")


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-70b-8192"
        )

    def extract_jobs(self, cleaned_text, fallback_title=None):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            Your job is to extract the main job posting from the scraped page content above.

            Only extract **one** job posting (the primary one).

            Return a valid JSON object with exactly these keys:
            - `role`: The job title as exactly written on the page (e.g., "Software Development Engineer I 2025").
            - `experience`: A very brief summary (1–2 sentences) of the required or preferred experience.
            - `skills`: A list or sentence of key skills required (e.g., "Python, AWS, microservices").
            - `description`: A clean, short paragraph summarizing the role and its responsibilities.

            Do not invent or guess any values.
            Do not return arrays. Return a single JSON object.

            ### OUTPUT (STRICTLY VALID JSON, NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            job_data = json_parser.parse(res.content)
            if fallback_title and job_data.get("role") and fallback_title.lower() not in job_data["role"].lower():
                job_data["role"] = fallback_title
        except OutputParserException:
            raise OutputParserException("Context too big or response was malformed. Unable to parse jobs.")
        return [job_data]

    def write_mail(self, role, job_description, experience):
        prompt_email = PromptTemplate.from_template(
            """
### JOB DESCRIPTION:
{job_description}

### YOUR EXPERIENCE:
{experience}

### INSTRUCTION:
You are an enthusiastic job seeker writing a cold email for the role above.

Only use the experience and job description provided. Do **not** invent any job titles, numbers, or achievements not mentioned. Stick to facts.

Write an email that:
- Begins with: “Hey, I hope you are doing well.”
- Then says: “Hi, I just came across the {{role}} position and I believe I’d be a great fit. Here’s why:”
- Includes **3 bullet points**, each 2–3 lines.
    - Start each bullet with: “Your role is focused on…”, “The job mentions…”, or “You’re looking for someone skilled in…”
    - Back it up using only the provided experience.
- Ends with: “Would you be open to a quick coffee chat this week to explore this further?”
- Then write:
    Thank you and warm regards,  
    Isha Agrawal  
    Email: ishaagrawal2000@gmail.com  
    GitHub: https://github.com/IshaAg07

Keep it real and natural. Avoid buzzwords or exaggeration.

### EMAIL (NO PREAMBLE):
"""
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "role": role,
            "job_description": str(job_description),
            "experience": experience
        })

        raw_email = res.content
        return fix_title_in_email(raw_email, role)


def fix_title_in_email(email_text: str, correct_title: str):
    import re
    # Replace the job title in the first matching sentence
    return re.sub(
        r"(Hi, I just came across the )(.*?)( position and I believe I’d be a great fit)",
        rf"\1{correct_title}\3",
        email_text
    )


if __name__ == "__main__":
    print("GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))

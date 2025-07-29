
# 📧 Cold Email Generator for Job Applications

This project automates the process of generating personalized cold emails based on job postings using LangChain, LLM (Groq LLaMA-3-70B), ChromaDB, and your prior experiences.

## 🔥 Key Features

- 🔍 **Scrapes job descriptions from public job posting URLs**
- 🧠 **Parses and summarizes job responsibilities and required skills using LLM**
- 🧾 **Matches relevant experience from your portfolio using vector embeddings**
- ✉️ **Generates a tailored cold email using LLM based on the role and matched experience**

---

## 📁 Project Structure

```

.
├── app/
│   ├── main.py               # Streamlit UI application
│   ├── chains.py             # LangChain prompts to extract job info & generate emails
│   ├── portfolio.py          # Loads experience CSV & performs similarity search using ChromaDB
│   ├── utils.py              # Helper function to clean scraped HTML text
│   ├── resource/
│   │   └── my\_portfolio.csv  # CSV of your real experience entries (job-role mapped)
│   └── .env                  # Contains GROQ\_API\_KEY
├── vectorstore/              # Local storage for ChromaDB vectors (auto-created)
├── requirements.txt          # List of required Python libraries
├── README.md                 # You're reading this 📖

````

---

## 🧠 How It Works

1. **Streamlit UI** takes a job posting URL from the user.
2. **BeautifulSoup** scrapes the HTML and extracts the job title + description.
3. **LangChain with LLaMA-3.70B (via Groq)** is used to:
   - Extract structured job role and requirements
   - Write a cold email tailored to that role
4. **ChromaDB** searches your past experience (`my_portfolio.csv`) to find relevant bullet points for the job.
5. **Email** is generated with 3 specific matching reasons, followed by your contact info.

---

## 📥 Prerequisites

- Python 3.10 or later
- A valid Groq API Key from https://console.groq.com/keys
- The following Python libraries:

```bash
pip install -r requirements.txt
````

### requirements.txt

```text
streamlit
requests
beautifulsoup4
pandas
chromadb
python-dotenv
langchain
langchain_groq
```

---

## 🔑 Environment Variable

Create a `.env` file inside the `app/` directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## 📂 Your Portfolio Format

CSV file: `app/resource/my_portfolio.csv`

| general\_role    | Experience                                            | Skills                         |
| ---------------- | ----------------------------------------------------- | ------------------------------ |
| Data Analyst     | Built Power BI dashboards to track churn and revenue. | Power BI, SQL, Python          |
| Machine Learning | Trained models using Scikit-learn and deployed APIs.  | Scikit-learn, FastAPI, AWS     |
| QA Engineer      | Wrote UI and API test automation frameworks.          | Selenium, Jenkins, RestAssured |

Use only these types of values for `general_role`:
✅ `Software Engineer`, `Data Analyst`, `Machine Learning`, `Data Scientist`, `QA Engineer`, `Data Engineer`

---

## 🚀 How to Run

### Step 1: Start the Streamlit app

```bash
streamlit run app/main.py
```

### Step 2: Use the UI

1. Paste a job listing URL (e.g., from LinkedIn, Adobe, Puma, etc.)
2. Click "Submit"
3. Cold email gets generated with relevant experience auto-injected 🎯

---

## 🛠️ Tips

* Works best with public job listings having clear titles and descriptions.
* Make sure `general_role` values in CSV are consistent (see list above).
* You can add multiple experiences for the same role in the CSV.

---


## 📬 Author

**Isha Agrawal**
Email: `ishaagrawal2000@gmail.com`
GitHub: [@IshaAg07](https://github.com/IshaAg07)

---



import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path

        # Use alternate encoding fallback
        try:
            self.data = pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            self.data = pd.read_csv(file_path, encoding="ISO-8859-1")

        self.chroma_client = chromadb.PersistentClient("vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Experience"]],
                    metadatas=[{
                        "role": row["general_role"],
                        "skills": row["Skills"]
                    }],
                    ids=[str(uuid.uuid4())]
                )

    def query_experience_by_role(self, job_role):
        role_query = job_role.lower()
        results = self.collection.query(
            query_texts=[role_query],
            n_results=2
        )
        metadatas = results.get("metadatas", [[]])[0]
        experiences = [meta["role"] + ": " + doc for meta, doc in zip(metadatas, results["documents"][0])]
        return "\n\n".join(experiences)

    def map_to_general_role(self, job_title):
        title_lower = job_title.lower()
        mapping = {
            "data analyst": ["data analyst", "business analyst", "financial analyst", "portfolio analyst", "healthcare analyst"],
            "data scientist": ["data scientist", "research scientist", "quantitative researcher"],
            "software engineer": ["software engineer", "developer", "full stack", "frontend", "backend"],
            "qa engineer": ["qa engineer", "quality engineer", "test engineer", "automation engineer", "performance engineer"],
            "ml engineer": ["ml engineer", "machine learning", "ai engineer"],
            "data engineer": ["data engineer", "etl developer"]
        }
        for general, keywords in mapping.items():
            if any(k in title_lower for k in keywords):
                return general.replace("_", " ").title()
        return "Data Analyst"  # default fallback

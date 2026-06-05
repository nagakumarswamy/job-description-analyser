import google.generativeai as genai
import json

# ── Configuration ─────────────────────────────────────────────────────────────
# Get your FREE API key from: https://aistudio.google.com/app/apikey
API_KEY = "your-gemini-api-key-here"

MY_PROFILE = """
Name: Chinimilli Naga Kumar Swamy
Skills: Python, SQL, Pandas, NumPy, BeautifulSoup, Prompt Engineering,
        GitHub, Power BI, MySQL, Excel, AWS Basics, Data Cleaning,
        Data Visualization, EDA, Dashboard Building
Experience: Fresher (0-1 years)
Education: B.E. Electronics and Communication Engineering
"""

PROMPT_TEMPLATE = """
You are an expert job description analyser.
Given a job description, return ONLY a valid JSON object with no extra text.
The JSON must have exactly these keys:
- required_skills: list of required skills (strings)
- experience_level: one of "Fresher", "Junior", "Mid-level", "Senior"
- key_responsibilities: list of top 3 responsibilities (strings)
- match_score: integer 0-100 based on how well the candidate profile matches
- missing_skills: list of skills in the JD that the candidate lacks
- recommendation: one sentence advice for the candidate

Candidate Profile:
{profile}

Job Description:
{job}
"""

# ── Core Function ─────────────────────────────────────────────────────────────
def analyse_job(job_description: str) -> dict:
    """Analyse a job description using Gemini API."""
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = PROMPT_TEMPLATE.format(
        profile=MY_PROFILE,
        job=job_description
    )

    response = model.generate_content(prompt)
    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def print_result(result: dict):
    """Print the analysis result in a readable format."""
    print("\n" + "="*50)
    print("        JOB DESCRIPTION ANALYSIS RESULT")
    print("="*50)
    print(f"\nExperience Level : {result.get('experience_level', 'N/A')}")
    print(f"Match Score      : {result.get('match_score', 0)}/100")

    print("\nRequired Skills:")
    for skill in result.get("required_skills", []):
        print(f"  - {skill}")

    print("\nKey Responsibilities:")
    for i, resp in enumerate(result.get("key_responsibilities", []), 1):
        print(f"  {i}. {resp}")

    print("\nMissing Skills (gaps to fill):")
    missing = result.get("missing_skills", [])
    if missing:
        for skill in missing:
            print(f"  - {skill}")
    else:
        print("  None — great match!")

    print(f"\nRecommendation:\n  {result.get('recommendation', '')}")
    print("="*50 + "\n")


# ── Sample Job Descriptions ───────────────────────────────────────────────────
sample_jobs = [
    """
    Job Title: Junior Data Analyst
    Company: TechCorp India

    Requirements:
    - Strong SQL skills for querying large datasets
    - Proficiency in Python and Pandas for data manipulation
    - Experience with Power BI or Tableau for dashboards
    - Good understanding of data cleaning and EDA
    - Knowledge of Excel for reporting
    - Basic cloud knowledge (AWS or Azure) is a plus

    Responsibilities:
    - Analyse business data and generate reports
    - Build dashboards to track KPIs
    - Clean and validate incoming data from multiple sources
    """,

    """
    Job Title: Associate Software Engineer
    Company: Accenture

    Requirements:
    - Python programming with OOP concepts
    - Basic knowledge of SQL databases
    - Familiarity with version control (GitHub/Git)
    - Understanding of REST APIs
    - Good problem-solving and debugging skills
    - Knowledge of AI tools is a plus

    Responsibilities:
    - Develop and maintain Python-based applications
    - Write and optimise SQL queries
    - Collaborate with team using GitHub
    """
]

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("AI-Powered Job Description Analyser")
    print("Powered by Google Gemini API (Free)\n")

    for i, jd in enumerate(sample_jobs, 1):
        print(f"Analysing Job {i}...")
        try:
            result = analyse_job(jd)
            print_result(result)
        except json.JSONDecodeError:
            print("Error: Could not parse response as JSON.")
        except Exception as e:
            print(f"Error: {e}")

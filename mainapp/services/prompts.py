def summary_prompt(text: str) -> str:
    return f"""
Summarize the following study notes in clear, concise language.
Use bullet points where helpful.

TEXT:
{text}
"""


def flashcards_prompt(text: str) -> str:
    return f"""
Generate flashcards from the text below.

Return STRICT JSON in this format:
[
  {{ "question": "...", "answer": "..." }}
]

TEXT:
{text}
"""



ALLOWED_SUBJECTS = [
    "Physics",
    "Mathematics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "Economics",
    "History",
    "Literature",
    "Engineering",
    "Other"
]


def subject_prompt(text: str) -> str:
    prompt = f"""
    You are an academic classifier.

    TASK:
    - Identify the main subject of the text
    - Choose ONE subject from this list only:
    {", ".join(ALLOWED_SUBJECTS)}

    RULES:
    - Return ONLY the subject name
    - No explanation
    - No punctuation

    TEXT:
    {text[:3000]}
    """
    return prompt


def format_notes(text):
    prompt = f"""
You are an academic note formatter.

Fix spelling and grammar.
Organize content with headings and bullet points.
Do NOT add new information.
Keep it concise and study-ready.


Text:
{text}
"""
    return prompt
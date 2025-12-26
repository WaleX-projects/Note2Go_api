from paddleocr import PaddleOCR
from google import genai
import os
from typing import List



def process_ocr(extracted_text: str):

    # Prompt for LLM cleanup and formatting
    contents = f"""
The following text was extracted from an image using Optical Character Recognition (OCR) and may contain recognition errors:

{extracted_text}

Your task is to:

Fix OCR-related errors, including spelling, grammar, and punctuation.

Preserve the original meaning, intent, and tone of the text.

Improve clarity and readability without changing the content.

Organize the text into a clean, professional document structure.

Use headings, paragraphs, and bullet points where appropriate.

Do not add new information unless it is strictly necessary for clarity.

Return only the final, fully formatted document text. Do not include explanations, comments, or metadata.
"""

    # Initialize Gemini client using environment variable (SECURE)
    client = genai.Client(
        api_key='AIzaSyAbhf6Aqd1NTk6-SM5IHL3zJbWnA3ZiZKs'
    )

    # Generate refined document
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )

    return response


def process_image(file_path: str) -> str:
    """
    Extracts text from an image using PaddleOCR and refines it
    into a clean, formatted document using Gemini.
    """

    # Initialize OCR once per call (can be global if reused often)
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )

    # Run OCR
    result = ocr.predict(input=file_path)

    # Safely extract recognized text lines
    extracted_lines: List[str] = result[0].get("rec_texts", [])
    extracted_text = "\n".join(extracted_lines)
    processed_text = process_ocr(extracted_text)
    return processed_text
    

def summerisation_agent():
    pass

def explanations():
    pass

def find_resources():
    pass
if __name__ == '__main__':
    item = process_ocr('thi sis a text of percence ok thst is a wrong spelling error thi ai stuff should hepl with that')
    print(item)
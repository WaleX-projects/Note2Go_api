from google import genai
import os
from typing import List

from django.conf import settings

def generate(prompt: str) -> str:
    
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY 
    )

    # Generate refined document
    response = client.models.generate_content(
        model=settings.AI_MODEL,
        contents=prompt
    )
    
    return response.text

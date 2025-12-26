from paddleocr import PaddleOCR
from typing import List

def extract_text(image_path) -> str:
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
    result = ocr.predict(input=image_path)

    # Safely extract recognized text lines
    extracted_lines: List[str] = result[0].get("rec_texts", [])
    extracted_text = "\n".join(extracted_lines)
    
    return extracted_text 
    
import cv2
import easyocr
import re

class ImageRecognizer:
    def __init__(self):
        # Initialize EasyOCR reader
        self.reader = easyocr.Reader(['en'])

    def recognize_text(self, frame):
        """
        Recognize text from a given image frame.
        - Converts the image to grayscale.
        - Uses EasyOCR to extract text data.
        - Filters text based on a regex pattern for registration numbers.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        results = self.reader.readtext(gray)
        for bbox, text, prob in results:
            # Remove spaces from the detected text
            text = text.replace(' ', '')
            # Filter text with 3 letters, 2 digits, and 1 letter or digit
            if prob > 0.6 and re.match(r'^[A-Z]{3}\d{2}[A-Z\d]$', text):
                return text
        return None  # No valid text found

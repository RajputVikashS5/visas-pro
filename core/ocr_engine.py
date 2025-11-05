import pytesseract
from PIL import ImageGrab

def ocr_text():
    screenshot = ImageGrab.grab()
    return pytesseract.image_to_string(screenshot).strip()
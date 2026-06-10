from PIL import Image, ImageOps, ImageFilter
import pytesseract


def preprocess_image(image_path):
    """Improve OCR readability with lightweight preprocessing."""
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)
    image = image.convert("L")
    image = ImageOps.autocontrast(image)
    image = image.filter(ImageFilter.SHARPEN)
    return image


def extract_text(image_path):
    """Extract text from an uploaded label image."""
    image = preprocess_image(image_path)
    return pytesseract.image_to_string(image)

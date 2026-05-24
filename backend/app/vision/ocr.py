from __future__ import annotations

import io

from PIL import Image


def _paddle_ocr(image: Image.Image) -> str | None:
    try:
        from paddleocr import PaddleOCR
    except Exception:
        return None

    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(image, cls=True)
    lines = []
    for line in result[0] if result else []:
        lines.append(line[1][0])
    return '\n'.join(lines)


def _tesseract_ocr(image: Image.Image) -> str:
    import pytesseract

    return pytesseract.image_to_string(image)


def extract_text(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    text = _paddle_ocr(image)
    if text:
        return text
    return _tesseract_ocr(image)

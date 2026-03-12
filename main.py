from fastapi import FastAPI, UploadFile, File, Form
import uvicorn
import cv2
import easyocr
import numpy as np
import re
import difflib
import logging

# 1. Configure the Production Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - QA_MICROSERVICE - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Batch Verification API")

logger.info("Booting up QA Microservice. Initializing EasyOCR Model...")
reader = easyocr.Reader(["en"])


def enhance_image_for_easyocr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    enhanced_color = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
    return enhanced_color


def extract_text_easyocr(image):
    strict_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    results = reader.readtext(
        image,
        detail=0,
        allowlist=strict_chars,
        mag_ratio=2.5,
        contrast_ths=0.05,
        adjust_contrast=0.5,
    )
    return " ".join(results)


def validate_batch_number(extracted_text, expected_batch):
    cleaned_extracted = re.sub(r"[^A-Z0-9]", "", extracted_text.upper())
    cleaned_expected = re.sub(r"[^A-Z0-9]", "", expected_batch.upper())

    similarity_ratio = difflib.SequenceMatcher(
        None, cleaned_extracted, cleaned_expected
    ).ratio()
    match = similarity_ratio >= 0.90

    return {
        "raw_ocr": extracted_text,
        "cleaned_extracted": cleaned_extracted,
        "expected_batch": cleaned_expected,
        "confidence_score": round(similarity_ratio * 100, 2),
        "match": match,
        "alert_required": not match,
    }


@app.post("/verify-batch")
async def verify_batch(expected_batch: str = Form(...), file: UploadFile = File(...)):
    logger.info(
        f"Incoming Request -> Expected Batch: '{expected_batch}' | Image: '{file.filename}'"
    )

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        logger.error("Failed to decode uploaded image. Corrupted file?")
        return {"error": "Invalid image file provided."}

    enhanced_img = enhance_image_for_easyocr(image)
    extracted_text = extract_text_easyocr(enhanced_img)
    result_payload = validate_batch_number(extracted_text, expected_batch)

    # 2. Log the Final Decision for the Audit Trail
    if result_payload["match"]:
        logger.info(
            f"✅ PASS: Read '{result_payload['cleaned_extracted']}'. Confidence: {result_payload['confidence_score']}%"
        )
    else:
        logger.warning(
            f"❌ FAIL: Expected '{result_payload['expected_batch']}' but read '{result_payload['cleaned_extracted']}'. Triggering DMO Alert!"
        )

    return result_payload


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

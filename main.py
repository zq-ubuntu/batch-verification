import cv2
import easyocr
import re
import difflib  # <-- NEW IMPORT

print("Initializing EasyOCR Model...")
reader = easyocr.Reader(["en"])


def get_cropped_roi(image):
    print("Please draw a box around the batch number on the neck of the bottle.")
    print("Press ENTER or SPACE to confirm the crop. Press 'c' to cancel.")
    r = cv2.selectROI(
        "Select Batch Number", image, showCrosshair=True, fromCenter=False
    )
    cropped = image[int(r[1]) : int(r[1] + r[3]), int(r[0]) : int(r[0] + r[2])]
    cv2.destroyWindow("Select Batch Number")
    return cropped


def extract_text_easyocr(image):
    print("Running EasyOCR on the cropped area...")
    results = reader.readtext(image, detail=0)
    text = " ".join(results)
    return text


def validate_batch_number(extracted_text, expected_batch):
    # 1. Regex Clean: Remove weird symbols
    cleaned_extracted = re.sub(r"[^A-Z0-9]", "", extracted_text.upper())
    cleaned_expected = re.sub(r"[^A-Z0-9]", "", expected_batch.upper())

    # 2. Calculate Fuzzy Similarity Score (0.0 to 1.0)
    similarity_ratio = difflib.SequenceMatcher(
        None, cleaned_extracted, cleaned_expected
    ).ratio()

    # 3. Define our threshold (e.g., 80% similar is considered a pass)
    # You can tweak this number up or down depending on how strict you want to be
    THRESHOLD = 0.80
    match = similarity_ratio >= THRESHOLD

    # 4. Build the response payload
    response = {
        "raw_ocr": extracted_text,
        "cleaned_extracted": cleaned_extracted,
        "expected_batch": cleaned_expected,
        "confidence_score": round(similarity_ratio * 100, 2),  # Convert to percentage
        "match": match,
        "alert_required": not match,
    }

    return response


if __name__ == "__main__":
    image_path = "sample-batch.jpg"

    # --- MOCK DMO DATA ---
    EXPECTED_BATCH_FROM_DMO = (
        "BEST BEFORE END 0427 599698-02"  # Put your actual batch number here
    )
    # ---------------------

    original_image = cv2.imread(image_path)

    if original_image is None:
        print(f"Error: Could not load image at {image_path}. Check the path.")
    else:
        cropped_img = get_cropped_roi(original_image)

        if cropped_img.size != 0:
            extracted_text = extract_text_easyocr(cropped_img)

            # Run the updated Day 4 Fuzzy Validation Logic
            validation_results = validate_batch_number(
                extracted_text, EXPECTED_BATCH_FROM_DMO
            )

            print("\n--- DAY 4: VALIDATION RESULTS ---")
            print(f"1. Raw OCR Found      : '{validation_results['raw_ocr']}'")
            print(
                f"2. Cleaned Extracted  : '{validation_results['cleaned_extracted']}'"
            )
            print(f"3. Expected by DMO    : '{validation_results['expected_batch']}'")
            print(f"4. Match Confidence   : {validation_results['confidence_score']}%")
            print("---------------------------------")
            if validation_results["match"]:
                print(
                    f"✅ MATCH SUCCESSFUL (Score: {validation_results['confidence_score']}%). No alert needed."
                )
            else:
                print(
                    f"❌ MISMATCH DETECTED (Score: {validation_results['confidence_score']}%). Triggering DMO Alert!"
                )
            print("---------------------------------\n")

            cv2.imshow("Cropped Original", cropped_img)
            print("Press 'q' or 'ESC' in the image window to close.")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Crop cancelled or invalid.")

import cv2
import easyocr
import re

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
    # 1. Regex Clean: Remove everything that is NOT A-Z or 0-9, and make uppercase
    cleaned_extracted = re.sub(r"[^A-Z0-9]", "", extracted_text.upper())
    cleaned_expected = re.sub(r"[^A-Z0-9]", "", expected_batch.upper())

    # 2. Check for an exact clean match
    match = cleaned_extracted == cleaned_expected

    # 3. Build the response payload (This is what your DMO will eventually read)
    response = {
        "raw_ocr": extracted_text,
        "cleaned_extracted": cleaned_extracted,
        "expected_batch": cleaned_expected,
        "match": match,
        "alert_required": not match,
    }

    return response


if __name__ == "__main__":
    image_path = "sample-batch.jpg"

    # --- MOCK DMO DATA ---
    # Change this to whatever the batch number on your sample photo ACTUALLY is
    EXPECTED_BATCH_FROM_DMO = "BEST BEFORE END 0427 599698-02"
    # ---------------------

    original_image = cv2.imread(image_path)

    if original_image is None:
        print(f"Error: Could not load image at {image_path}. Check the path.")
    else:
        cropped_img = get_cropped_roi(original_image)

        if cropped_img.size != 0:
            extracted_text = extract_text_easyocr(cropped_img)

            # Run the Day 4 Validation Logic
            validation_results = validate_batch_number(
                extracted_text, EXPECTED_BATCH_FROM_DMO
            )

            print("\n--- DAY 4: VALIDATION RESULTS ---")
            print(f"1. Raw OCR Found      : '{validation_results['raw_ocr']}'")
            print(
                f"2. Cleaned Extracted  : '{validation_results['cleaned_extracted']}'"
            )
            print(f"3. Expected by DMO    : '{validation_results['expected_batch']}'")
            print("---------------------------------")
            if validation_results["match"]:
                print("✅ MATCH SUCCESSFUL. No alert needed.")
            else:
                print("❌ MISMATCH DETECTED. Triggering DMO Alert!")
            print("---------------------------------\n")

            cv2.imshow("Cropped Original", cropped_img)
            print("Press 'q' or 'ESC' in the image window to close.")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Crop cancelled or invalid.")

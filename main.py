import cv2
import pytesseract
import numpy as np


def get_cropped_roi(image):
    print("Please draw a box around the batch number on the neck of the bottle.")
    print("Press ENTER or SPACE to confirm the crop. Press 'c' to cancel.")
    r = cv2.selectROI(
        "Select Batch Number", image, showCrosshair=True, fromCenter=False
    )
    cropped = image[int(r[1]) : int(r[1] + r[3]), int(r[0]) : int(r[0] + r[2])]
    cv2.destroyWindow("Select Batch Number")
    return cropped


def preprocess_image(image):
    # 1. Upscale the image by 2x
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # 2. Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Apply a very slight blur
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # 4. Adaptive Thresholding (Inverted)
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # 5. Morphological Dilation (Smudging the dot-matrix dots together)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(binary, kernel, iterations=1)

    # 6. Invert back to black text on white background
    final_processed = cv2.bitwise_not(dilated)

    # 7. Add a 20-pixel white border (Fixed: single value 255 for grayscale)
    final_processed = cv2.copyMakeBorder(
        final_processed, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255
    )

    return final_processed


def extract_text(processed_image):
    print("Running OCR on the cropped area...")

    # Try the strict single-line configuration first
    custom_config = r"--oem 3 --psm 7"

    try:
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        return text
    except pytesseract.pytesseract.TesseractError:
        print("Tesseract crashed on psm 7 (no text found). Falling back to psm 6...")
        # Fallback to the uniform block configuration which handles empty reads better
        fallback_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(processed_image, config=fallback_config)
        return text


if __name__ == "__main__":
    image_path = "sample-batch.jpg"
    original_image = cv2.imread(image_path)

    if original_image is None:
        print(f"Error: Could not load image at {image_path}. Check the path.")
    else:
        cropped_img = get_cropped_roi(original_image)

        if cropped_img.size != 0:
            processed_crop = preprocess_image(cropped_img)
            extracted_batch = extract_text(processed_crop)

            print("\n--- OCR EXTRACTION RESULTS ---")
            print(f"Raw Extracted Text:\n{extracted_batch}")
            print("------------------------------\n")

            cv2.imshow("Cropped Original", cropped_img)
            cv2.imshow("Processed Crop for OCR", processed_crop)
            print("Press 'q' or 'ESC' in any window to close.")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Crop cancelled or invalid.")

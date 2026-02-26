import cv2


def load_and_show_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Check if the image was successfully loaded
    if image is None:
        print(f"Error: Could not load image at {image_path}. Check the path.")
        return

    # Display the image in a window
    cv2.imshow("Original Batch Image", image)

    print("Image loaded successfully. Press 'q' or 'ESC' in the image window to close.")

    # Wait indefinitely until a key is pressed
    cv2.waitKey(0)

    # Clean up and close windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Replace with the actual name of your sample-image
    load_and_show_image("sample-batch.jpg")
